import os
import shutil

import git
from appapy.common.cli import (
    do_ask,
    do_ask_until_confirmed,
    do_parameter,
    do_selection_until_confirmed,
)
from appapy.common.constants import DRY_RUN, command_dir, common_dirs
from appapy.common.env import get_home
from appapy.common.shell import run
from appapy.templating.choices import ChoiceCollections
from appapy.templating.owner import owners
from appapy.templating.repository import Repository
from appapy.templating.template import Template
from colorama.ansi import Fore, Style


class TemplateProcessor:
    def process(self, repo: Repository, template: Template):

        repo.year.value = "2021"
        self.get_directory(repo, template)
        self.parse_directory(repo, template)

        owner_index = do_selection_until_confirmed(
            repo.owner.confirmation_message, owners, repo.owner.selection_message
        )
        owner = owners[owner_index]
        repo.owner.value = owner.name
        repo.ownerid.value = owner.key

        self.extract_project(repo, template)
        self.extract_technology(repo, template)
        self.extract_author(repo, template)

        repo.author.value = do_ask_until_confirmed(
            repo.author.value,
            repo.author.confirmation_message,
            repo.author.enter_message,
            repo.author.enter_validation,
        )

        repo.project.value = do_ask_until_confirmed(
            repo.project.value,
            repo.project.confirmation_message,
            repo.project.enter_message,
            repo.project.enter_validation,
        )

        repo.technology.value = do_ask_until_confirmed(
            repo.technology.value,
            repo.technology.confirmation_message,
            repo.technology.enter_message,
            repo.technology.enter_validation,
        )

        template.extract_library(repo)
        template.get_display_name(repo)
        template.get_package(repo)

        if len(owner.license_options) == 0:
            license = ChoiceCollections.license_lookup["NONE"]
        elif len(owner.license_options) == 1:
            license = owner.license_options[0]
        else:
            license_index = do_selection_until_confirmed(
                repo.license.confirmation_message,
                owner.license_options,
                repo.license.selection_message,
            )
            license = owner.license_options[license_index]

        repo.license.value = license.key
        repo.licenseid.value = license.spdx_id

        description = do_parameter(
            repo.description.enter_message, repo.description.enter_validation
        )
        repo.description.value = do_ask_until_confirmed(
            description,
            repo.description.confirmation_message,
            repo.description.enter_message,
            repo.description.enter_validation,
        )

        if not repo.description.value.endswith("."):
            repo.description.value += "."

        template.pre_confirm(repo)

        if not self.confirm_execution(repo, template):
            return

        self.copy_files(repo, template)

        template.process_license(repo, owner)
        self.process_token_replacements(repo, template)

        # self.process_workspace(repo)
        self.process_repository(repo, template)
        self.process_generator(repo, template)
        
        template.post_execution(repo)

    def process_repository(self, repo: Repository, template: Template):
        print(f"{Fore.BLUE}Initializing repository...")

        remote_url = (
            f"https://github.com/AppalachiaInteractive/{repo.package.value}.git"
        )

        if DRY_RUN:
            print(remote_url)
            return
        try:
            git_repo = git.Repo(repo.directory.value)
        except git.InvalidGitRepositoryError:
            can_create = do_ask(
                f'{Fore.YELLOW}The remote "origin" at {Fore.CYAN}[{remote_url}]{Fore.YELLOW} does not exist.  {Fore.MAGENTA}Should we create it?'
            )

            if not can_create:
                return

            public = do_ask(f"{Fore.MAGENTA}Is this repository public?")

            command = 'sh "{0}" "AppalachiaInteractive/{1}" {2} "{3}"'.format(
                os.path.join(get_home(), command_dir, "repo", "init.sh"),
                repo.package.value,
                "public" if public else "private",
                repo.description.value,
            )

            print(command)
            run(command)

    def process_generator(self, repo: Repository, template: Template):
        if template.generator == "":
            return

        print("Running generator...")

        command = f'{template.generator} && git add . && git commit -m "Adding project scaffolding" && git push'

        print(command)
        run(command)

    def copy_files(self, repo: Repository, template: Template):
        home = os.getenv("HOME")

        all_dirs = common_dirs.copy()
        
        all_dirs.extend([template.template_dir])
        
        for relative_walk_dir in all_dirs:
            print(f"{Fore.CYAN}[COPY FILES]: {Fore.YELLOW}{relative_walk_dir}")

            walk_dir = os.path.join(home, relative_walk_dir)

            for dir_path, dir_names, file_names in os.walk(walk_dir):

                for path_names in [dir_names, file_names]:

                    for pathname in path_names:
                        path_from = os.path.join(dir_path, pathname)
                        path_to = os.path.join(repo.directory.value, pathname)

                        print(
                            f"{Fore.CYAN}[FROM] {path_from} {Fore.WHITE}|{Fore.YELLOW} [TO] {path_to}"
                        )

                        if DRY_RUN:
                            continue

                        if os.path.isdir(path_from):
                            shutil.copytree(path_from, path_to, dirs_exist_ok=True)
                        else:
                            shutil.copy(path_from, path_to)

                break

    def extract_project(self, repo: Repository, template: Template):
        for choice in ChoiceCollections.projects:
            if choice.key in repo.path_parts:
                repo.project.value = choice.name
                repo.projectid.value = choice.key

    def extract_technology(self, repo: Repository, template: Template):
        for choice in ChoiceCollections.technologies:
            if choice.key in repo.path_parts:
                repo.technology.value = choice.name
                repo.technologyid.value = choice.key

    def extract_author(self, repo: Repository, template: Template):
        for choice in ChoiceCollections.authors:
            if choice.key in repo.path_parts:
                repo.author.value = choice.name
                repo.authorid.value = choice.key

    def get_directory(self, repo: Repository, template: Template):
        directory = os.getcwd()

        directory = do_ask_until_confirmed(
            directory,
            repo.directory.confirmation_message,
            repo.directory.enter_message,
            repo.directory.enter_validation,
        )

        os.chdir(directory)
        repo.directory.set(directory)

    def parse_directory(self, repo: Repository, template: Template):
        home = get_home()
        absolute = os.path.abspath(repo.directory.value)
        package = (
            absolute.replace(home, "")
            .replace("Assets", "")
            .replace("Editor", "")
            .replace("Library", "")
            .replace("internal", "")
            .replace("external", "")
            .replace("common", "")
            .replace("experimental", "")
            .replace("\\\\", ".")
            .replace("\\\\", ".")
            .replace("\\", ".")
            .replace("/", ".")
            .replace("..", ".")
            .replace("..", ".")
            .replace("..", ".")
            .strip()
            .strip(".")
            .strip()
        )

        parts = package.split(".")
        for part in parts:
            if part in repo.path_parts:
                continue
            repo.path_parts.append(part)

    def confirm_execution(self, repo: Repository, template: Template):

        repo.token_keys = [prop.key for prop in repo.tokenized_properties]
        repo.token_lookup = {prop.key: prop for prop in repo.tokenized_properties}

        print("\n")
        print(f"{Fore.CYAN}Please confirm your choices:")
        print("----------------------------")
        print("\n")
        for token_key in repo.token_keys:
            prop = repo.token_lookup[token_key]

            print(f"{Fore.WHITE}{prop.display_name}: {Fore.GREEN}[{prop.value}]")

        print("----------------------------")

        return do_ask(f"{Fore.YELLOW}{Style.BRIGHT}Would you like to proceed?")

    def process_token_replacements(self, repo: Repository, template: Template):
        print("Replacing tokens...")

        self.token_keys = [prop.key for prop in repo.tokenized_properties]
        self.token_lookup = {prop.key: prop for prop in repo.tokenized_properties}

        for dir_path, dir_names, file_names in os.walk(repo.directory.value):
            for file_name in file_names:

                token_file_path = os.path.join(dir_path, file_name)

                print(token_file_path)
                if not os.path.isfile(token_file_path):
                    print(f"Missing {token_file_path}")
                    continue

                print(f"Replacing tokens for [{token_file_path}]...")

                if DRY_RUN:
                    continue

                new_file_name = file_name
                new_file_path = token_file_path

                for token in repo.tokenized_properties:
                    new_file_name = token.replace(new_file_name)

                if new_file_name != file_name:
                    new_file_path = os.path.join(dir_path, new_file_name)
                    print(f"Moving from [{file_name}] to [{new_file_name}]...")
                    shutil.move(token_file_path, new_file_path)

                lines = []
                try:
                    with open(new_file_path, mode="r", encoding="utf-8") as fs:
                        for line in fs:
                            for token in repo.tokenized_properties:
                                line = token.replace(line)

                            lines.append(line)

                    with open(new_file_path, mode="w") as fs:
                        fs.write("".join(lines))
                except UnicodeError as ue:
                    pass

        print("Token replacement completed.")

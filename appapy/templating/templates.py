import os
import shutil
from abc import ABC
from typing import Dict, List

import git
from appapy.common import shell
from appapy.common.cli import *
from appapy.common.constants import *
from appapy.common.env import get_home
from appapy.templating.constants import *
from appapy.templating.owners import *
from appapy.templating.repositories import Repository
from appapy.templating.utils import *
from colorama import Back, Fore, Style


class Template(ABC):
    def __init__(self, key: str, name: str, template_dir: str, generator: str = ""):
        self.key = key
        self.name = name
        self.template_dir = template_dir
        self.generator = generator

    def process(self, repo: Repository, owner: Owner):

        parts = repo.package.value.split(".")

        owner.set_license(repo)
        owner.extract_metadata(repo, parts)

        description = do_parameter("Enter a package description", no_validation)
        repo.description.value = do_ask_until_confirmed(
            description,
            "Is this the package description? [{0}]",
            "Enter a package description",
            no_validation,
        )

        if not self.confirm_execution(repo):
            return

        self.copy_files(repo)
        self.process_license(repo, owner)

        repo.process_token_replacements()

        #self.process_workspace(repo)
        self.process_repository(repo)
        self.process_generator(repo)

    def confirm_execution(self, repo: Repository):
        print("\n")
        print(f"{Fore.CYAN}Please confirm your choices:")
        print("----------------------------")
        print("\n")
        for token_key in repo.token_keys:
            prop = repo.token_lookup[token_key]

            print(f"{Fore.WHITE}{prop.display_name}: {Fore.GREEN}[{prop.value}]")

        print("----------------------------")

        return do_ask(f"{Fore.YELLOW}{Style.BRIGHT}Would you like to proceed?")

    def process_license(self, repo: Repository, owner: Owner):
        license_type = repo.license.value

        if license_type == "NONE":
            return

        print(f"{Fore.CYAN}Updating license to use {Fore.YELLOW}{0}".format(license_type))

        license_file = os.path.join(
            get_home(), license_dir, owner.key, f"LICENSE_{license_type}.md"
        )

        if DRY_RUN:
            print(license_file)
            return

        shutil.copy(license_file, "LICENSE.md")

    # def process_workspace(self, repo: Repository):
    #     print(f"{Fore.BLUE}Renaming workspace...")
    #     workspace_file = "workspace.code-workspace"
    #     target_file = workspace_file.replace(
    #         "workspace.", "{0}.".format(repo.package.value)
    #     )

    #     rename_file(workspace_file, target_file, True)

    def process_repository(self, repo: Repository):
        print(f"{Fore.BLUE}Initializing repository...")

        remote_url = (
            f"https://github.com/AppalachiaInteractive/{repo.package.value}.git"
        )

        if DRY_RUN:
            print(remote_url)
            return
        try:
            git_repo = git.Repo(repo.directory)
        except git.InvalidGitRepositoryError:
            can_create = do_ask(
                f'{Fore.YELLOW}The remote "origin" at {Fore.CYAN}[{remote_url}]{Fore.YELLOW} does not exist.  {Fore.MAGENTA}Should we create it?'
            )

            if not can_create:
                return

            public = do_ask(f"{Fore.MAGENTA}Is this repository public?")

            command = 'sh {0} "AppalachiaInteractive/{1}" {2} "{3}"'.format(
                os.path.join(get_home(), command_dir, "repo", "init.sh"),
                repo.package.value,
                "public" if public else "private",
                repo.description.value,
            )

            print(command)
            shell.run(command)

    def process_generator(self, repo: Repository):
        if self.generator == "":
            return

        print("Running generator...")

        command = f'{self.generator} && git add . && git commit -m "Adding project scaffolding" && git push'

        print(command)
        shell.run(command)

    def copy_files(self, repo: Repository):
        home = os.getenv("HOME")

        for relative_walk_dir in [self.template_dir, common_dir]:
            print(f"{Fore.CYAN}[COPY FILES]: {Fore.YELLOW}{relative_walk_dir}")

            walk_dir = os.path.join(home, relative_walk_dir)

            for dir_path, dir_names, file_names in os.walk(walk_dir):

                for path_names in [dir_names, file_names]:

                    for pathname in path_names:
                        path_from = os.path.join(dir_path, pathname)
                        path_to = os.path.join(repo.directory, pathname)

                        print(f"{Fore.CYAN}[FROM] {path_from} {Fore.WHITE}|{Fore.YELLOW} [TO] {path_to}")

                        if DRY_RUN:
                            continue

                        if os.path.isdir(path_from):
                            shutil.copytree(path_from, path_to, dirs_exist_ok=True)
                        else:
                            shutil.copy(path_from, path_to)

                break


class TemplateAPPA(Template):
    def __init__(self):
        super(TemplateAPPA, self).__init__(
            "APPA", "General", f"{root_dir}/appa/templates/com.appalachia"
        )


class TemplateUNITY(Template):
    def __init__(self):
        super(TemplateUNITY, self).__init__(
            "UNITY",
            "Unity Project",
            f"{root_dir}/appa/templates/com.appalachia.unity3d",
        )


class TemplateUNITYPKG(Template):
    def __init__(self):
        super(TemplateUNITYPKG, self).__init__(
            "UNITYPKG",
            "Unity Package",
            f"{root_dir}/appa/templates/com.appalachia.unity3d.package",
        )


class TemplateVSCODE(Template):
    def __init__(self):
        super(TemplateVSCODE, self).__init__(
            "VSCODE",
            "VS Code Extension",
            f"{root_dir}/appa/templates/com.appalachia.vscode",
            "yo code",
        )


class TemplateNODE(Template):
    def __init__(self):
        super(TemplateNODE, self).__init__(
            "NODE",
            "nodeJS Package",
            f"{root_dir}/appa/templates/com.appalachia.node",
            "yo node",
        )


class TemplateCS(Template):
    def __init__(self):
        super(TemplateCS, self).__init__(
            "CS",
            "C# Project",
            f"{root_dir}/appa/templates/com.appalachia.cs",
            "dotnet new classlib -f netcoreapp3.1",
        )


class TemplatePY(Template):
    def __init__(self):
        super(TemplatePY, self).__init__(
            "PY",
            "Python Module",
            f"{root_dir}/appa/templates/com.appalachia.py",
            "yo py",
        )


templates: List[Template] = [
    TemplateAPPA(),
    TemplateUNITY(),
    TemplateUNITYPKG(),
    TemplateVSCODE(),
    TemplateNODE(),
    TemplateCS(),
    TemplatePY(),
]

templates_lookup = {template.key: template for template in templates}

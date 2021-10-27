import os
import shutil
from abc import ABC
from typing import Dict, List

from appapy.common import shell
from appapy.common.cli import *
from appapy.common.constants import *
from appapy.common.env import get_home
from appapy.templating.args import Args
from appapy.templating.choices import ChoiceCollections
from appapy.templating.constants import *
from appapy.templating.owner import *
from appapy.templating.repository import Repository
from appapy.templating.utils import *
from colorama import Back, Fore, Style
import git


class Template(ABC):
    def __init__(self, key: str, name: str, template_dir: str, generator: str = ""):
        self.key = key
        self.name = name
        self.template_dir = template_dir
        self.generator = generator

    def pre_confirm(self, repo: Repository, args: Args) -> None:
        pass

    def extract_library(self, repo: Repository):
        library_parts = repo.path_parts.copy()
        replace_parts = [
            "com",
            "appalachia",
            repo.projectid.value,
            repo.technology.value,
            repo.technologyid.value,
        ]

        for id, part in reversed(list(enumerate(library_parts))):
            if [e.lower() for e in replace_parts if e == part]:
                library_parts.pop(id)

        repo.thirdparty = False

        for id, part in enumerate(library_parts):
            if part == "appa":
                library_parts[id] = "appalachia"
            if part == "third-party":
                repo.thirdparty = True

        initial_case = ".".join(library_parts)
        title_case = initial_case.title()
        repo.library.value = initial_case

        for index in range(len(title_case)):
            if repo.library.value[index].isupper() or title_case[index].isupper() or initial_case[index].isupper():
                repo.library.value = repo.library.value[:index] + title_case[index].upper() + repo.library.value[index + 1:]

        repo.csnamespace.value = self.fix_third_party(repo.library.value)

    def fix_third_party(self, value):
        return value.replace('Appalachia.Third-Party.', '')

    def generate_display_name(self, repo: Repository):
        display = self.fix_third_party(repo.library.value)
        no_project = repo.projectid.value == ""

        basic = f"{display} for {repo.technology.value}"
        basic_project = f"{basic} ({repo.project.value})"
        named = f"{repo.technology.value} Assets by {display}"
        named_project = f"{named} ({repo.project.value})"
        unity_named = f"Packages by Unity Technologies"
        unity_named_project = f"{named} ({repo.project.value})"

        if repo.ownerid == "appa":            
            if no_project:
                repo.display.value = basic
            else:
                repo.display.value = basic_project
        elif repo.ownerid.value == "unity":
            if no_project:
                repo.display.value = named
            else:
                repo.display.value = named_project
        elif repo.ownerid.value == "assets":
            if no_project:
                repo.display.value = named
            else:
                repo.display.value = named_project
        else:
            if no_project:
                repo.display.value = basic
            else:
                repo.display.value = basic_project

    def get_display_name(self, repo: Repository, args: Args):
        self.generate_display_name(repo)

        repo.display.value = do_ask_until_confirmed(
            repo.display.value,
            repo.display.confirmation_message,
            repo.display.enter_message,
            repo.display.enter_validation,
            args.autodisplayname
        )

    def get_package(self, repo: Repository, args: Args):

        package = ".".join([p for p in repo.path_parts if p != "appa"]).lower()

        package = do_ask_until_confirmed(
            package,
            repo.package.confirmation_message,
            repo.package.enter_message,
            repo.package.enter_validation,
            args.autopackage
        )

        if len(package) < 8:
            raise ValueError(package)

        repo.package.set(package)

    def process_license(self, repo: Repository, owner: Owner):
        license_type = repo.license.value

        if license_type == "NONE":
            return

        print(
            f"{Fore.CYAN}Updating license to use {Fore.YELLOW}{license_type}"
        )

        license_file = os.path.join(
            get_home(), license_dir, owner.key, f"LICENSE_{license_type}"
        )

        if DRY_RUN:
            print(license_file)
            return

        shutil.copy(license_file, "LICENSE")

    def post_execution(self, repo: Repository):
        pass

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

    def pre_confirm(self, repo: Repository, args: Args) -> None:
        repo.tokenized_properties.append(repo.csnamespace)

        repo.csnamespace.value = do_ask_until_confirmed(
            repo.csnamespace.value,
            repo.csnamespace.confirmation_message,
            repo.csnamespace.enter_message,
            repo.csnamespace.enter_validation,
            args.autonamespace
        )

    def post_execution(self, repo: Repository):        
        print(f"{Fore.YELLOW}-----------------------")
        print(f"{Fore.YELLOW}| Remember to refresh Unity Asset Database.")
        print(f"{Fore.YELLOW}-----------------------")


class TemplateUNITYPKGFRK(Template):
    def __init__(self):
        super(TemplateUNITYPKGFRK, self).__init__(
            "UNITYPKGFRK",
            "Unity Package (Forked)",
            f"{root_dir}/appa/templates/com.appalachia.unity3d.package.fork",
        )

    def process_license(self, repo: Repository, owner: Owner):
        license_type = repo.license.value
        license = ChoiceCollections.license_lookup[license_type]

        if repo.license.value == "NONE":
            return
        if repo.license.value != "DUAL":
            super(TemplateUNITYPKGFRK, self).process_license(repo, owner)
            return

        props = [repo.license1, repo.license2, repo.commit]

        for prop in props:
            repo.tokenized_properties.append(prop)
            repo.token_keys.append(prop.key)
            repo.token_lookup[prop.key] = prop

        print(
            f"{Fore.CYAN}Updating license to use {Fore.YELLOW}{0}".format(
                repo.license.value
            )
        )

        repo.license.value = license.key
        repo.licenseid.value = license.spdx_id

        license_index = do_selection_until_confirmed(
            repo.license1.confirmation_message,
            owner.license_options,
            repo.license1.selection_message,
        )

        repo.license1.value = owner.license_options[license_index].key

        license_index = do_selection_until_confirmed(
            repo.license2.confirmation_message,
            owner.license_options,
            repo.license2.selection_message,
        )
        repo.license2.value = owner.license_options[license_index].key

        repo.commit.value = shell.run_and_read("git rev-parse HEAD")
        repo.commit.value = do_ask_until_confirmed(
            repo.commit.value,
            repo.commit.confirmation_message,
            repo.commit.enter_message,
            commit_hash,
        )

        license_file = os.path.join(
            get_home(), license_dir, owner.key, f"LICENSE_{repo.license.value}"
        )
        license_file1 = os.path.join(
            get_home(), license_dir, owner.key, f"LICENSE_{repo.license1.value}"
        )
        license_file2 = os.path.join(
            get_home(), license_dir, "appa", f"LICENSE_{repo.license2.value}"
        )

        if DRY_RUN:
            print(license_file)
            return

        shutil.copy(license_file, "LICENSE")
        shutil.copy(license_file1, "LICENSE.ORIGINAL.md")
        shutil.copy(license_file2, "LICENSE.UPDATED.md")


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
    TemplateUNITYPKG(),
    TemplateUNITYPKGFRK(),
    TemplatePY(),
    TemplateNODE(),
    TemplateCS(),
    TemplateVSCODE(),
    TemplateUNITY(),
    TemplateAPPA(),
]

templates_lookup = {template.key: template for template in templates}

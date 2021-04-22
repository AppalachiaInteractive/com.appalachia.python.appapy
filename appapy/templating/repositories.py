import os

from ..common.cli import *
from ..common.env import get_home
from .constants import *
from .tokens import TokenizedProperty
from .utils import *


class Repository:
    def __init__(self):
        self.directory = ""

        self.package = TokenizedProperty(
            "package", "Package", "Enter the name of the package"
        )
        self.project = TokenizedProperty(
            "project", "Project", "Enter the name of the project"
        )
        self.display = TokenizedProperty(
            "display", "Display", "Enter the display name of the package"
        )
        self.version = TokenizedProperty(
            "version", "Version", "Enter the intitial ersion of the package"
        )
        self.description = TokenizedProperty(
            "description", "Description", "Enter a description of the package"
        )
        self.license = TokenizedProperty(
            "license", "License", "Enter the license of the package"
        )
        self.licenseid = TokenizedProperty(
            "licenseid", "License ID", "Enter the license identifier of the package"
        )
        self.author = TokenizedProperty(
            "author", "Author", "Enter the author of the package"
        )

        self.tokenized_properties = [
            self.package,
            self.project,
            self.display,
            self.version,
            self.description,
            self.license,
            self.licenseid,
            self.author,
        ]

        self.token_keys = [prop.key for prop in self.tokenized_properties]
        self.token_lookup = {prop.key: prop for prop in self.tokenized_properties}

    def get_directory(self):
        directory = os.getcwd()

        directory = do_ask_until_confirmed(
            directory,
            "Is {0} the intended directory?",
            "Enter the directory (starting with ~/)",
            os.path.isdir,
        )

        os.chdir(directory)
        self.directory = directory

    def get_package(self):
        home = get_home()
        absolute = os.path.abspath(self.directory)
        package = (
            absolute.replace(home, "")
            .replace("Assets", "")
            .replace("internal", "")
            .replace("experimental", "")
            .replace("\\\\", ".")
            .replace("\\\\", ".")
            .replace("\\", ".")
            .replace("/", ".")
            .replace("..", ".")
            .replace("..", ".")
            .replace("..", ".")
            .strip(".")
        )

        package = do_ask_until_confirmed(
            package,
            "Is this the correct package?  {0}",
            "Enter the package name",
            no_validation,
        )

        if len(package) < 8:
            raise ValueError(package)

        self.package.set(package)

    def process_token_replacements(self):
        print("Replacing tokens...")

        for token_file_name in token_files:

            token_file_path = os.path.join(self.directory, token_file_name)
            
            print(token_file_path)
            if not os.path.isfile(token_file_path):
                print(f"Missing {token_file_path}")
                continue

            print(f"Replacing tokens for [{token_file_path}]...")
        
            if DRY_RUN:
                continue
            
            lines = []
            with open(token_file_path, mode="r",encoding='utf-8') as fs:
                for line in fs:
                    for token in self.tokenized_properties:
                        line = token.replace(line)

                    lines.append(line)

                if DRY_RUN:
                    print(lines)
                    continue

            with open(token_file_path, mode="w") as fs:
                fs.write("".join(lines))

        print("Token replacement completed.")

import os
import shutil

from appapy.common.cli import *
from appapy.common.env import get_home
from appapy.templating.constants import *
from appapy.templating.tokens import TokenizedProperty
from appapy.templating.utils import *


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
        self.license1 = TokenizedProperty(
            "license1", "License 1", "Enter the original license of the package"
        )
        self.license2 = TokenizedProperty(
            "license2", "License 2", "Enter the update license of the package"
        )
        self.commit = TokenizedProperty(
            "commit", "License Transition Commit Hash", "Enter the commit hash that indicates the license change"
        )
        self.licenseid = TokenizedProperty(
            "licenseid", "License ID", "Enter the license identifier of the package"
        )
        self.author = TokenizedProperty(
            "author", "Author", "Enter the author of the package"
        )
        self.year = TokenizedProperty(
            "year", "Copyright Year", "Enter the copyright year of the package"
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
            self.year
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
            .strip().strip(".").strip()
        )

        package = do_ask_until_confirmed(
            package,
            "Is this the correct package?  {0}",
            "Enter the package name",
            package_validation,
        )                

        if len(package) < 8:
            raise ValueError(package)

        self.package.set(package)
        
    def process_token_replacements(self):
        print("Replacing tokens...")
        
        for dir_path, dir_names, file_names in os.walk(self.directory):
            for file_name in file_names:          
                
                token_file_path = os.path.join(dir_path, file_name)
                    
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

                with open(token_file_path, mode="w") as fs:
                    fs.write("".join(lines))
                
                new_file_name = file_name
                for token in self.tokenized_properties:
                    new_file_name = token.replace(new_file_name)
                    
                if new_file_name != file_name:
                    new_file_path = os.path.join(dir_path, new_file_name)
                    print(f"Moving from [{file_name}] to [{new_file_name}]...")
                    shutil.move(token_file_path, new_file_path)

        print("Token replacement completed.")

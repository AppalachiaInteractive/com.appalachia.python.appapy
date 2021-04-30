import os
import shutil

from appapy.common.cli import *
from appapy.common.env import get_home
from appapy.templating.constants import *
from appapy.templating.tokens import TokenizedProperty
from appapy.templating.utils import *


class Repository:
    def __init__(self):
        self.directory = TokenizedProperty(
            "directory", "Directory", "Enter the directory (starting with ~/)", "Is {0} the intended directory??  {0}", os.path.isdir
        )
        self.package = TokenizedProperty(
            "package", "Package", "Enter the package name", "Is this the correct package?  {0}", package_validation
        )
        self.project = TokenizedProperty(
            "project", "Project", "Enter the name of the project",  "Is this the correct project name?  {0}", no_validation
        )
        self.display = TokenizedProperty(
            "display", "Display", "Enter the display name of the package", "Is this the package display name? [{0}]",no_validation
        )
        self.version = TokenizedProperty(
            "version", "Version", "Enter the initial version of the package", "Is {0} the intended initial version?", no_validation
        )
        self.description = TokenizedProperty(
            "description", "Description", "Enter a description of the package", "Is this the package description? [{0}]", no_validation
        )
        self.license = TokenizedProperty(
            "license", "License", "Enter the license of the package", "Is {0} the intended license?", no_validation
        )
        self.license1 = TokenizedProperty(
            "license1", "License 1", "Enter the original license of the package", "Is {0} the intended original license?", no_validation
        )
        self.license2 = TokenizedProperty(
            "license2", "License 2", "Enter the updated license of the package", "Is {0} the intended updated license?", no_validation
        )
        self.csnamespace = TokenizedProperty(
            "csnamespace", "C# Namespace", "Enter the C# Root Namespace of the package", "Is this the correct C# Root Namespace? {0}", no_validation
        )
        self.commit = TokenizedProperty(
            "commit", "License Transition Commit Hash", "Enter the commit hash that indicates the license change", "Is this the correct C# Root Namespace? {0}", no_validation
        )
        self.licenseid = TokenizedProperty(
            "licenseid", "License ID", "Enter the license identifier of the package", "Is {0} the intended license?", no_validation
        )
        self.author = TokenizedProperty(
            "author", "Author", "Enter the author of the package", "Is this the package author? [{0}]", no_validation
        )
        self.year = TokenizedProperty(
            "year", "Copyright Year", "Enter the copyright year of the package", "Is {0} the intended year?", no_validation
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
            self.directory.confirmation_message,
            self.directory.enter_message,
            self.directory.enter_validation
        )

        os.chdir(directory)
        self.directory.set(directory)

    def get_package(self):
        home = get_home()
        absolute = os.path.abspath(self.directory.value)
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
            self.package.confirmation_message,
            self.package.enter_message,
            self.package.enter_validation,
        )

        if len(package) < 8:
            raise ValueError(package)

        self.package.set(package)
        
    def process_token_replacements(self):
        print("Replacing tokens...")
        
        for dir_path, dir_names, file_names in os.walk(self.directory.value):
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

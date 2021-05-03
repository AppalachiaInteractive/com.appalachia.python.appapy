import os
from typing import Dict

from appapy.common.cli import *
from appapy.templating.constants import *
from appapy.templating.tokenizedproperty import TokenizedProperty
from appapy.templating.utils import *


class Repository:
    def __init__(self):

        self.owner = TokenizedProperty("owner", "Owner", no_validation)
        self.ownerid = TokenizedProperty("ownerid", "Owner ID", no_validation)
        self.directory = TokenizedProperty("directory", "Directory Path", os.path.isdir)
        self.package = TokenizedProperty("package", "Package Name", package_validation)
        self.library = TokenizedProperty("library", "Library Name", no_validation)
        self.project = TokenizedProperty("project", "Project Name", no_validation)
        self.projectid = TokenizedProperty("projectid", "Project ID", no_validation)
        self.display = TokenizedProperty("display", "Display Name", no_validation)
        self.version = TokenizedProperty("version", "Current Version", no_validation)
        self.description = TokenizedProperty(
            "description", "Description", no_validation
        )
        self.license = TokenizedProperty("license", "License", no_validation)
        self.licenseid = TokenizedProperty("licenseid", "License ID", no_validation)
        self.author = TokenizedProperty("author", "Author", no_validation)
        self.authorid = TokenizedProperty("authorid", "Author ID", no_validation)
        self.technology = TokenizedProperty("technology", "Technology", no_validation)
        self.technologyid = TokenizedProperty(
            "technologyid", "Technology ID", no_validation
        )
        self.year = TokenizedProperty("year", "Copyright Year", no_validation)
        self.commit = TokenizedProperty(
            "commit", "License Transition Commit Hash", no_validation
        )
        self.license1 = TokenizedProperty("license1", "License 1", no_validation)
        self.license2 = TokenizedProperty("license2", "License 2", no_validation)
        self.csnamespace = TokenizedProperty(
            "csnamespace", "C# Root Namespace", no_validation
        )

        self.tokenized_properties = [
            self.owner,
            self.package,
            self.library,
            self.project,
            self.projectid,
            self.display,
            self.version,
            self.description,
            self.license,
            self.licenseid,
            self.author,
            self.authorid,
            self.technology,
            self.technologyid,
            self.year,
        ]

        self.token_keys: List[TokenizedProperty] = [
            prop.key for prop in self.tokenized_properties
        ]
        self.token_lookup: Dict[str, TokenizedProperty] = {
            prop.key: prop for prop in self.tokenized_properties
        }
        self.path_parts: List[str] = []

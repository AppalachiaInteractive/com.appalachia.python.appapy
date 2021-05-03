import json
import os
from typing import Callable, Dict, List


class ChoiceOptions:
    def __init__(self, key: str, name: str, notes: str):
        self.key: str = key
        self.name: str = name
        self.notes: str = notes


class Author(ChoiceOptions):
    def __init__(self, key: str, name: str, notes: str):
        super(Author, self).__init__(key, name, notes)


class License(ChoiceOptions):
    def __init__(self, key: str, spdx_id: str, name: str, notes: str):
        super(License, self).__init__(key, name, notes)
        self.spdx_id = spdx_id


class Project(ChoiceOptions):
    def __init__(self, key: str, name: str, notes: str):
        super(Project, self).__init__(key, name, notes)


class Technology(ChoiceOptions):
    def __init__(self, key: str, name: str, notes: str):
        super(Technology, self).__init__(key, name, notes)


class ChoiceCollections:
    directory = os.path.abspath(os.path.dirname(__file__))

    authors_path = os.path.join(directory, "json", "authors.json")
    licenses_path = os.path.join(directory, "json", "licenses.json")
    projects_path = os.path.join(directory, "json", "projects.json")
    technologies_path = os.path.join(directory, "json", "technologies.json")
    
    authors_content = open(authors_path).read()
    licenses_content = open(licenses_path).read()
    projects_content = open(projects_path).read()
    technologies_content = open(technologies_path).read()
    
    authors_json = json.loads(authors_content)
    licenses_json = json.loads(licenses_content)
    projects_json = json.loads(projects_content)
    technologies_json = json.loads(technologies_content)

    authors: List[Author] = [Author(**author) for author in authors_json]
    licenses: List[License] = [License(**license) for license in licenses_json]
    projects: List[Project] = [Project(**project) for project in projects_json]
    technologies: List[Technology] = [Technology(**technology) for technology in technologies_json]
        
    author_lookup = {author.key : author for author in authors}
    license_lookup = {license.key : license for license in licenses}
    project_lookup = {project.key : project for project in projects}
    technology_lookup = {
        technology.key : technology for technology in technologies
    }

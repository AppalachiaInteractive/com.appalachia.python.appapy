from appapy.common.cli import *
from appapy.templating.constants import *
from appapy.templating.owners import owners
from appapy.templating.repositories import Repository
from appapy.templating.templates import templates
from appapy.templating.utils import *


def execute(args : List[str]):
    print("Enter x to exit.")
    repo = Repository()
    repo.version.set(default_version)
    repo.get_directory()
    repo.get_package()

    owner_index = do_selection(
        [owner.name for owner in owners], "Select the package owner"
    )
    owner = owners[owner_index]

    template_index = do_selection(
        [template.name for template in templates], "Select the package template"
    )
    template = templates[template_index]

    template.process(repo, owner)


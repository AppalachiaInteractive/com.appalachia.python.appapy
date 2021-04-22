from ..common.cli import *
from .constants import *
from .owners import owners
from .repositories import Repository
from .templates import templates
from .utils import *


def execute():

    repo = Repository()
    repo.version.set(default_version)
    repo.get_directory()
    repo.get_package()

    owner_index = do_selection([owner.name for owner in owners], "Select the package owner")
    owner = owners[owner_index]
    
    template_index = do_selection(
        [template.name for template in templates], "Select the package template"
    )
    template = templates[template_index]

    template.process(repo, owner)

    return


print("Enter x to exit.")
execute()

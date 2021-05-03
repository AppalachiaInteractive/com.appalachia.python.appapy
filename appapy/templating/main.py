from appapy.common.cli import *
from appapy.templating.constants import *
from appapy.templating.repository import Repository
from appapy.templating.template import templates
from appapy.templating.templateprocessor import TemplateProcessor
from appapy.templating.utils import *


def execute(args: List[str]):
    print("Enter x to exit.")
    processor = TemplateProcessor()
    repo = Repository()
    repo.version.set(default_version)

    template_index = do_selection(
        [template.name for template in templates], "Select the package template"
    )
    template = templates[template_index]

    processor.process(repo, template)

    # shell.run("sh direnv allow")

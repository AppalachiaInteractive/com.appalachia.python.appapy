from appapy.common.cli import do_selection
from appapy.common.exceptions import QuitError, RestartError
from appapy.templating.args import Args
from appapy.templating.constants import default_version
from appapy.templating.repository import Repository
from appapy.templating.template import templates
from appapy.templating.templateprocessor import TemplateProcessor
from appapy.templating.utils import *
import sys


def execute(cliArguments: List[str]):
    print("Enter `x` or `q` to exit.")
    print("Enter `r` to restart.")

    try:

        args = Args(cliArguments)
        processor = TemplateProcessor()
        repo = Repository()
        repo.version.set(default_version)
  
        template_index = do_selection(
            [template.name for template in templates],
            "Select the package template",
            args.template_id,
        )

        template = templates[template_index]

        processor.process(repo, template, args)
    except QuitError:
        print("Quitting!")
        sys.exit(1)

    except RestartError:
        print("Restarting...")
        execute(cliArguments)

    # shell.run("sh direnv allow")

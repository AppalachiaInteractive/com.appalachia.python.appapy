from appapy.templating.constants import default_version
from appapy.common.cli import do_selection
from appapy.common.exceptions import QuitError, RestartError
from appapy.templating.repository import Repository
from appapy.templating.template import templates
from appapy.templating.templateprocessor import TemplateProcessor
from appapy.templating.utils import *
import sys

def execute(args: List[str]):
    print("Enter `x` or `q` to exit.")
    print("Enter `r` to restart.")
    
    try:
            
        processor = TemplateProcessor()
        repo = Repository()
        repo.version.set(default_version)

        template_index = do_selection(
            [template.name for template in templates], "Select the package template"
        )
        template = templates[template_index]

        processor.process(repo, template)
    except QuitError:
        print('Quitting!')
        sys.exit(1)
    
    except RestartError:
        print('Restarting...')
        execute(args)
        

    # shell.run("sh direnv allow")

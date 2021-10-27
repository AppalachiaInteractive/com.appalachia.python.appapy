from typing import Dict

from appapy.common.cli import *
from appapy.templating.constants import *
from appapy.templating.tokenizedproperty import TokenizedProperty
from appapy.templating.utils import *

class Args:
    def __init__(self, args: List[str]):

        self.template_id: int = None
        self.autodirectory: bool = None
        self.owner_id: int = None
        self.autoauthor: bool = None
        self.autoproject: bool = None
        self.autotechnology: bool = None
        self.autodisplayname: bool = None
        self.autopackage: bool = None
        self.autonamespace: bool = None
        self.createrepo: bool = None
        self.repopublic: bool = None

        hasAny = False

        if len(args) > 0:
            hasAny = True
            self.template_id = int(args[0].strip())
        if len(args) > 1:
            self.autodirectory = parse_bool(args[1].strip())
        if len(args) > 2:
            self.owner_id = int(args[2].strip())
        if len(args) > 3:
            self.autoauthor = parse_bool(args[3].strip())
        if len(args) > 4:
            self.autoproject = parse_bool(args[4].strip())
        if len(args) > 5:
            self.autotechnology = parse_bool(args[5].strip())
        if len(args) > 6:
            self.autodisplayname = parse_bool(args[6].strip())
        if len(args) > 7:
            self.autopackage = parse_bool(args[7].strip())
        if len(args) > 8:
            self.autonamespace = parse_bool(args[8].strip())
        if len(args) > 9:
            self.createrepo = parse_bool(args[9].strip())
        if len(args) > 10:
            self.repopublic = parse_bool(args[10].strip())

        if hasAny:
            demarcate("AUTO ARGS")
            highlight("template_id", self.template_id)
            highlight("autodirectory", self.autodirectory)
            highlight("owner_id", self.owner_id)
            highlight("autoauthor", self.autoauthor)
            highlight("autoproject", self.autoproject)
            highlight("autotechnology", self.autotechnology)
            highlight("autodisplayname", self.autodisplayname)
            highlight("autopackage", self.autopackage)
            highlight("autonamespace", self.autonamespace)
            highlight("createrepo", self.createrepo)
            highlight("repopublic", self.repopublic)
            note("----------------------------")

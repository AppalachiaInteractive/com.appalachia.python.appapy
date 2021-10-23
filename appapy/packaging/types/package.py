import os
from abc import ABC
from typing import List, Tuple

from appapy.common import shell
from appapy.common.cli import demarcate, note
from appapy.common.env import get_home


class Package(ABC):
    def __init__(self, directory: str, bump: str):
        self.directory = directory
        self.bump = bump

    def preversion(self):
        demarcate("[PREVERSION]")
        shell.run("git fetch -q -p && git pull -q && git fetch -q --tags -f && git pull -q --tags && git push -q --tags")

    def version(self):
        demarcate("[VERSION]")

        self.changelog()
        self.releaselog()

        mods = "modifications.sh"
        if os.path.isfile(mods):
            shell.run(f"bash {mods}")

        shell.run(f"git add .")
        self.after_version()
        
    def after_version(self):
        pass

    def changelog(self):
        home = get_home()
        shell.run(f"bash {home}/com.appalachia/appa/appa.sh docs changelog")

    def releaselog(self):
        home = get_home()
        shell.run(f"bash {home}/com.appalachia/appa/appa.sh docs releaselog")

    def postversion(self):
        demarcate("[POSTVERSION]")

    def prepack(self):
        demarcate("[PREPACK]")

    def package(self):
        demarcate("[PACKAGE]")

    def postpack(self):
        demarcate("[POSTPACK]")

    def vscode_prepublish(self):
        demarcate("[VSCODE-PREPUBLISH]")

    def prepublishOnly(self):
        demarcate("[PREPUBLISH-ONLY]")

    def publish(self):
        demarcate("[PUBLISH]")

    def postpublish(self):
        demarcate("[POSTPUBLISH]")

    def lint(self):
        demarcate("[LINT]")

    def compile(self):
        demarcate("[COMPILE]")

    def pretest(self):
        demarcate("[PRETEST]")

    def test(self):
        demarcate("[TEST]")

    def posttest(self):
        demarcate("[POSTTEST]")

    def execute_version(self) -> Tuple[str, List[str]]:
        return

    def execute_package(self) -> Tuple[str, List[str]]:
        return ("", [])

    def release(self, package_path: str):
        return

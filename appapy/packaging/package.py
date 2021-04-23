import os
from abc import ABC
from typing import List, Tuple

from appapy.common.env import get_home

from appapy.common import shell
from appapy.common.cli import demarcate, note


class Package(ABC):
    def __init__(self, directory : str, bump : str):
        self.directory = directory
        self.bump = bump

    def preversion(self):
        demarcate("[PREVERSION]")

        shell.run("git fetch -p && git pull --tags && git add .")

    def version(self):
        demarcate("[VERSION]")

        home = get_home()
        shell.run(f"bash {home}/com.appalachia/appa/appa.sh docs releaselog && git add .")

    def postversion(self):
        demarcate("[POSTVERSION]")

        home = get_home()
        shell.run(f"bash {home}/com.appalachia/appa/appa.sh docs changelog")
        mods = "modifications.sh"
        if os.path.isfile(mods):
            shell.run(f"bash {mods}")

        shell.run("git push && git push --tags && git add .")

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

    def execute(self) -> Tuple[str, List[str]]:
        return ('', [])
    
    def release(self, package_path : str):
        pass
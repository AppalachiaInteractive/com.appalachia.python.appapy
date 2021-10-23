import os
import shutil
from typing import List, Tuple

from appapy.common import shell
from appapy.common.cli import demarcate, note
from appapy.common.constants import *
from appapy.packaging.types.npm import NPMPackage


class VSCode(NPMPackage):
    def __init__(self, directory: str, bump: str):
        super(VSCode, self).__init__(directory, bump)

    def vscode_prepublish(self):
        demarcate("[VSCODE-PREPUBLISH]")
        self.package()

    def package(self):
        demarcate("[PACKAGE]")
                
        shell.run('webpack --mode production --devtool hidden-source-map')

    def get_vsix_name(self) -> str:
        name = self.json["name"]
        version = self.json["version"]
        return f"{name}-{version}.vsix"
        
    def lint(self):
        demarcate("[LINT]")
        shell.run("eslint src --ext ts")

    def compile(self):
        demarcate("[COMPILE]")
        shell.run("webpack")

    def pretest(self):
        demarcate("[PRETEST]")
        self.test_compile()
        self.lint()
        
    def test(self):
        demarcate("[TEST]")
        shell.run("./out/test/runTest.js")

    def test_compile(self):
        demarcate("[TEST-COMPILE]")
        shell.run("tsc -p ./")

        
    def execute_package(self) -> Tuple[str, List[str]]:
        cwd = os.getcwd()
        dist_folder= os.path.join(cwd, output_folder)
        
        vsix=self.get_vsix_name()        
        vsix_path = os.path.join(dist_folder, vsix)     
        ext_path = os.path.join(cwd, 'extension.vsix')
           
        shell.run(f"vsce package -o {vsix_path}")
        
        shutil.copy(vsix_path, ext_path)
        
        os.chdir(dist_folder)
        shell.run(f'npm pack ..')
        os.chdir(cwd)

        package_path = self.get_package_path()
        return package_path, [vsix_path]

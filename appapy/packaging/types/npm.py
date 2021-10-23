import os
import shutil
from typing import List, Tuple

from appapy.common import shell
from appapy.common.cli import demarcate, note
from appapy.common.constants import *
from appapy.common.env import get_home
from appapy.packaging.types.package import Package
from pynpm.package import NPMPackage as npmpackage


class NPMPackage(Package):
    def __init__(self, directory: str, bump: str):
        super(NPMPackage, self).__init__(directory, bump)
        self.npm_package: npmpackage = None
        self.json: None

        self.refresh_package()

    def refresh_package(self):
        self.npm_package = npmpackage(os.path.join(self.directory, "package.json"))
        self.json = self.npm_package.package_json

    def releaselog(self):
        home = get_home()
        self.refresh_package()        
        version = self.json["version"]
        shell.run(f"bash {home}/com.appalachia/appa/appa.sh docs releaselog {version}")

        
    def execute_version(self) -> None:    
        if self.bump == 'existing':         
            self.preversion()

            self.refresh_package()        
            version = self.json["version"]
            return

        elif self.bump == 'current':            
            self.preversion()
            
            self.refresh_package()        
            version = self.json["version"]
            
            shell.run(f"git tag {version} && git push -q --tags")
            self.version()
            shell.run(f"git add . && git commit -q -m ${version} && git push -q")
            self.postversion()
        else:
            shell.run(f'npm version {self.bump}')

        self.refresh_package()

        for folder in [".dist", "dist", output_folder]:
            if os.path.isdir(folder):
                shutil.rmtree(folder)

        os.mkdir(output_folder)
    
    def execute_package(self) -> Tuple[str, List[str]]:
           
        if self.bump != 'existing':               
            cwd = os.getcwd()
            dist_folder= os.path.join(cwd, output_folder)
            os.chdir(dist_folder)
            shell.run(f'npm --quiet pack ..')
            os.chdir(cwd)

        try:
            package_path = self.get_package_path()
        except ValueError:
            self.bump = 'create'
            return self.execute_package()

        return package_path, []
    
    def get_package_path(self):
        package_path = ""
        for dir_path, dir_names, file_names in os.walk(output_folder):
            for file_name in file_names:
                if file_name.endswith("tgz"):
                    package_path = os.path.join(dir_path, file_name)
                    break

        if package_path == "":
            raise ValueError(self.directory)
        
        return package_path
    
    def get_gh_file_args(self, files : List[str]) -> str:
        file_args = ''
        if len(files) > 0:
            file_args = '\"{0}\"'.format('\", \"'.join(files))
        return file_args
                
    def release(self, package_path: str, additional_files : List[str]):
        package_path = f'./{package_path}'
        shell.run(f'npm --quiet --registry {npm_registry} --max-old-space-size=4096 publish {package_path}')

        file_args = self.get_gh_file_args(additional_files)
        
        shell.run("git push -q")
        
        version = self.json["version"]
        shell.run(
            f'gh release create v{version} \"{package_path}\" {file_args} -F RELEASELOG.md'
        )

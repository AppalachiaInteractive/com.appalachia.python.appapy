import json
from appapy.common import shell
from appapy.common.cli import note
from appapy.packaging.types.npm import NPMPackage
import shutil, os


class Unity3D(NPMPackage):
    def __init__(self, directory: str, bump: str):
        super(Unity3D, self).__init__(directory, bump)

    def after_version(self) -> None:
        # note("Creating UPM package.json")
        # npm_package_path=os.path.join(self.directory, "package.json")
        # upm_package_path=os.path.join(self.directory, "package.upm.json")
        # if os.path.isfile(upm_package_path):
        #     os.remove(upm_package_path)
            
        # shutil.copyfile(npm_package_path, upm_package_path)
         
        # with open(upm_package_path, 'r') as upm_package_content:
        #     upm_package_json = json.load(upm_package_content)
        
        # note("------------------------------")
        # note("------------------------------")
        # note(upm_package_content)
        # note("------------------------------")
        # note(upm_package_json)
        # note("------------------------------")
        # note("")
        
        # upm_package_json.pop('scripts', None)
        
        # with open(upm_package_path, 'w') as data_file:
        #     json.dump(upm_package_json, data_file)
    
        # shell.run("git add .")
        pass
        
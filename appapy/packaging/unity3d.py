from appapy.common import shell
from appapy.common.cli import note
from appapy.packaging.npm import NPMPackage


class Unity3D(NPMPackage):
    def __init__(self, directory: str, bump: str):
        super(Unity3D, self).__init__(directory, bump)


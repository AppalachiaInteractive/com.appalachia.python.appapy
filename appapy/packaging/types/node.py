from appapy.common import shell
from appapy.common.cli import demarcate, note
from appapy.packaging.types.npm import NPMPackage


class Node(NPMPackage):
    def __init__(self, directory: str, bump: str):
        super(Node, self).__init__(directory, bump)

    def test():
        demarcate("[TEST]")
        shell.run("mocha")

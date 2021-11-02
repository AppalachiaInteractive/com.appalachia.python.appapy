import os
from argparse import ArgumentError
from typing import List

from appapy.common.cli import *
from appapy.packaging.types.generic import Generic
from appapy.packaging.types.node import Node
from appapy.packaging.types.package import Package
from appapy.packaging.types.unity3d import Unity3D
from appapy.packaging.types.vscode import VSCode
from colorama import Fore


def execute(args: List[str], alsoPublish: bool):

    if len(args) != 0:
        raise ArgumentError(args, "No arguments needed!")

    package: Package
    working_directory = os.getcwd()

    note(f"Working Directory: {Fore.YELLOW}[{working_directory}]")

    path_markers = {
        "node": ["node"],
        "vscode": ["vscode"],
        "unity3d": ["Assets", "mdabros"],
    }

    tech = "generic"

    for marker in path_markers.keys():
        for value in path_markers[marker]:
            if value in working_directory:
                tech = marker
                break

    if tech == "generic":
        package = Generic(working_directory, 'patch')
    if tech == "node":
        package = Node(working_directory, 'patch')
    elif tech == "vscode":
        package = VSCode(working_directory, 'patch')
    elif tech == "unity3d":
        package = Unity3D(working_directory, 'patch')

    package_path, additional_files = package.execute_package()
    
    package_path = package_path.replace("\\", "/")

    if alsoPublish and package_path != '':
        package.release(package_path, additional_files)
        
    # package.execute_version()
    
    celebrate(f"{tech} publish successful!")

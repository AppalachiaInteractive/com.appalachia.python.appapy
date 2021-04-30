import os
from argparse import ArgumentError
from typing import List

from appapy.common.cli import *
from appapy.packaging.generic import Generic
from appapy.packaging.node import Node
from appapy.packaging.package import Package
from appapy.packaging.unity3d import Unity3D
from appapy.packaging.vscode import VSCode
from colorama import Fore


def execute(args: List[str]):

    if len(args) == 1:
        bump = args[0]
    else:
        raise ArgumentError(args, "Must provide a packaging bump.")

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
        package = Generic(working_directory, bump)
    if tech == "node":
        package = Node(working_directory, bump)
    elif tech == "vscode":
        package = VSCode(working_directory, bump)
    elif tech == "unity3d":
        package = Unity3D(working_directory, bump)

    package.execute_version()    
    package_path, additional_files = package.execute_package()    
    
    if package_path != '':
        package.release(package_path, additional_files)
    
    celebrate(f"{tech} {bump} successful!")

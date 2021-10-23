import os
from argparse import ArgumentError
from typing import List

from appapy.common.cli import *
from appapy.packaging.types.generic import Generic
from appapy.packaging.types.node import Node
from appapy.packaging.types.package import Package
from appapy.packaging.types.unity3d import Unity3D
from appapy.packaging.types.vscode import VSCode
from colorama.ansi import Fore


def execute(args: List[str]):

    if len(args) == 2:
        tech = args[0]
        stage = args[1]
    else:
        raise ArgumentError(args, "Must provide a packaging technology and stage.")

    highlight("Technology", tech)
    highlight("Stage", stage)

    package: Package
    working_directory = os.getcwd()

    if tech == "generic":
        package = Generic(working_directory, "")
    if tech == "node":
        package = Node(working_directory, "")
    elif tech == "vscode":
        package = VSCode(working_directory, "")
    elif tech == "unity3d":
        package = Unity3D(working_directory, "")

    func = getattr(package, stage)
    func()
    
    celebrate(f"{tech} {stage} successful!")

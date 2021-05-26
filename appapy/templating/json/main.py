import json, os
from typing import List

from appapy.templating.choices import Author, Project, License, Technology

projects = [
    Project("koc", "Keepers of Creation", ""),
]

authors = [
    Author("appa", "Appalachia Interactive", ""),
    Author("amplify", "Amplify Creations, Lda", ""),
    Author("aron-granberg", "Aron Granberg", ""),
    Author("awesome-technologies", "Awesome Technologies", ""),
    Author("dogmatic", "Dogmatic Games", ""),
    Author("gurbu", "GurBu Technologies", ""),
    Author("hapki", "Malte Hildingsson", ""),
    Author("hendrik-haupt", "Hendrik Haupt", ""),
    Author("jason-booth", "Jason Booth", ""),
    Author("mob-sakai", "mob-sakai", ""),
    Author("nature-manufacture", "Nature Manfuacture", ""),
    Author("procedural-worlds", "Procedural Worlds", ""),
    Author("qq_d_y", "Steven Gerrard", ""),
    Author("rootmotion", "ROOTMOTION", ""),
    Author("sandolkakos", "Marllon Vilano", ""),
    Author("sirenix", "Sirenix IVS", ""),
    Author("sycoforge-technogies", "Sycoforge Technologies", ""),
    Author("terraincomposer", "TerrainComposer", ""),
    Author("ultimate-game-tools", "Ultimate Game Tools", ""),
    Author("unity", "Unity Technologies", ""),
    Author("virtual-method", "Virtual Method", ""),
]

technologies = [
    Technology("dotnet", "Microsoft.NET", ""),
    Technology("python", "Python", ""),
    Technology("unity3d", "Unity3D", ""),
]

licenses = [
    License(
        "NONE",
        "UNLICENSED",
        "None",
        "This work will not be explicitly licensed, which releases no rights to the work to the public.",
    ),
    License(
        "AGPL",
        "AGPL-3.0-or-later",
        "GNU AGPLv3",
        "Permissions of this strongest copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license.",
    ),
    License(
        "GPL",
        "GPL-3.0-only",
        "GNU GPLv3",
        "Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license.",
    ),
    License(
        "LGPL",
        "LGPL-3.0-only",
        "GNU LGPLv3",
        "Permissions of this copyleft license are conditioned on making available complete source code of licensed works and modifications under the same license or the GNU GPLv3.",
    ),
    License(
        "MIT",
        "MIT",
        "MIT License",
        "A short and simple permissive license with conditions only requiring preservation of copyright and license notices.",
    ),
    License(
        "APL",
        "Apache-2.0",
        "Apache License 2.0",
        "A permissive license whose main conditions require preservation of copyright and license notices.",
    ),
    License(
        "MPL",
        "MPL-2.0",
        "Mozilla Public License 2.0",
        "Permissions of this weak copyleft license are conditioned on making available source code of licensed files and modifications of those files under the same license.",
    ),
    License(
        "UCL",
        "SEE LICENSE IN LICENSE",
        "Unity Companion License",
        "For open-source projects created by Unity Technologies ApS.",
    ),
    License(
        "ASEULA",
        "SEE LICENSE IN LICENSE",
        "Asset Store End User License Agreement",
        "For assets purchased on the Unity Asset Store",
    ),
    License(
        "CC",
        "CC-BY-NC-SA-4.0",
        "Creative Commons Attribution Non Commercial Share Alike 4.0 International",
        "Requires attribution, cannot be used commercially, and must be released under the same license.",
    ),
    License(
        "CCFREE",
        "CC-BY-SA-4.0",
        "Creative Commons Attribution Share Alike 4.0 International",
        "Requires attribution and must be released under the same license.",
    ),
    License(
        "DUAL",
        "SEE LICENSE IN LICENSE",
        "Dual licensing for forked projects",
        "Two licenses because the project was forked - identifies a commit that will mark the transition.",
    ),
]


def execute(args: List[str]):
    directory = os.path.abspath(os.path.dirname(__file__))

    projects_str = json.dumps(projects, default=vars, indent=4, sort_keys=True)
    projects_path = os.path.join(directory, "projects.json")
    with open(projects_path, mode="w") as fs:
        fs.write(projects_str)

    authors_str = json.dumps(authors, default=vars, indent=4, sort_keys=True)
    authors_spath = os.path.join(directory, "authors.json")
    with open(authors_spath, mode="w") as fs:
        fs.write(authors_str)

    technologies_str = json.dumps(technologies, default=vars, indent=4, sort_keys=True)
    technologies_path = os.path.join(directory, "technologies.json")
    with open(technologies_path, mode="w") as fs:
        fs.write(technologies_str)

    licenses_str = json.dumps(licenses, default=vars, indent=4, sort_keys=True)
    licenses_path = os.path.join(directory, "licenses.json")
    with open(licenses_path, mode="w") as fs:
        fs.write(licenses_str)

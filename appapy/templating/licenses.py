class License:
    def __init__(self, key: str, spdx_id: str, name: str, notes: str):
        self.key = key
        self.spdx_id = spdx_id
        self.name = name
        self.notes = notes

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
        "SEE LICENSE IN LICENSE.MD",
        "Unity Companion License",
        "For open-source projects created by Unity Technologies ApS.",
    ),
    License(
        "ASEULA",
        "SEE LICENSE IN LICENSE.MD",
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
        "SEE LICENSE IN LICENSE.MD",
        "Dual licensing for forked projects",
        "Two licenses because the project was forked - identifies a commit that will mark the transition.",
    ),
]

license_lookup = {license.key: license for license in licenses}

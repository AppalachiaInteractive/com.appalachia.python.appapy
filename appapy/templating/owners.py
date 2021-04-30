from abc import ABC, abstractmethod
from os import name
from typing import List

from appapy.common.cli import *
from appapy.templating.constants import *
from appapy.templating.licenses import License, license_lookup
from appapy.templating.repositories import Repository
from appapy.templating.utils import *


class Owner(ABC):
    def __init__(self, key: str, name: str, license_options: List[License]):
        self.key: str = key
        self.name: str = name
        self.license_options: List[License] = license_options
        self.license: License = None

    def set_license(self, repo: Repository):

        if len(self.license_options) == 0:
            self.license = license_lookup["NONE"]
        elif len(self.license_options) == 1:
            self.license = self.license_options[0]
        else:
            license_index = do_selection_until_confirmed(
                repo.license.confirmation_message,
                self.license_options,
                repo.license.enter_message
            )
            self.license = self.license_options[license_index]

        repo.license.value = self.license.key
        repo.licenseid.value = self.license.spdx_id

    @abstractmethod
    def extract_metadata(self, repo: Repository, parts: List[str]):
        pass


class AppalachiaInteractive(Owner):
    def __init__(self):
        super(AppalachiaInteractive, self).__init__(
            "appa",
            "Appalachia Interactive",
            license_options=[
                license_lookup["NONE"],
                license_lookup["AGPL"],
                license_lookup["MIT"],
                license_lookup["CC"],
                license_lookup["CCFREE"],
            ],
        )

    def extract_metadata(self, repo: Repository, parts: List[str]):
        if len(parts) == 3:
            # com.appalachia.library
            libr = get_clean_part(parts[2])
            repo.display.value = f"{libr}"
        elif len(parts) == 4:
            # com.appalachia.technology.library
            tech = get_clean_part(parts[2])
            libr = get_clean_part(parts[3])
            repo.display.value = f"{libr} for {tech}"
        elif len(parts) == 5:
            # com.appalachia.project.technology.library
            proj = get_clean_part(parts[2])
            tech = get_clean_part(parts[3])
            libr = get_clean_part(parts[4])
            repo.project.value = proj
            repo.display.value = f"{proj} - {libr} for {tech}"
        else:
            raise ValueError(repo.package.vaue)

        repo.author.value = "Appalachia Interactive"


class ThirdParty(Owner):
    def __init__(self):
        super(ThirdParty, self).__init__(
            "external",
            "Third Party",
            license_options=[
                license_lookup["AGPL"],
                license_lookup["GPL"],
                license_lookup["LGPL"],
                license_lookup["MIT"],
                license_lookup["APL"],
                license_lookup["MPL"],
                license_lookup["DUAL"],
            ],
        )

    def extract_metadata(self, repo: Repository, parts: List[str]):
        if len(parts) == 4:
            # com.appalachia.technology.library
            tech = get_clean_part(parts[2])
            libr = get_clean_part(parts[3])
            repo.display.value = f"{libr} for {tech}"
        elif len(parts) == 5:
            # com.appalachia.technology.author.library
            tech = get_clean_part(parts[2])
            auth = get_clean_part(parts[3])
            libr = get_clean_part(parts[4])
            repo.author.value = auth
            repo.display.value = f"{libr} for {tech}"
        elif len(parts) == 6:
            # com.appalachia.project.technology.author.library
            proj = get_clean_part(parts[2])
            tech = get_clean_part(parts[3])
            auth = get_clean_part(parts[4])
            libr = get_clean_part(parts[5])
            repo.project.value = proj
            repo.author.value = auth

            if tech == "servers":
                repo.display.value = f"{proj} - {libr}"
            else:
                repo.display.value = f"{proj} - {libr} for {tech}"
        else:
            raise ValueError(repo.package.value)


class UnityTechnologies(Owner):
    def __init__(self):
        super(UnityTechnologies, self).__init__(
            "unity",
            "Unity Technologies",
            license_options=[
                license_lookup["UCL"],
                license_lookup["MIT"],
                license_lookup["APL"],
            ],
        )

    def extract_metadata(self, repo: Repository, parts: List[str]):
        if len(parts) == 5:
            # com.appalachia.unity3d.unity.library
            libr = get_clean_part(parts[4])
            repo.display.value = f"{libr}"
        elif len(parts) == 6:
            # com.appalachia.project.unity3d.unity.library
            proj = get_clean_part(parts[2])
            libr = get_clean_part(parts[5])
            repo.project.value = proj
            repo.display.value = f"{proj} - {libr} for Unity 3D"
        else:
            raise ValueError(repo.package.value)

        repo.author.value = "Unity Technologies"


class UnityAssetStore(Owner):
    def __init__(self):
        super(UnityAssetStore, self).__init__(
            "assets",
            "Unity Asset Store Publisher",
            license_options=[
                license_lookup["ASEULA"],
            ],
        )

    def extract_metadata(self, repo: Repository, parts: List[str]):
        if len(parts) == 5:
            # com.appalachia.unity3d.author.library
            tech = get_clean_part(parts[2])
            auth = get_clean_part(parts[3])
            libr = get_clean_part(parts[4])
            repo.author.value = auth
            repo.display.value = f"{libr} for {tech}"
        elif len(parts) == 6:
            # com.appalachia.project.unity3d.author.library
            proj = get_clean_part(parts[2])
            tech = get_clean_part(parts[3])
            auth = get_clean_part(parts[4])
            libr = get_clean_part(parts[5])
            repo.project.value = proj
            repo.author.value = auth
            repo.display.value = f"{proj} - {libr} for {tech}"
        else:
            raise ValueError(repo.package.value)


owners: List[Owner] = [
    AppalachiaInteractive(),
    ThirdParty(),
    UnityTechnologies(),
    UnityAssetStore(),
]

owner_lookup = {owner.key: owner for owner in owners}

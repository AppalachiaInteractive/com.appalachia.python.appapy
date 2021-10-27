from abc import ABC, abstractmethod
from os import name
from typing import List

from appapy.common.cli import *
from appapy.templating.choices import ChoiceCollections, License
from appapy.templating.constants import *
from appapy.templating.repository import Repository
from appapy.templating.utils import *


class Owner(ABC):
    def __init__(self, key: str, name: str, license_options: List[License]):
        self.key: str = key
        self.name: str = name
        self.license_options: List[License] = license_options


class AppalachiaInteractive(Owner):
    def __init__(self):
        super(AppalachiaInteractive, self).__init__(
            "appa",
            "Appalachia Interactive",
            license_options=[
                ChoiceCollections.license_lookup["MIT"],
                ChoiceCollections.license_lookup["AGPL"],
                ChoiceCollections.license_lookup["CC"],
                ChoiceCollections.license_lookup["CCFREE"],
                ChoiceCollections.license_lookup["NONE"],
            ],
        )


class ThirdParty(Owner):
    def __init__(self):
        super(ThirdParty, self).__init__(
            "external",
            "Third Party",
            license_options=[
                ChoiceCollections.license_lookup["AGPL"],
                ChoiceCollections.license_lookup["GPL"],
                ChoiceCollections.license_lookup["LGPL"],
                ChoiceCollections.license_lookup["MIT"],
                ChoiceCollections.license_lookup["APL"],
                ChoiceCollections.license_lookup["MPL"],
                ChoiceCollections.license_lookup["DUAL"],
            ],
        )


class UnityTechnologies(Owner):
    def __init__(self):
        super(UnityTechnologies, self).__init__(
            "unity",
            "Unity Technologies",
            license_options=[
                ChoiceCollections.license_lookup["UCL"],
                ChoiceCollections.license_lookup["MIT"],
                ChoiceCollections.license_lookup["APL"],
            ],
        )


class UnityAssetStore(Owner):
    def __init__(self):
        super(UnityAssetStore, self).__init__(
            "assets",
            "Unity Asset Store Publisher",
            license_options=[
                ChoiceCollections.license_lookup["ASEULA"],
            ],
        )


owners: List[Owner] = [
    AppalachiaInteractive(),
    UnityTechnologies(),
    UnityAssetStore(),
    ThirdParty(),
]

owner_lookup = {owner.key: owner for owner in owners}

import os
from typing import List, Callable

from .constants import *

def remove_file(path: str, include_meta: bool = True):
    if DRY_RUN:
        return

    meta = "{0}.meta".format(path)
    os.remove(path)
    if include_meta and os.path.isfile(meta):
        os.remove(meta)


def rename_file(old: str, new: str, include_meta: bool = True):
    if DRY_RUN:
        return

    meta_old = "{0}.meta".format(old)
    meta_new = "{0}.meta".format(new)
    os.rename(old, new)
    if include_meta and os.path.isfile(meta_old):
        os.rename(meta_old, meta_new)


def no_validation(parameter: str) -> bool:
    return True

def get_clean_part(value: str) -> str:
    return value.replace("-", " ").replace("3d", "3D").title()

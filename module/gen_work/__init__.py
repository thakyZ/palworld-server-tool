#!/usr/bin/env python3

"""Main Function for the module `gen_work`."""

from .gen_pal_skills import GenPalSkills
from .gen_pal_type import GenPalType


def generate() -> None:
    """Generates Enum Types from Web Requests."""
    GenPalSkills().generate()
    GenPalType().generate()

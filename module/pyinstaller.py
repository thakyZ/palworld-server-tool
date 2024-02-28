#!/usr/bin/env python3

"""Python Installer Build Script"""

# pyright: reportAttributeAccessIssue=false
# cSpell:ignore --onefile

import platform
from pathlib import Path
import PyInstaller
from gen_work import generate

HERE: Path = Path(__file__).parent.absolute()
path_to_main: str = str(HERE.joinpath("sav_cli.py"))


def get_system_info() -> tuple[str, str]:
    """Gets system information for the file name.

    Returns:
        tuple[str, str]: A tuple containing the OS name and Architecture type.
    """
    (os, _, _, _, arch, _) = platform.uname()
    return (os.lower(), arch.lower())


def install() -> None:
    """Main build function."""

    (os, arch) = get_system_info()
    generate()
    # pylint: disable-next=E1101
    PyInstaller.__main__.run([
        path_to_main,
        "--onefile",
        "-n",
        f"sav_cli_{os}_{arch}"
    ])

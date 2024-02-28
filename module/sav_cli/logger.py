#!/usr/bin/env python3

"""Logger Module"""

from datetime import datetime
from typing import Literal


def log(text: str, level: Literal["INFO", "WARN", "ERROR"] = "INFO") -> None:
    """Logs the information to console with a logging level.

    Args:
        text (str): The text to log to console.
        level (Literal["INFO", "WARN", "ERROR"], optional): The log level. Defaults to "INFO".
    """
    prefix = "[SAV-CLI]"
    current: str = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    print(f"{prefix} {current} | {level.upper()} | {text}")

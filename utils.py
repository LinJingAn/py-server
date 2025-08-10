"""
utils.py

Platform helpers and lightweight dependency checks.
"""

import platform
import shutil
import logging

logger = logging.getLogger(__name__)


def is_linux() -> bool:
    return platform.system().lower() == "linux"


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def check_tool_available(name: str) -> bool:
    """Return True if `name` exists in PATH."""
    return shutil.which(name) is not None


def ensure_ubuntu_deps() -> list:
    """
    Log and return missing tools commonly used on Ubuntu for window/control:
    - wmctrl, xdotool, python3-xlib (python3-xlib is not checkable via PATH)
    This does NOT install anything; it only warns.
    """
    missing = []
    for tool in ("wmctrl", "xdotool"):
        if not check_tool_available(tool):
            missing.append(tool)

    if missing:
        logger.warning(
            "Missing system tools: %s. On Ubuntu install: sudo apt install %s",
            ", ".join(missing), " ".join(missing)
        )
    else:
        logger.debug("All checked Ubuntu tools present.")

    return missing

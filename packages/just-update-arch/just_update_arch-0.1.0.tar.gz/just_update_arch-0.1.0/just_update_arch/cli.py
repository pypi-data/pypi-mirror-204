#!/usr/bin/env python3
# Licensed under the GNU General Public License v3.0.

import pathlib
import subprocess

from shutil import which
from colorama import Fore


aur_packages: list[str]
# The AUR helpers supported by this tool.
aur_helpers: list[str] = ["paru"]
found_aur_helpers: list[str] = []

"""
    Loops through `aur_helpers`, a list of supported
    AUR helpers, and appends whatever AUR helper is
    found to `found_aur_helpers`.
"""


def detect_aur_helpers():
    global aur_helpers
    global found_aur_helpers
    global use_paru_cache

    # Check whether Paru is available
    for aur_helper in aur_helpers:
        if which(aur_helper) is not None:
            match aur_helper:
                case "paru":
                    found_aur_helpers.append("paru")


"""
    Lists all installed AUR packages using the `pacman`
    command, and removes the version numbers of said
    packages.

    Returns a list of strings.
"""


def get_aur_packages() -> list[str]:
    global aur_packages

    package_query = subprocess.check_output("pacman -Qm | awk '{print $1}'", shell=True)
    package_query = package_query.decode()

    aur_packages = str(package_query).split()

    return aur_packages


"""
    Simply builds an AUR package using:
    ```sh
        cd $repository_path && makepkg -si --noconfirm
    ```

    The `$repository_path` variable is not actually
    set as a Shell variable, instead it is the
    `repository_path` variable in the `cli.py` script.
"""


def build_aur_package(repository_path: str):
    subprocess.run(f"cd {repository_path} && makepkg -si --noconfirm", shell=True)


"""
    Checks the found AUR helpers, and loops through
    their cached packages, which are in the form
    of cloned Git repositories.
"""


def build_aur_packages():
    global aur_packages
    global found_aur_helpers

    for aur_package in aur_packages:
        print(aur_package)

    # Check the cache directories of matching AUR helpers
    for found_aur_helper in found_aur_helpers:
        match found_aur_helper:
            case "paru":
                paru_cache = pathlib.Path(f"{pathlib.Path.home()}/.cache/paru/clone")
                for repository in paru_cache.iterdir():
                    build_aur_package(repository)


"""
    Updates both the vanilla Arch packages and AUR packages.
"""


def update():
    subprocess.run("sudo pacman -Syu", shell=True)

    get_aur_packages()
    detect_aur_helpers()
    build_aur_packages()


if __name__ == "__main__":
    update()

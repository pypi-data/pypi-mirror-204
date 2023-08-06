import subprocess
import os
from setuptools import find_packages, setup

with open("README.md", encoding="UTF-8") as readme:
    long_desc = readme.read()

if os.path.exists("src"):
    subprocess.run("mv src just_update_arch", shell=True)

setup(
    name="just_update_arch",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    description="Updates installed AUR packages.",
    author="MolassesLover",
    author_email="60114762+MolassesLover@users.noreply.github.com",
    url="https://github.com/MolassesLover/JustUpdateArch",
    install_requires=["colorama"],
    license="GNU General Public License v3.0",
    entry_points={
        "console_scripts": [
            "just_update_arch = just_update_arch.cli:update",
        ]
    },
)

if os.path.exists("just_update_arch"):
    subprocess.run("mv just_update_arch src", shell=True)
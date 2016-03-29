#!/usr/bin/env python3
import os
import sys
from setuptools import setup

from rock_cli import __version__

if sys.argv[-1] == 'publish':
    if os.system("pip3 freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    os.system("python3 setup.py sdist upload")
    os.system("python3 setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(__version__))
    print("  git push --tags")
    sys.exit()

setup(
    name="rock-cli",
    version=__version__,
    author="Ale",
    author_email="ale@songbee.net",
    description="A Rocketbank CLI",
    url="https://github.com/iamale/rock",
    packages=["rock_cli"],
    install_requires=[
        "Click==6.4",
        "yamlcfg==0.5.3",
        "tabulate==0.7.5",
        "arequests==0.1.0",
    ],
    entry_points="""
        [console_scripts]
        rock=rock_cli.cli:cli
    """,
)

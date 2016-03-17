from setuptools import setup

from rock_cli import __version__

setup(
    name="rock-cli",
    version=__version__,
    author="Ale",
    author_email="ale@songbee.net",
    description="A Rocketbank CLI",
    url="https://github.com/iamale/rock",
    packages=["rock_cli"],
    install_requires=[
        "Click",
        "yamlcfg",
        "tabulate",
        "arequests==0.1.0",
    ],
    entry_points="""
        [console_scripts]
        rock=rock_cli.cli:cli
    """,
)

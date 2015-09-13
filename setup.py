from setuptools import setup

setup(
    name='rock-cli',
    version='0.1',
    py_modules=['rock_cli'],
    install_requires=[
        'Click',
        'requests',
        'yamlcfg',
    ],
    entry_points='''
        [console_scripts]
        rock=rock_cli.cli:cli
    ''',
)

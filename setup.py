from setuptools import setup

setup(
    name='rock-cli',
    version='0.1.1',
    author='Ale',
    author_email='ale@songbee.net',
    description='A Rocketbank CLI',
    url='https://github.com/iamale/rock',
    packages = ['rock_cli'],
    install_requires=[
        'Click',
        'requests',
        'yamlcfg',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        rock=rock_cli.cli:cli
    ''',
)

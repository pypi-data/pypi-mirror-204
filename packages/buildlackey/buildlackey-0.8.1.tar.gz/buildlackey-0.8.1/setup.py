import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README  = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()
VERSION = (HERE / 'buildlackey/resources/version.txt').read_text()

setup(
    name="buildlackey",
    version=VERSION,
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Project Maintenance Scripts',
    long_description=README,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url="https://github.com/buildlackey",
    packages=[
        'buildlackey',
        'buildlackey.exceptions',
        'buildlackey.resources',
    ],
    package_data={
        'buildlackey.resources': ['loggingConfiguration.json', 'version.txt'],
    },

    install_requires=[
        'click~=8.1.3',
    ],
    entry_points={
        "console_scripts": [
            "runtests=buildlackey.Commands:runtests",
            "cleanup=buildlackey.Commands:cleanup",
            "runmypy=buildlackey.Commands:runmypy",
            "deploy=buildlackey.Commands:deploy",
            "prodpush=buildlackey.Commands:prodpush",
        ]
    },
)

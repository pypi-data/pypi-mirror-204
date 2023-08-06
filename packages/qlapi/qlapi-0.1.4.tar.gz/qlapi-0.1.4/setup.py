from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.4'
AUTHOR='eegion'
EMAIL='hehuajun@eegion.com'
REQUIRED = [
    'mne',
]

setup(
    name='qlapi',  # package name
    version=VERSION,  # package version
    author=AUTHOR,
    author_email=EMAIL,
    requires=REQUIRED,
    description='Api for use quanlan device',  # package description
    packages=find_packages(),
    package_data={
        "qlapi": ["lib/*.dll"],
        "":["*.txt", "*.md"]
    },
    zip_safe=False,
)
from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.2'

setup(
    name='qlapi',  # package name
    version=VERSION,  # package version
    description='Api for use quanlan device',  # package description
    packages=find_packages(),
    package_data={
        "device": ["lib/*.dll"],
        "":["*.txt", "*.md"]
    },
    zip_safe=False,
)
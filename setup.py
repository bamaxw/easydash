from setuptools import setup, find_packages
import os
import re


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rt") as fh:
        return fh.read()

_version_regex = r'^\s*__version__\s*=\s*(\"|\')(?P<version>.*)\1'
def get_version():
    version_str = read("easydash/__init__.py")
    match = re.search(_version_regex, version_str)
    if match is None:
        raise ValueError("Failed to find version number")
    return match['version']

setup(
    name="EasyDash",
    author="Maximus Wasylow",
    version=get_version(),
    author_email="bamwasylow@gmail.com",
    description="A command line tool for easy cloud-watch dashboard generation",
    long_description=read("README.md"),
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'boto3'
    ],
    dependency_links=[
        'https://bitbucket.org/maxwasylow/helpers.git#egg=helpers'
    ],
    entry_points={
        'console_scripts': [
            'dash=easydash.command:main'
        ]
    }
)

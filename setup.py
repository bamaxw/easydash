from setuptools import setup, find_packages
import os
import re


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rt") as fh:
        return fh.read()

_version_regex = r'^\s*__version__\s*=\s*(\"|\')(?P<version>.*)\1'
def get_version():
    version_str = read("easydash/__init__.py")
    matches = re.findall(_version_regex, version_str)
    if len(matches) == 0:
        raise ValueError("Failed to find version number")
    return matches[0]

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
        'git+https://bitbucket.org/maxwasylow/helpers.git'
    ],
    entry_points={
        'console_scripts': [
            'dash=easydash.command:main'
        ]
    }
)

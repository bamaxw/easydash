from setuptools import setup, find_packages
import os
import re


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rt") as fh:
        return fh.read()

setup(
    name="EasyDash",
    author="Maximus Wasylow",
    version='0.0.0',
    author_email="bamwasylow@gmail.com",
    description="A command line tool for easy cloud-watch dashboard generation",
    long_description=read("README.md"),
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=['boto3'],
    dependency_links=['https://github.com/bamaxw/ion.git'],
    entry_points={'console_scripts': ['dash=easydash.cli:cli']}
)

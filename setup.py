import os

from setuptools import find_packages
from setuptools import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def parse_requirements():
    with open("requirements.txt") as req_file:
        install_requires = list()
        for line in req_file.read().splitlines():
            comment_start = line.find("#")
            if comment_start > -1:
                line = line[:comment_start].strip()
            if line and not line.startswith("-"):
                install_requires.append(line)
        return install_requires


setup(
    name="unbridaled",
    version=get_version("src/__init__.py"),
    packages=find_packages(include=["src", "tests"]),
    install_requires=parse_requirements(),
)

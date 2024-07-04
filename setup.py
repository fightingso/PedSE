import io
import os

import setuptools


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf8") as f:
        return f.read()


def get_requirements():
    with open("requirements.txt", encoding="utf8") as f:
        return f.read().splitlines()


setuptools.setup(
    name="pedse",
    version="0.0.dev1",
    author="fightingso",
    license="MIT",
    long_description=get_long_description(),
    url="https://github.com/fightingso/pedse"
    install_requires=get_requirements(),
)

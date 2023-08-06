#!/usr/bin/env python
# coding: utf8

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as handle:
    readme = handle.read()

setup(
    name="tzconv",
    version="1.2",
    description="command-line tool to convert a date and time to several time zones at once",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Gabor Nyeki",
    url="https://codeberg.org/gnyeki/tzconv",
    packages=["tzconv"],
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "tzconv = tzconv:main",
        ],
    }
    )

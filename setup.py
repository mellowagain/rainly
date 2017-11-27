#!/usr/bin/env python

from setuptools import setup

readme = ""
with open("README.md") as file:
    readme = file.read()

requirements = []
with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="rainly",
    version="0.0.1",
    description="A wrapper around various web hooks for the Discord WebHooks API",
    author="Marc Steiner",
    author_email="info@marcsteiner.me",
    url="https://github.com/Marc3842h/rainly",
    long_description=readme,
    include_package_data=True,
    packages=[
        "rainly",
        "rainly.modules"
    ],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat"
    ]
)

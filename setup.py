#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="protocards",
    version="0.1.1",
    author="Finn Ellis",
    author_email="relsqui@chiliahedron.com",
    license="MIT",
    description="Basic tools for working with generic game cards in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/relsqui/protocards",
    provides=[
        "protocards",
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

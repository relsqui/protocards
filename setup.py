#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="pycards",
        version='0.1.0',
        description="Simple tools for building card games in python.",
        license="MIT",
        author="Finn Ellis", 
        author_email="relsqui@chiliahedron.com",
        url="https://github.com/relsqui/pycards",
        provides=[
            "pycards",
        ],
        packages=[
            "pycards",
            "pycards.tests"
        ],
        package_data={
            'pycards': ["README.md"],
        },
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

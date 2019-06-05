#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="pydeck",
        #version='0.0.0',
        description="Simple tools for building card games in python.",
        #license="",
        author="Finn Ellis", 
        author_email="relsqui@chiliahedron.com",
        url="https://github.com/relsqui/pydeck",
        provides=[
            "pydeck",
        ],
        packages=[
            "pydeck",
            "pydeck.tests"
        ],
        package_data={
            'pydeck': ["README.md"],
        },
        include_package_data=True,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    )

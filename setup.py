#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="protocards",
        version='0.1.0',
        description="Simple tools for building card games in python.",
        license="MIT",
        author="Finn Ellis",
        author_email="relsqui@chiliahedron.com",
        url="https://github.com/relsqui/protocards",
        provides=[
            "protocards",
        ],
        packages=[
            "protocards",
            "protocards.tests"
        ],
        package_data={
            'protocards': ["README.md"],
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

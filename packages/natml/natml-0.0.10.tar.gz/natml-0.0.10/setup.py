# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from setuptools import find_packages, setup

# Get readme
with open("README.md", "r") as readme:
    long_description = readme.read()

# Get version
with open("natml/version.py") as version_source:
    gvars = {}
    exec(version_source.read(), gvars)
    version = gvars["__version__"]

# Setup
setup(
    name="natml",
    version=version,
    author="NatML Inc.",
    author_email="hi@natml.ai",
    description="Zero deployment machine learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
	python_requires=">=3.7",
    install_requires=[
        "filetype",
        "numpy",
        "pillow",
        "requests",
        "rich",
        "typer"
    ],
    url="https://natml.ai",
    packages=find_packages(
        include=["natml", "natml.*"],
        exclude=["test", "examples"]
    ),
    entry_points={
        "console_scripts": [
            "natml=natml.cli.__init__:app"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries",
    ],
    project_urls={
        "Documentation": "https://docs.natml.ai/python",
        "Source": "https://github.com/natmlx/natml-py"
    },
)
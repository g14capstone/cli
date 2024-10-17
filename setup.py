"""
Setup script for the Duckington CLI tool.

This script uses setuptools to configure and package the Duckington CLI application.
It specifies the package name, version, dependencies, and entry points for the CLI.

Key components:
- name: The name of the package as it will appear in pip and PyPI.
- packages: Automatically finds and includes all Python packages in the project.
- install_requires: Specifies the dependencies required to run the application.
- version: The current version of the package.
- entry_points: Defines the command-line interface entry point, allowing the app
                to be run using the 'quack' command after installation.

To install the package, run: pip install . or pip install -e . for debugging/editable mode.
After installation, the CLI can be invoked using the 'quack' command.
"""

from setuptools import setup, find_packages

setup(
    name="duckington-cli",
    packages=find_packages(),
    install_requires=["click", "requests"],
    version="0.0.1",
    entry_points="""
    [console_scripts]
    quack=src.main:quack
    """,
)

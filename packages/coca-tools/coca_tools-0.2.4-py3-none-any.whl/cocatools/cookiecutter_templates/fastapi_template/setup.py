# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='{{cookiecutter.project_name}}',
    version='0.1.0',
    author='{{cookiecutter.author_name}}',
    author_email='{{cookiecutter.email}}',
    packages=find_packages(),
    install_requires=[
        # Add any required packages here
    ],
)

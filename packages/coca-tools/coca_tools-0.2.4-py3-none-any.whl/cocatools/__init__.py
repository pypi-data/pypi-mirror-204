# -*- coding: utf-8 -*-

"""Entry point of my coca tools
"""
import os

from cookiecutter.main import cookiecutter

__version__ = '0.2.4'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_PATH, 'cookiecutter_templates')


def welcome():
    """Say welcome to users"""
    print('welcome to coca tools')


def create_fastapi_app():
    template_path = os.path.join(TEMPLATE_PATH, 'fastapi_template')
    cookiecutter(template_path)


def create_django_app():
    template_path = os.path.join(TEMPLATE_PATH, 'django_template')
    cookiecutter(template_path)


def create_monorepo_project():
    pass


def create_monorepo_fastapi_service():
    pass


def create_monorepo_django_service():
    pass

# -*- coding: utf-8 -*-
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.project.settings')
django.setup()


from .apps.proxy_mgmt import db_initializers as proxy_db_initializers
from .apps.taiga_mgmt import db_initializers as taiga_db_initializers
from .apps.user import db_initializers as user_db_initializers


def rull_initializers():
    proxy_db_initializers.create_proxy()
    taiga_db_initializers.create_taiga_account()
    taiga_db_initializers.create_taiga_api()
    user_db_initializers.create_admin()


if __name__ == '__main__':
    rull_initializers()

# -*- coding: utf-8 -*-
import logging  # noqa


async def event_01_reversed():
    pass


async def event_02_connect_postgresql_database():
    pass


async def event_03_disconnect_nats():
    pass


async def event_04_connect_redis():
    pass


async def event_05_load_config():
    pass


async def event_06_connect_telegram():
    pass


async def event_99_notify_app_stopped():
    pass


events = [v for k, v in locals().items() if k.startswith("event_")]

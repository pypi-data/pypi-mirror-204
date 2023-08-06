# -*- coding: utf-8 -*-
import logging  # noqa
from src import constants
from src.settings import settings


logger = logging.getLogger(constants.CONSOLE_LOGGER)


async def event_01_connect_redis():
    if not settings.REDIS_ENABLE:
        return
    from src.dbs.redis_cache.client_manager import RedisManager

    redis_manager = RedisManager()
    await redis_manager.set_client(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_AUTH,
        db=settings.REDIS_DB
    )


async def event_02_connect_database():
    if not settings.DB_MONGO_ENABLE:
        return
    from src.dbs.mongodb import client      # noqa  just import to trigger connection


events = [v for k, v in sorted(locals().items()) if k.startswith("event_")]
print(events)

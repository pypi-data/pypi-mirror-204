# -*- coding: utf-8 -*-
import asyncio
import inspect
import logging
from typing import Callable, Dict
from src import constants
from src.utils.singleton import SingletonClass
from redis.asyncio import Redis, Sentinel
from redis.asyncio.lock import Lock as RedisLock
from redis.client import PubSub


class RedisManager(SingletonClass):
    master_client: Redis = None
    slave_client: Redis = None
    logger: logging.Logger = logging.getLogger(constants.CONSOLE_LOGGER)

    def _singleton_init(self):
        self.user_status_scanner_lock: RedisLock = None

    def set_logger(self, logger: logging.Logger):
        if not isinstance(logger, logging.Logger):
            raise ValueError(f'expected logger is an instance of logging.Logger -> get {logger=}')
        self.logger = logger

    async def set_client(
        self,
        host: str = None,
        port: int = None,
        password: str = None,
        db: int = 0,
        client: Redis = None
    ):
        """_summary_

        Args:
            host (str, optional): _description_. Defaults to None.
            port (int, optional): _description_. Defaults to None.
            password (str, optional): _description_. Defaults to None.
            db (int, optional): _description_. Defaults to 0.
            client (Redis, optional): _description_. Defaults to None.
        """
        if isinstance(client, Redis):
            self.master_client = client
            self.slave_client = client
            return
        if host and port:
            if not db:
                db = 0
            self.master_client = Redis(
                host=host,
                port=port,
                db=db,
                password=password
            )
            self.slave_client = self.master_client
            self.logger.info(f'connect redis {self.master_client=} | {self.slave_client=}')
            return

    async def set_sentinel(self, sentinel: Sentinel = None):
        """For latter

        Args:
            sentinel (Sentinel, optional): _description_. Defaults to None.
        """
        pass

    def get_subscriber(self) -> PubSub:
        return self.slave_client.pubsub()

    async def handle_pubsub_msg(
        self,
        subscriber: PubSub,
        handler: Callable,
        handler_kwargs: Dict = {},
        sleep_time: float = 0.1
    ):
        if not subscriber:
            subscriber = self.get_subscriber()
        while True:
            data = await subscriber.get_message()
            if data:
                message = data['data']
                if message and message != 1:
                    await handler(message, **handler_kwargs)
            await asyncio.sleep(sleep_time)

    async def subscribe(
        self,
        channel: str,
        handler: Callable,
        handler_kwawrgs: Dict = {},
        sleep_time: float = 0.1
    ):
        """_summary_

        Args:
            channel (str): _description_
            handler (Callable): _description_
            handler_kwawrgs (Dict, optional): _description_. Defaults to {}.
            sleep_time (float, optional): _description_. Defaults to 0.1.

        Raises:
            ValueError: _description_
        """
        if not inspect.iscoroutinefunction(handler):
            raise ValueError('handler must be a coroutine')

        subscriber: PubSub = self.get_subscriber()
        await subscriber.subscribe(channel, ignore_subscribe_messages=True)
        task = asyncio.create_task(
            self.handle_pubsub_msg(subscriber, handler, handler_kwawrgs, sleep_time)
        )
        self.logger.debug(f'PubsubManager subscribe {channel=} with {handler} -> {task=}')

    async def publish(self, channel: str, message: str):
        """_summary_

        Args:
            channel (str): _description_
            message (str): _description_

        Raises:
            ValueError: _description_
        """
        for i in (channel, message,):
            if not i or not isinstance(i, str):
                raise ValueError('parameter must be an instance of string')

        await self.master_client.publish(channel, message)


client_manager = RedisManager()
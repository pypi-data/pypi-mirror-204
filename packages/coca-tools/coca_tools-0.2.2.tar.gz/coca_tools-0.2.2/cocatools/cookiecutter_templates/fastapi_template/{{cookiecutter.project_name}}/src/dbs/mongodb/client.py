# -*- coding: utf-8 -*-
import asyncio
from umongo.frameworks import MotorAsyncIOInstance
from motor.motor_asyncio import AsyncIOMotorClient
from ...settings import settings

# print(env.APP_DB_MONGO_URI)

client = AsyncIOMotorClient(settings.get_mongo_uri())[settings.DB_MONGO_DB_NAME]
# fix mongo connection attached to a different loop
client.get_io_loop = asyncio.get_running_loop
umongo_cnx = MotorAsyncIOInstance(client)


# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://host1,host2/?replicaSet=my-replicaset-name')

# more detail in links bellow
# https://github.com/Scille/umongo
# https://motor.readthedocs.io/en/stable/tutorial-asyncio.html

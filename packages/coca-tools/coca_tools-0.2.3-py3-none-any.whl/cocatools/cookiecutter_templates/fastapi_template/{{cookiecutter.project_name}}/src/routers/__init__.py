# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .example import example_router

# import your router here


api_router = APIRouter()


for r in (
    example_router,
    # add your router here
):
    api_router.include_router(r)

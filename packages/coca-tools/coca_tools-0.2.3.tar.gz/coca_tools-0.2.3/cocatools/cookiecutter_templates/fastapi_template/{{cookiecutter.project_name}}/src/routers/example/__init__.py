# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .schema import GetInfoRequest
from .utils import get_detail_info_example

example_router = APIRouter(prefix='/example')


@example_router.post('/get_info')
async def get_example_info(req: GetInfoRequest):
    return {'data': [get_detail_info_example(req.user_id)]}

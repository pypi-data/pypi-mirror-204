#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : fastapi流式接口
# @Time         : 2023/4/14 13:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/weixin_43228814/article/details/130063010

from meutils.pipe import *

from typing import Generator
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI()


def generate_data():
    for i in range(10):
        time.sleep(i)
        print(i)
        yield f"data {i}\n"


@app.get("/")
async def stream_data():
    return StreamingResponse(generate_data())


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : s
# @Time         : 2023/3/7 上午9:57
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.docarray_ import DocumentArray, Document

from jina import  Executor, Flow, requests

logger.info(os.getpid())


class FooExec(Executor):
    logger.info(os.getpid())

    @requests
    async def add_text(self, docs: DocumentArray, **kwargs):
        logger.info(os.getpid())

        # print(os.getpid(), file=f'{os.getpid()}.txt')

        for d in docs:
            d.text += 'hello, world!'


class BarExec(Executor):
    logger.info(os.getpid())

    @requests
    async def add_text(self, docs: DocumentArray, **kwargs):
        logger.info(os.getpid())
        # print(os.getpid(), file=f'{os.getpid()}.txt')

        for d in docs:
            d.text += 'goodbye!'


f = Flow(port=12345).add(uses=FooExec, replicas=3).add(uses=BarExec, replicas=2)

with f:
    f.post(DocumentArray(Document(text='我在南京')))
    # for i in tqdm(range(100)):
    #     da = DocumentArray([Document(text='a')])
    #     f.post(da)
    f.block()

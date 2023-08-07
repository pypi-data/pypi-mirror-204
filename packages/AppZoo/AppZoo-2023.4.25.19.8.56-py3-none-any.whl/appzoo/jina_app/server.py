#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : server
# @Time         : 2022/9/9 下午4:59
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

os.environ['JINA_HIDE_SURVEY'] = '0'
import time

import jieba
from jina import Document, DocumentArray, Executor, Flow, requests, Deployment


class MyExec(Executor):
    @requests(on='/search')
    def add_text(self, docs: DocumentArray, **kwargs):
        print('#')

        for d in docs:
            d.text += 'hello, world!'


class Cut(Executor):
    @requests(on='/cut')
    def add_text(self, docs: DocumentArray, **kwargs):
        print('##')
        for d in docs:
            d.text = ' '.join(jieba.lcut(d.text))


class Read(Executor):
    @requests(on='/read')
    async def add_text(self, docs: DocumentArray, **kwargs):

        with open('data.txt') as f:
            for i in f:
                print(i)
                time.sleep(1)
                yield i

        for d in docs:
            d.text = ' '.join(jieba.lcut(d.text))


def generate_data():
    for i in range(10):
        time.sleep(i)
        print(i)
        yield f"data {i}\n"


class StreamingExecutor(Executor):

    @requests(on='/stream')
    def foo(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            for ret in generate_data():
                yield Document(text=ret)


# f = Flow(port=9955).add(uses=MyExec)
# f = Flow(port=8501, protocol=['GRPC']).add(uses=MyExec).add(uses=Cut)
f = Flow(port=[8500, 8501], protocol=['GRPC', 'HTTP']).add(uses=MyExec)#.add(uses=Cut).add(uses=Read)
#
# with f:
#     # 测试
#     # r = f.post('/', DocumentArray(Document(text='我是中國人')))
#     r = f.post('/', DocumentArray.empty(2))
#
#     print(r.texts)
#
#     # backend server forever
#     f.block()


with Deployment(name='myexec1', uses=MyExec) as dep:
    dep.post(on='/bar', inputs=Document(), on_done=print)
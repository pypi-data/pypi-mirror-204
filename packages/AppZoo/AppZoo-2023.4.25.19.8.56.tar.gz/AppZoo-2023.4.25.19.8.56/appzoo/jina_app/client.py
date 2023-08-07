#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : client
# @Time         : 2022/9/9 下午5:02
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from jina import Client, Document, DocumentArray

# c = Client(host='grpc://0.0.0.0:8501')
c = Client(host='http://0.0.0.0:8501')


print(c.post('/cut', DocumentArray(Document(text='我在南京'))).texts)

# r = c.post(
#     '/',
#     inputs=DocumentArray([
#         Document(text='如何更换花呗绑定银行卡'),
#         Document(text='花呗更改绑定银行卡')
#     ])
# )
# print(r.embeddings)

#
# {
#     "data": [
#         {
#             "text": "我在南京"
#         }
#     ]
# }

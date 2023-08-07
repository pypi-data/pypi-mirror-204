#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : flask流式接口
# @Time         : 2023/4/14 13:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : test
# @Time         : 2023/4/14 10:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from flask import Flask, Response

import time

from flask import Flask, Response

app = Flask(__name__)


def generate_data():
    for i in range(10):
        time.sleep(i)
        yield f"data {i}\n"


# 流式接口路由
@app.route('/')
def stream():
    # 返回Response对象并设置Content-Type为text/event-stream
    return Response(generate_data(), mimetype='text/event-stream')

#
# import requests
#
# # 发送GET请求并获取响应对象
# response = requests.get('http://127.0.0.1:8000', stream=True)
#
# # 遍历响应内容并处理每个数据块
# for chunk in response.iter_content(chunk_size=1024):
#     if chunk:
#         # 处理流式数据块，例如将其写入文件、解析JSON等
#         print(chunk)



if __name__ == '__main__':
    app.run(debug=True)

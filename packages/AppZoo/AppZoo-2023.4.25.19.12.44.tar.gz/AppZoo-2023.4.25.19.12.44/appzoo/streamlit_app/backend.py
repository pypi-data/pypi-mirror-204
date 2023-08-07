#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : backend
# @Time         : 2023/4/9 12:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 后台起服务：一个线程起http 主进程grpc

from meutils.pipe import *

import streamlit as st
from meutils.decorators import backend

print("xxxxx")
st.markdown('xxxxx')


@st.experimental_memo  # 运行一次
@backend
def api():
    print('api')
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return jsonify({"message": "Hello, World"})

    app.run(port=8000)


api()

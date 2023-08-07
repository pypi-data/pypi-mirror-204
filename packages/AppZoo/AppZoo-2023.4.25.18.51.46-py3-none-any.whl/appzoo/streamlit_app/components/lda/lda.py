#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lda
# @Time         : 2023/4/9 11:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import streamlit as st
from streamlit.components.v1 import components

_component_func = components.declare_component(
    # We give the component a simple, descriptive name ("my_component"
    # does not fit this bill, so please choose something better for your
    # own component :)
    "st_autorefresh",
    # Pass `url` here to tell Streamlit that the component will be served
    # by the local dev server that you run via `npm run start`.
    # (This is useful while your component is in development.)
    url="http://localhost:3001",
)


def st_autorefresh(interval=1000, limit=None, key=None):
    count = _component_func(interval=interval, limit=limit, key=key)
    if count is None:
        return 0

    return int(count)

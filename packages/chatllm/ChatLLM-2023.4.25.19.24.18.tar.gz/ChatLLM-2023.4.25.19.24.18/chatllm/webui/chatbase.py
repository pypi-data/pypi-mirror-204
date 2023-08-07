#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatpdf
# @Time         : 2023/4/25 17:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.applications import ChatBase
from chatllm.utils import llm_load4chat

import streamlit as st
from appzoo.streamlit_app.utils import display_pdf, reply4input

st.set_page_config('🔥ChatLLM', layout='wide', initial_sidebar_state='collapsed')


@st.experimental_singleton
def get_chat_func():
    chat_func = llm_load4chat(
        model_name_or_path="/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm"
    )
    return chat_func


chat_func = get_chat_func()

qa = ChatBase(chat_func=chat_func).qa

container = st.container()  # 占位符
text = st.text_area(label="用户输入", height=100, placeholder="请在这儿输入您的问题")
# knowledge_base = st.sidebar.text_area(label="知识库", height=100, placeholder="请在这儿输入您的问题")

if st.button("发送", key="predict"):
    with st.spinner("AI正在思考，请稍等........"):
        history = st.session_state.get('state')
        st.session_state["state"] = reply4input(text, history, container=container, reply_func=qa, max_turns=1)

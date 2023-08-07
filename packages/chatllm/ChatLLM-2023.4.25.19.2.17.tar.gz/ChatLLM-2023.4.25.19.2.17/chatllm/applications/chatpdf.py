#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ChatPDF
# @Time         : 2023/4/21 11:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from chatllm.applications import ChatBase
from meutils.pipe import *


class ChatPDF(ChatBase):

    def __init__(self, chat_func):
        super().__init__(chat_func)

    def qa(self, query, knowledge_base='', **kwargs):
        """可重写"""
        return self._qa(query, knowledge_base, **kwargs)

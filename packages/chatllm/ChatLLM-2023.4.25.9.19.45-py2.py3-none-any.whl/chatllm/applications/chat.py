#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : Question2Answer
# @Time         : 2023/4/21 12:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import types
from meutils.pipe import *
from meutils.decorators import clear_cuda_cache


class Chat(object):

    def __init__(self, chat_func, prompt_template=None):
        self.chat_func = chat_func

        self.history = []
        self.knowledge_base = None

        self.prompt_template = prompt_template
        if prompt_template is None:
            self.prompt_template = self.default_document_prompt

    def __call__(self, **kwargs):
        return self.qa(**kwargs)

    @abstractmethod  # 重写
    def qa(self, query, knowledge_base='', **kwargs):
        return self._qa(query, knowledge_base, **kwargs)

    @clear_cuda_cache
    def _qa(self, query, knowledge_base='', max_turns=1):
        if knowledge_base:
            self.knowledge_base = knowledge_base
            query = self.prompt_template.format(context=knowledge_base, question=query)

        result = self.chat_func(query=query, history=self.history[-max_turns:])

        if isinstance(result, types.GeneratorType):
            return self._stream(result)
        else:  # list(self._stream(result)) 想办法合并
            response, history = result
            # self.history_ = history  # 历史所有
            self.history += [[None, response]]  # 置空知识

        return response

    def _stream(self, result):  # yield > return
        response = None
        for response, history in tqdm(result, desc='Stream', ascii=True, ncols=100):
            yield response, history
        # self.history_ = history  # 历史所有
        self.history += [[None, response]]  # 置空知识

    @property
    def default_document_prompt(self):
        prompt_template = """
            基于以下已知信息，简洁和专业的来回答用户的问题。
            如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文。
            已知内容: {context}
            问题: {question}
            """.strip()

        return prompt_template

    def set_chat_kwargs(self, **kwargs):
        self.chat_func = partial(self.chat_func, **kwargs)


if __name__ == '__main__':
    from chatllm.utils import llm_load4chat

    chat_func = llm_load4chat(
        model_name_or_path="/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm",
        device='mps')

    qa = Chat(chat_func=chat_func)

    for i, _ in qa(query='提取关键词', knowledge_base='我今天去听了周杰伦的演唱会'):
        print(i, flush=True)

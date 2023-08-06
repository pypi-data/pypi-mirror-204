#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ann4qa
# @Time         : 2023/4/24 18:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from chatllm.applications import Chat


class ANN4QA(Chat):

    def __init__(self, chat_func):
        super().__init__(chat_func)

    # def qa(self, query, knowledge_base='', **kwargs):
    #     pass


if __name__ == '__main__':
    from chatllm.utils import llm_load4chat

    chat_func = llm_load4chat(
        model_name_or_path="/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm",
        device='mps',
    )

    qa = ANN4QA(chat_func=chat_func)

    for i, _ in qa(query='1+1'):
        print(i)

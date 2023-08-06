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
from meutils.docarray_ import DocumentArray
from meutils.decorators import clear_cuda_cache
from meutils.request_utils.crawler import Crawler


class Question2Answer(object):

    def __init__(self, chat_func, prompt_template=None):
        self.chat_func = chat_func
        # self.query_embedd = lru_cache()(query_embedd)  # 缓存
        # self.docs = docs

        self.history = []

        self.prompt_template = prompt_template
        if prompt_template is None:
            self.prompt_template = self.default_document_prompt

    def crawler4qa(self, query,
                   url="https://top.baidu.com/board?tab=realtime",
                   xpath='//*[@id="sanRoot"]/main/div[2]/div/div[2]/div[*]/div[2]/a/div[1]//text()'
                   ):
        knowledge_base = Crawler(url).xpath(xpath)

        return self.qa(query, knowledge_base)

    def ann4qa(self, query, max_turns=1, topk=3, query_embedd, da: DocumentArray):

        # ann召回知识
        v = query_embedd(query)
        knowledge_base = da.find(v, topk=topk)[0].texts  # [:, ('text', 'scores__cosine__value')]

        return self.qa(query, knowledge_base, max_turns=max_turns)

    @clear_cuda_cache
    def qa(self, query, knowledge_base='', max_turns=1):
        if knowledge_base:
            query = self.prompt_template.format(context=knowledge_base, question=query)

        result = self.chat_func(query=query, history=self.history[-max_turns:])
        response = history = None
        if isinstance(result, types.GeneratorType):
            for response, history in tqdm(result, desc='Stream'):
                yield response, history
        else:
            response, history = result

        self.history = history  # 历史所有
        return response

    @property
    def default_document_prompt(self):
        prompt_template = """
            基于以下已知信息，简洁和专业的来回答用户的问题。
            如果无法从中得到答案，请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文。
            已知内容:
            {context}
            问题:
            {question}
            """.strip()

        return prompt_template

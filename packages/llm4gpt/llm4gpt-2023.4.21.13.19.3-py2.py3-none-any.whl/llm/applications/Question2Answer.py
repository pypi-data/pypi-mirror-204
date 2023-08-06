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


class Question2Answer(object):

    def __init__(self, chat_func, query_embedd, docs: DocumentArray, prompt_template=None):
        self.chat_func = chat_func
        self.query_embedd = lru_cache()(query_embedd)  # 缓存
        self.docs = docs

        self.history = []

        self.prompt_template = prompt_template
        if prompt_template is None:
            self.prompt_template = self.default_document_prompt

    def __call__(self, *args, **kwargs):
        return self.qa(*args, **kwargs)

    @clear_cuda_cache
    def qa(self, query, topk=3, max_turns=1, return_source_documents=True):

        v = self.query_embedd(query)
        context = self.docs.find(v, topk=topk).texts  # [:, ('text', 'scores__cosine__value')]
        query = self.prompt_template.format(context=context, question=query)

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

from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens

# ME
from meutils.pipe import *
from llm.utils import cuda_empty_cache


class ChatLLM(LLM):
    """
    from llm.utils import llm_load

    model, tokenizer = llm_load("/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")
    glm = ChatLLM()
    # glm.chat_func = partial(model.chat, tokenizer=tokenizer)
    glm.chat_func = partial(model.stream_chat, tokenizer=tokenizer)


    """
    chat_func: Callable = None
    history = []
    max_turns = 3

    @property
    def _llm_type(self) -> str:
        return "ChatLLM"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        cuda_empty_cache()  # todo: 减少调用次数

        response, _ = self.chat_func(query=prompt, history=self.history[-self.max_turns:])
        if stop:
            response = enforce_stop_tokens(response, stop)
        self.history += [(None, response)]
        return response

    def set_chat_kwargs(self, **kwargs):
        self.chat_func = partial(self.chat_func, **kwargs)


if __name__ == '__main__':
    from llm.utils import llm_load

    model, tokenizer = llm_load("/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm")
    glm = ChatLLM()
    # glm.chat_func = partial(model.chat, tokenizer=tokenizer)
    glm.chat_func = partial(model.stream_chat, tokenizer=tokenizer)

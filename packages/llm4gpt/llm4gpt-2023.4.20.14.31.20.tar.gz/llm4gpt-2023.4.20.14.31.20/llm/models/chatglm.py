from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens

# ME
from meutils.pipe import *
from llm.utils import cuda_empty_cache, llm_load


class ChatGLM(LLM):

    def __init__(self, model_name_or_path="THUDM/chatglm-6b", device='cpu', device_map: Optional[Dict[str, int]] = None,
                 history=None, max_turns=3,
                 *args, **kwargs):
        self.max_turns = max(max_turns, 1)
        self.history = history if history is not None else []

        self.model, tokenizer = llm_load(model_name_or_path, device, device_map)

        self.model.chat = partial(self.model.chat, tokenizer=tokenizer)
        self.model.stream_chat = partial(self.model.stream_chat, tokenizer=tokenizer)

        super().__init__(*args, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "ChatGLM"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        cuda_empty_cache()  # todo: 减少调用次数

        response, _ = self.model.chat(query=prompt, history=self.history[-self.max_turns:])
        if stop:
            response = enforce_stop_tokens(response, stop)
        self.history += [(None, response)]
        return response

    def set_chat_kwargs(self, **kwargs):
        self.model.chat = partial(self.model.chat, **kwargs)
        self.model.stream_chat = partial(self.model.stream_chat, **kwargs)

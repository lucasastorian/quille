import anthropic
from typing import List, Optional
from abc import ABC, abstractmethod

from schema import Message, Document
from assistant.actions.base.base_parser import BaseParser
from assistant.utils.prompt_formatter import PromptFormatter


class BaseAction(ABC):

    name: str
    assistant_prefix: Optional[str] = None
    stop_sequences: List[str] = None

    def __init__(self, response_id: str, document: Document, messages: List[Message], sse,
                 model: str = "claude-3-haiku-20240307", temperature: float = 0.25):
        self.response_id = response_id
        self.document = document
        self.document_id = document['id']
        self.messages = messages
        self.sse = sse
        self.model = model
        self.temperature = temperature

        self.client = anthropic.AsyncAnthropic()
        self.prompt_formatter = PromptFormatter(messages=messages)

        assert self.name, "Name must be defined for an action"

    @abstractmethod
    async def call(self):
        """Calls a particular action"""
        raise NotImplementedError

    async def _call_anthropic(self, system_prompt: str, parser: BaseParser) -> Message:
        """Makes an API call to Anthropic"""
        prompt = self.prompt_formatter.format()
        if self.assistant_prefix:
            prompt += [{"role": "assistant", "content": self.assistant_prefix}]

        parameters = {
            "model": self.model,
            "system": system_prompt,
            "max_tokens": 4096,
            "messages": prompt,
            "stop_sequences": self.stop_sequences
        }

        completion = self.assistant_prefix or ""
        async with self.client.messages.stream(**parameters) as stream:
            async for chunk in stream.text_stream:
                completion += chunk
                await parser.stream(completion=completion)

        if self.stop_sequences:
            completion += self.stop_sequences[0]

        message = await parser.complete(completion=completion)

        return message

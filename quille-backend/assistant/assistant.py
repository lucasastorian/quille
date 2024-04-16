import json
import logging
import traceback
from typing import List
from aiohttp_sse.helpers import _ContextManager

from schema import Message, Document
from assistant.router.router import Router
from assistant.router.prompts.new_document import NewDocumentPrompt


class Assistant:

    def __init__(self, messages: List[Message], document: Document, model: str = "claude-3-haiku-20240307"):
        self.messages = messages
        self.document = document
        self.document_id = document['id']
        self.model = model

    async def call(self, sse_queue: _ContextManager):
        """Streams a completion back to the client"""
        try:
            num_iter = 0
            while num_iter < 3:
                await self.step(sse_queue=sse_queue)
                num_iter += 1

                if self.complete():
                    break

            print("Sending complete")
            # await self._on_complete(sse_queue=sse_queue)

        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(e)

    async def step(self, sse_queue: _ContextManager):
        """Completes a single step of the assistant"""
        router = Router(document=self.document, messages=self.messages, sse_queue=sse_queue, model=self.model)
        system_prompt = NewDocumentPrompt().format()
        await router.route(system_prompt=system_prompt)

    def complete(self) -> bool:
        """Returns True if the assistant has completed"""
        return self.messages[-1].get("action") != "web-search-results"

    @staticmethod
    async def _on_complete(sse_queue: _ContextManager):
        """Helper function to push data to redis and convert it to JSON."""
        await sse_queue.send(json.dumps({"name": "Complete", "body": {}}))

    @staticmethod
    async def _on_failed(sse_queue: _ContextManager):
        """Helper function to push data to redis and convert it to JSON."""
        await sse_queue.send(json.dumps({"name": "Failed", "body": {}}))

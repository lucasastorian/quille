import uuid
import anthropic
from typing import List
from functools import partial
from aiohttp_sse.helpers import _ContextManager

from schema import Message, Document
from assistant.actions.base.base_action import BaseAction
from assistant.utils.prompt_formatter import PromptFormatter
from assistant.actions import CreateDocumentAction, CreateOutlineAction, InquireAction, WebSearchAction


class Router:

    def __init__(self, document: Document, messages: List[Message], sse_queue: _ContextManager,
                 model: str = "claude-3-haiku-20240307", temperature: float = 0.25):
        self.document = document
        self.messages = messages
        self.sse_queue = sse_queue
        self.model = model
        self.temperature = temperature
        self.client = anthropic.AsyncAnthropic()
        self.prompt_formatter = PromptFormatter(messages=messages)

    async def route(self, system_prompt: str):
        """Routes the message to an action and executes that action"""
        actions = self.available_actions()
        action_name = await self._choose_action(system_prompt=system_prompt, actions=actions)
        action = next((action for action in actions if action.name == action_name), None)

        if action is not None:
            await action.call()
        else:
            raise ValueError(f"No action found with name '{action_name}'")

    def available_actions(self) -> List[BaseAction]:
        """Returns a list of available actions"""
        response_id = str(uuid.uuid4())
        parameters = {
            "response_id": response_id,
            "document": self.document,
            "messages": self.messages,
            "sse": self.sse_queue,
            "model": self.model,
            "temperature": self.temperature
        }

        actions = [CreateDocumentAction, CreateOutlineAction, InquireAction, WebSearchAction]

        create_action = partial(lambda action: action(**parameters))
        return [create_action(action) for action in actions]

    async def _choose_action(self, system_prompt: str, actions: List[BaseAction]):
        """Chooses a specific action to route to"""
        prompt = self.prompt_formatter.format() + [{"role": "assistant", "content": "<"}]

        resp = await self.client.messages.create(
            model="claude-3-haiku-20240307",  # Router model is hardcoded for maximum speed.
            max_tokens=20,
            system=system_prompt,
            messages=prompt,
            stop_sequences=[">"]
        )

        available_action_names = [action.name for action in actions]
        action = resp.content[0].text

        assert action in available_action_names, f"Action {action} not found in available actions"

        return action

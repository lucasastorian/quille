from assistant.actions.base.base_action import BaseAction
from assistant.actions.inquire.prompt import InquirePrompt
from assistant.actions.inquire.parser import InquireParser


class InquireAction(BaseAction):

    name: str = "inquire"
    assistant_prefix = "<message>"
    stop_sequences = ["</inquiry>"]

    async def call(self):
        """Calls the create-outline action"""
        system_prompt = InquirePrompt().format()
        parser = InquireParser(response_id=self.response_id, document_id=self.document_id, sse=self.sse)
        message = await self._call_anthropic(system_prompt=system_prompt, parser=parser)
        self.messages.append(message)

from assistant.actions.base.base_action import BaseAction
from assistant.actions.create_outline.parser import CreateOutlineParser
from assistant.actions.create_outline.prompt import CreateOutlinePrompt


class CreateOutlineAction(BaseAction):

    name: str = "create-outline"
    assistant_prefix = "<message>"
    stop_sequences = ["</outline>"]

    async def call(self):
        """Calls the create-outline action"""
        system_prompt = CreateOutlinePrompt().format()
        parser = CreateOutlineParser(response_id=self.response_id, document_id=self.document_id, sse=self.sse)
        message = await self._call_anthropic(system_prompt=system_prompt, parser=parser)
        self.messages.append(message)

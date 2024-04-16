from assistant.actions.base.base_action import BaseAction
from assistant.actions.create_document.parser import CreateDocumentParser
from assistant.actions.create_document.prompt import CreateDocumentPrompt


class CreateDocumentAction(BaseAction):

    name: str = "write-document"
    assistant_prefix = "<message>"
    stop_sequences = ["</document>"]

    async def call(self):
        """Calls the create-document action"""
        system_prompt = CreateDocumentPrompt().format()
        parser = CreateDocumentParser(response_id=self.response_id, document_id=self.document_id, sse=self.sse)
        message = await self._call_anthropic(system_prompt=system_prompt, parser=parser)
        self.messages.append(message)

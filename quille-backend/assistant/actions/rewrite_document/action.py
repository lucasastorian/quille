from assistant.actions.base.base_action import BaseAction
from assistant.actions.rewrite_document.prompt import RewriteDocumentPrompt
from assistant.actions.rewrite_document.parser import RewriteDocumentParser


class RewriteDocumentAction(BaseAction):
    name: str = "rewrite-document"
    assistant_prefix = "<message>"
    stop_sequences = ["</document>"]

    async def call(self):
        """Calls the create-document action"""
        system_prompt = RewriteDocumentPrompt(document=self.document).format()
        parser = RewriteDocumentParser(response_id=self.response_id, document_id=self.document_id, sse=self.sse)
        message = await self._call_anthropic(system_prompt=system_prompt, parser=parser)
        self.messages.append(message)

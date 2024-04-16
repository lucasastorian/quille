import re
from assistant.actions.base.base_parser import BaseParser

from schema import Document, Message
from assistant.utils.html_converter import convert_markdown_content_to_html


class RewriteDocumentParser(BaseParser):

    async def stream(self, completion: str) -> Message:
        """Parses and streams a completion to the client"""
        content = self._message_content(completion=completion)

        message = self._get_message(content=content)
        document = self._parse_document(completion=completion)
        print(document)

        await self._stream_message(message=message)
        await self._stream_document(document=document)

        return message

    async def complete(self, completion: str) -> Message:
        """Streams the 'Message' with the 'Completed' status"""
        content = self._message_content(completion=completion)
        message = self._get_message(content=content, status="Completed")
        await self._stream_message(message=message)

        return message

    def _parse_document(self, completion: str) -> Document:
        """Parses the document from the raw XML completion"""
        match = re.search(r"<document>(.*?)</document>|<document>(.*)", completion, re.DOTALL)
        document_str = match.group(1) or match.group(2) if match else None

        if document_str is None:
            return self._get_document(name=None, content=None)

        match = re.search(r"<name>(.*?)</name>|<name>(.*)", completion, re.DOTALL)
        name = match.group(1) or match.group(2) if match else None

        match = re.search(r"<content>(.*?)</content>|<content>(.*)", completion, re.DOTALL)
        content = match.group(1) or match.group(2) if match else None

        if content is not None:
            content = convert_markdown_content_to_html(content=content)

        return self._get_document(name=name, content=content)

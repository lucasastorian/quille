import re
import json
from abc import ABC, abstractmethod
from typing import Literal, Optional

from utils.utils import now
from schema import Message, Document


class BaseParser(ABC):
    """The parser class parses XML and streams it to the client"""

    def __init__(self, response_id: str, document_id: str, sse):
        self.response_id = response_id
        self.document_id = document_id
        self.sse = sse

    @abstractmethod
    async def stream(self, completion: str) -> Message:
        """Parses and streams a completion to the client"""
        raise NotImplementedError

    @abstractmethod
    async def complete(self, completion: str) -> Message:
        """Streams the 'Message' object with status 'Completed"""
        raise NotImplementedError

    @staticmethod
    def _message_content(completion: str) -> Optional[str]:
        """Uses regex to extract the message content"""
        match = re.search(r"<message>(.*?)<|<message>(.*)", completion, re.DOTALL)
        return match.group(1) or match.group(2) if match else None

    def _get_message(self, content: str, status: Literal['InProgress', 'Completed'] = 'InProgress') -> Message:
        """Returns a message object"""
        return Message(id=self.response_id, date=now(), action=None, hidden=False, role="Assistant",
                       status=status, content=content, inquire=None, outline=None, web_search_query=None,
                       web_search_results=None, created_at=now(), updated_at=now())

    def _get_document(self, name: Optional[str], content: Optional[str]) -> Document:
        """Returns a Document Object"""
        return Document(id=self.document_id, name=name, content=content, created_at=now(), updated_at=now())

    async def _stream_message(self, message: Message):
        """Streams the message to the client"""
        await self.sse.send(json.dumps({"name": "Message", "body": message}))

    async def _stream_document(self, document: Document):
        """Streams the document to the client"""
        await self.sse.send(json.dumps({"name": "Document", "body": document}))

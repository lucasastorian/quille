import re
from typing import Optional
from assistant.actions.base.base_parser import BaseParser

from schema import Inquire, Message


class InquireParser(BaseParser):

    async def stream(self, completion: str) -> Message:
        """Streams the outline back to the client"""
        content = self._message_content(completion=completion)
        message = self._get_message(content=content)

        message['action'] = "inquire"
        message['inquire'] = self._parse_inquiry(completion=completion)

        await self._stream_message(message=message)

        print(message)
        return message

    async def complete(self, completion: str) -> Message:
        """Streams the 'Message' with the 'Completed' status"""
        content = self._message_content(completion=completion)
        message = self._get_message(content=content, status="Completed")

        message['action'] = "inquire"
        message['inquire'] = self._parse_inquiry(completion=completion)

        print(message)
        await self._stream_message(message=message)

        return message

    @staticmethod
    def _parse_inquiry(completion: str) -> Optional[Inquire]:
        """Parses the inquiry"""
        inquiry = Inquire(question="", options=[], allows_input=False, input_label="", input_placeholder="")

        # Parse question
        match = re.search(r"<question>(.*?)</question>|<question>(.*)", completion, re.DOTALL)
        if match:
            inquiry["question"] = match.group(1) or match.group(2)

        # Parse options
        options = re.findall(r"<option>(.*?)</option>", completion)
        inquiry["options"] = options

        # Parse allows_input
        match = re.search(r"<allowsInput>(.*?)</allowsInput>", completion)
        if match:
            inquiry["allows_input"] = match.group(1).lower() == "true"

        # Parse input_label
        match = re.search(r"<inputLabel>(.*?)</inputLabel>", completion)
        if match:
            inquiry["input_label"] = match.group(1)

        # Parse input_placeholder
        match = re.search(r"<inputPlaceholder>(.*?)</inputPlaceholder>", completion)
        if match:
            inquiry["input_placeholder"] = match.group(1)

        return inquiry

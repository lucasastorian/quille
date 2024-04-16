import re
from typing import Optional
from assistant.actions.base.base_parser import BaseParser

from schema import Outline, Message


class CreateOutlineParser(BaseParser):

    async def stream(self, completion: str) -> Message:
        """Streams the outline back to the client"""
        print(completion)
        print("---------------------------------------------")
        content = self._message_content(completion=completion)
        message = self._get_message(content=content)

        message['action'] = "create-outline"
        message['outline'] = self._parse_outline(completion=completion)

        await self._stream_message(message=message)

        return message

    async def complete(self, completion: str) -> Message:
        """Streams the 'Message' with the 'Completed' status"""
        content = self._message_content(completion=completion)
        message = self._get_message(content=content, status="Completed")

        message['action'] = "create-outline"
        message['outline'] = self._parse_outline(completion=completion)

        await self._stream_message(message=message)

        return message

    @staticmethod
    def _parse_outline(completion: str) -> Optional[Outline]:
        """Parses the XML outline into an 'Outline' object"""
        sections = re.findall(r"<section>(.*?)</section>|<section>(.*)", completion, re.DOTALL)
        if not sections:
            return None

        sections = [section[0] or section[1] for section in sections]

        parsed_sections = []
        for section in sections:
            title_match = re.search(r"<title>(.*?)</title>|<title>(.*)", section, re.DOTALL)
            title = title_match.group(1) or title_match.group(2) if title_match else ""
            title = title.strip().strip("\n")

            subsections = re.findall(r"<subsection>(.*?)</subsection>|<subsection>(.*)", section, re.DOTALL)
            subsections = [subsection[0] or subsection[1] for subsection in subsections]

            parsed_subsections = [{"title": subsection.strip().strip("\n")} for subsection in subsections]

            parsed_sections.append({"title": title, "subsections": parsed_subsections})

        return {"sections": parsed_sections}

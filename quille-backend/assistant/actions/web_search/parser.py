import re
from typing import Optional, List
from assistant.actions.base.base_parser import BaseParser

from schema import Message, WebSearch, WebSearchQuery


class WebSearchQueryParser(BaseParser):

    async def stream(self, completion: str) -> Message:
        """Streams the outline back to the client"""
        content = self._message_content(completion=completion)
        message = self._get_message(content=content)

        message['action'] = 'search-web'
        message['web_search_query'] = self._parse_search_questions(completion=completion)

        await self._stream_message(message=message)

        return message

    async def complete(self, completion: str) -> Message:
        """Streams the 'Message' with the 'Completed' status"""
        content = self._message_content(completion=completion)
        message = self._get_message(content=content, status="Completed")

        message['action'] = 'search-web'
        message['web_search_query'] = self._parse_search_questions(completion=completion)

        await self._stream_message(message=message)

        return message

    @staticmethod
    def _parse_search_questions(completion: str) -> Optional[WebSearch]:
        """Parses the inquiry"""
        questions = re.findall(r"<questions>(.*?)</questions>|<questions>(.*)", completion, re.DOTALL)

        if not questions:
            return None

        questions = [question[0] or question[1] for question in questions]

        parsed_queries: List[WebSearchQuery] = []
        for question in questions:
            question_match = re.search(r"<question>(.*?)</question>|<question>(.*)", question, re.DOTALL)
            question = question_match.group(1) or question_match.group(2) if question_match else ""
            question = question.strip().strip("\n")

            parsed_queries.append({"query": question})

        return {"queries": parsed_queries}

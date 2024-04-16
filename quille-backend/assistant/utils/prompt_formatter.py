from typing import List
from anthropic.types.message import Message as AnthropicMessage

from schema import Message


class PromptFormatter:

    def __init__(self, messages: list[Message]):
        self.messages = messages

    def format(self) -> List[dict]:
        """Formats the Prompt for Anthropic"""
        prompt = []
        for message in self.messages:
            role = message['role'].lower()

            if message.get("inquire"):
                content = self._format_inquire(message=message)

            elif message.get("outline"):
                content = self._format_outline(message=message)

            elif message.get("web_search_query"):
                content = self._format_web_search_query(message=message)

            elif message.get("web_search_results"):
                role = "user"  # reformat tool message as a user message
                content = self._format_web_search_results(message=message)

            elif message.get("content"):
                content = message['content']

            else:
                raise ValueError("Message must have an outline, content, or inquire key")

            prompt.append({"role": role, "content": content})

        return prompt

    @staticmethod
    def _format_inquire(message: Message) -> str:
        """Formats the inquire message action"""
        inquire = message['inquire']
        content = f"{inquire['question']}\n"

        if inquire.get("options"):
            content += "\n - ".join(inquire['options'])

        if inquire.get("allows_input"):
            content += f"\n{inquire['input_label']}: {inquire['input_placeholder']}"

        return content

    @staticmethod
    def _format_web_search_query(message: Message) -> str:
        """Formats the web search query action"""
        queries = message['web_search_query']['queries']
        content = f"{message['content']}\n"

        for query in queries:
            content += f"- {query['query']}\n"

        return content

    @staticmethod
    def _format_web_search_results(message: Message) -> str:
        """Formats the results from a web search query"""
        search_results = message['web_search_results']['results']
        content = ""

        for result in search_results:
            content += f"<search-result>#{result['title']} ({result['url']})\n{result['text']}</search-result>\n"

        return content

    @staticmethod
    def _format_outline(message: Message):
        """Formats the outline"""
        outline = message['outline']
        content = f"{message['content']}\n"

        for i, section in enumerate(outline['sections'], start=1):
            content += f"{section['title']}\n"

            for j, subsection in enumerate(section.get("subsections", []), start=1):
                content += f"    - {subsection['title']}\n"

        return content

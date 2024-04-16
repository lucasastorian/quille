import json
import uuid
from typing import List

from utils.utils import now
from schema import Message, WebSearchResults, WebSearchResult
from assistant.actions.base.base_action import BaseAction
from assistant.actions.web_search.prompt import WebSearchQueryPrompt
from assistant.actions.web_search.parser import WebSearchQueryParser
from assistant.actions.web_search.tavily_web_search import TavilyWebSearch


class WebSearchAction(BaseAction):

    name: str = "search-web"
    assistant_prefix = "<message>"
    stop_sequences = ["</questions>"]

    async def call(self):
        """Calls the create-outline action"""
        system_prompt = WebSearchQueryPrompt().format()
        parser = WebSearchQueryParser(response_id=self.response_id, document_id=self.document_id, sse=self.sse)
        message = await self._call_anthropic(system_prompt=system_prompt, parser=parser)
        print("web search query message")
        print(message)
        self.messages.append(message)

        questions = [query['query'] for query in message['web_search_query']['queries']]
        tavily_search = TavilyWebSearch(queries=questions)
        search_results = await tavily_search.search()

        message = await self._log_and_stream_search_result_as_tool_message(results=search_results)
        self.messages.append(message)

    async def _log_and_stream_search_result_as_tool_message(self, results: List[WebSearchResult]) -> Message:
        """Logs and streams the message to the client"""
        message = Message(id=str(uuid.uuid4()), date=now(), action="web-search-results", hidden=False, role="Tool",
                          status="Completed", content=None, inquire=None, outline=None, web_search_query=None,
                          web_search_results=WebSearchResults(results=results), created_at=now(), updated_at=now())

        await self._stream_message(message=message)

        return message

    async def _stream_message(self, message: Message):
        """Streams the inquiry to the client"""
        payload = json.dumps({"name": "Message", "body": message})
        print(payload)
        await self.sse.send(json.dumps({"name": "Message", "body": message}))

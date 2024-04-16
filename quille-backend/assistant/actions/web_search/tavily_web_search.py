import os
import aiohttp
import asyncio
from typing import List, Literal

from schema import WebSearchResult


class TavilyWebSearch:
    """Class for running asynchronous queries with Tavily"""

    include_raw_content: bool = False

    def __init__(self, queries: List[str], max_results: int = 10, search_depth: Literal['basic', 'advanced'] = 'basic'):
        self.queries = queries
        self.max_results = max_results
        self.search_depth = search_depth

    async def search(self) -> List[WebSearchResult]:
        """Runs one or more asynchronous queries of the web"""
        async with aiohttp.ClientSession() as session:
            tasks = [self._search_with_tavily(query=query, session=session) for query in self.queries]
            results = await asyncio.gather(*tasks)

            results = [item for sublist in results for item in sublist]

            unique_results = list({item['content']: item for item in results}.values())

            results = [
                {"query": result['query'], "title": result['title'], "url": result['url'], "text": result['content']}
                for result in unique_results]

            return results

    async def _search_with_tavily(self, query: str, session: aiohttp.ClientSession) -> List[dict]:
        """Executes a single search with Tavily"""
        body = {"api_key": os.environ['TAVILY_API_KEY'], "query": query,
                "search_depth": str(self.search_depth), "max_results": str(self.max_results),
                "include_raw_content": self.include_raw_content}

        async with session.post("https://api.tavily.com/search", json=body) as response:
            if response.status == 200:
                data = await response.json()

                results = data['results']
                [result.update({"query": query}) for result in results]

                return results

            else:
                raise ValueError("Could not execute search")

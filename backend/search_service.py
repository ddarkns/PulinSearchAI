import os
import asyncio
import httpx
import trafilatura
from tavily import TavilyClient

class SearchService:
    def __init__(self):
        self.tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    async def fetch_and_extract(self, url: str, client: httpx.AsyncClient):
        """Asynchronously fetches and cleans a single webpage."""
        try:
            # 10s timeout prevents one slow site from hanging the whole app
            response = await client.get(url, timeout=10.0, follow_redirects=True)
            if response.status_code == 200:
                # trafilatura is synchronous, so we run it in a separate thread
                return await asyncio.to_thread(trafilatura.extract, response.text, include_comments=False)
        except Exception:
            return None
        return None

    async def web_search(self, query: str):
        """Finds URLs and scrapes them all in parallel."""
        # 1. Get URLs from Tavily (Sync call)
        response = self.tavily_client.search(query, max_results=10)
        search_results = response.get('results', [])
        
        # 2. Scrape all URLs in parallel using httpx
        async with httpx.AsyncClient(headers={"User-Agent": "PulinSearchAI/1.0"}) as client:
            tasks = [self.fetch_and_extract(res['url'], client) for res in search_results]
            contents = await asyncio.gather(*tasks)

        # 3. Combine results
        final_results = []
        for res, content in zip(search_results, contents):
            if content:
                final_results.append({
                    'title': res.get('title', ''),
                    'url': res.get('url'),
                    'content': content
                })
        return final_results
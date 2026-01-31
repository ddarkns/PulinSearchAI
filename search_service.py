import os
from typing import Literal, List
from tavily import TavilyClient

import trafilatura

class SearchService:
    def __init__(self):
        self.tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


    # --- Normal Search Method ---
    def web_search(self, query: str):
        results = []
        response = self.tavily_client.search(query, max_results=10)
        search_results = response.get('results', [])
        for result in search_results:
            page_content = trafilatura.fetch_url(result.get('url'))
            ans = trafilatura.extract(page_content, include_comments=False)
            results.append({
                'title': result.get('title', ''),
                "url": result.get("url"),
                "content": ans
            })
        return results


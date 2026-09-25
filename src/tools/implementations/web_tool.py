from typing import Dict, Any
import urllib.request
import urllib.parse
import json
import re
from pydantic import BaseModel, Field
from src.tools.base import BaseTool
from src.utils.logger import logger

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Searches the web for up-to-date information, facts, or answers using DuckDuckGo."

    class ToolInput(BaseModel):
        query: str = Field(..., description="The search query string.")

    input_schema = ToolInput

    def _run(self, args: Dict[str, Any]) -> str:
        query = args.get("query")
        if not query:
            return "Error: The 'query' parameter is missing from the request."

        results = []
        # 1. Try DuckDuckGo Instant Answer API (Fastest/cleanest)
        try:
            api_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                abstract = data.get("AbstractText")
                if abstract:
                    results.append(f"Summary: {abstract}")
                
                related = data.get("RelatedTopics", [])
                for topic in related[:5]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append(f"- {topic['Text']}")
        except Exception as e:
            logger.warning(f"DuckDuckGo API failed for '{query}': {e}")

        # 2. Fallback to DuckDuckGo Lite (If no results from API or network issues)
        if not results:
            try:
                lite_url = "https://lite.duckduckgo.com/lite/"
                form_data = urllib.parse.urlencode({"q": query}).encode("utf-8")
                req = urllib.request.Request(lite_url, data=form_data, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    html = resp.read().decode("utf-8")
                    # Extract snippets and titles using regex
                    snippets = re.findall(r'<td class="result-snippet"[^>]*>(.*?)<\/td>', html, re.DOTALL)
                    titles = re.findall(r'<a class="result-link"[^>]*>(.*?)<\/a>', html, re.DOTALL)
                    
                    for i in range(min(len(titles), len(snippets), 5)):
                        clean_title = re.sub(r'<[^>]+>', '', titles[i]).strip()
                        clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
                        if clean_title or clean_snippet:
                            results.append(f"- {clean_title}: {clean_snippet}")
            except Exception as e:
                logger.warning(f"DuckDuckGo Lite failed for '{query}': {e}")

        if not results:
            return f"No search results found for query: '{query}'."

        return "\n".join(results)

from src.tools.registry import registry
registry.register(WebSearchTool())

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
            return "Error: Query cannot be empty."

        results = []
        try:
            # 1. Try DuckDuckGo Instant Answer API
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
            logger.warning(f"DuckDuckGo API search failed: {e}")

        # 2. If API didn't yield enough results, query DuckDuckGo Lite HTML
        if not results:
            try:
                lite_url = "https://lite.duckduckgo.com/lite/"
                form_data = urllib.parse.urlencode({"q": query}).encode("utf-8")
                req = urllib.request.Request(lite_url, data=form_data, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    html = resp.read().decode("utf-8")
                    snippets = re.findall(r'<td class="result-snippet"[^>]*>(.*?)<\/td>', html, re.DOTALL)
                    titles = re.findall(r'<a class="result-link"[^>]*>(.*?)<\/a>', html, re.DOTALL)
                    
                    for i in range(min(len(titles), len(snippets), 5)):
                        clean_title = re.sub(r'<[^>]+>', '', titles[i]).strip()
                        clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
                        results.append(f"- {clean_title}: {clean_snippet}")
            except Exception as e:
                logger.warning(f"DuckDuckGo Lite HTML search failed: {e}")

        if not results:
            return f"No search results found for query: '{query}'."

        return "\n".join(results)

from src.tools.registry import registry
registry.register(WebSearchTool())

"""
Search Service - Web Search using Brave Search API

Brave Search API provides free tier: 2000 queries/month
Alternative: SerpAPI (100 searches/month free)
"""

import os
import logging
from typing import Dict, Any, List, Optional
import httpx

from app.config import settings

logger = logging.getLogger(__name__)

# Try Brave Search first, fallback to SerpAPI
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")


class SearchService:
    """
    Web search service using Brave Search or SerpAPI.
    
    Provides real-time web search with result summarization.
    """
    
    def __init__(self):
        """Initialize search service."""
        self.brave_api_key = BRAVE_API_KEY
        self.serpapi_key = SERPAPI_KEY
        self.use_brave = bool(self.brave_api_key)
        self.use_serpapi = bool(self.serpapi_key)
        
        if not self.use_brave and not self.use_serpapi:
            logger.warning("⚠️ No search API keys configured. Search features will be disabled.")
        else:
            logger.info(f"✅ Search service initialized (Brave: {self.use_brave}, SerpAPI: {self.use_serpapi})")
    
    async def search(
        self,
        query: str,
        num_results: int = 5
    ) -> Dict[str, Any]:
        """
        Perform web search.
        
        Args:
            query: Search query
            num_results: Number of results to return (max 20)
            
        Returns:
            Dict with search results and summary
        """
        if not query.strip():
            return {
                "success": False,
                "error": "Search query cannot be empty"
            }
        
        # Limit results
        num_results = min(num_results, 20)
        
        # Try Brave Search first
        if self.use_brave:
            result = await self._search_brave(query, num_results)
            if result.get("success"):
                return result
        
        # Fallback to SerpAPI
        if self.use_serpapi:
            result = await self._search_serpapi(query, num_results)
            if result.get("success"):
                return result
        
        # No API available
        return {
            "success": False,
            "error": "Search API not configured. Please set BRAVE_API_KEY or SERPAPI_KEY."
        }
    
    async def _search_brave(
        self,
        query: str,
        num_results: int
    ) -> Dict[str, Any]:
        """Search using Brave Search API."""
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {
                "q": query,
                "count": num_results,
                "safesearch": "moderate",
                "freshness": "py"  # Past year
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
            
            # Parse results
            results = []
            web_results = data.get("web", {}).get("results", [])
            
            for item in web_results[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", ""),
                    "age": item.get("age", "")
                })
            
            # Generate summary
            summary = self._generate_summary(results, query)
            
            logger.info(f"✅ Brave search: {len(results)} results for '{query}'")
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "summary": summary,
                "total_results": len(results),
                "provider": "brave"
            }
            
        except Exception as e:
            logger.error(f"❌ Brave search error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _search_serpapi(
        self,
        query: str,
        num_results: int
    ) -> Dict[str, Any]:
        """Search using SerpAPI."""
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "num": num_results,
                "engine": "google"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            # Parse results
            results = []
            organic_results = data.get("organic_results", [])
            
            for item in organic_results[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "description": item.get("snippet", ""),
                    "age": ""
                })
            
            # Generate summary
            summary = self._generate_summary(results, query)
            
            logger.info(f"✅ SerpAPI search: {len(results)} results for '{query}'")
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "summary": summary,
                "total_results": len(results),
                "provider": "serpapi"
            }
            
        except Exception as e:
            logger.error(f"❌ SerpAPI search error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_summary(self, results: List[Dict], query: str) -> str:
        """
        Generate a summary of search results.
        
        Args:
            results: List of search results
            query: Original search query
            
        Returns:
            Summary string
        """
        if not results:
            return f"No results found for '{query}'."
        
        # Simple summary: combine top 3 results
        top_results = results[:3]
        summary_parts = [f"Found {len(results)} results for '{query}':\n"]
        
        for i, result in enumerate(top_results, 1):
            title = result.get("title", "Untitled")
            description = result.get("description", "")
            # Truncate description
            if len(description) > 150:
                description = description[:147] + "..."
            
            summary_parts.append(f"{i}. **{title}**\n{description}\n")
        
        if len(results) > 3:
            summary_parts.append(f"\n... and {len(results) - 3} more results.")
        
        return "\n".join(summary_parts)


# Global search service instance
_search_service = None


def get_search_service() -> SearchService:
    """Get or create global search service instance."""
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service

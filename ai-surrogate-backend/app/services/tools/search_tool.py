"""
Search Tool for Agno Agents

Provides web search capability as an Agno tool.
"""

import logging
from typing import Dict, Any
from agno.tools import Toolkit

from app.services.search_service import get_search_service

logger = logging.getLogger(__name__)


class SearchToolkit(Toolkit):
    """
    Web search toolkit for Agno agents.
    
    Provides tools for:
    - Web search with result summarization
    """
    
    name: str = "Web Search Toolkit"
    description: str = "Tools for searching the web and getting real-time information"
    
    def __init__(self):
        """Initialize search toolkit."""
        super().__init__()
        self.search_service = get_search_service()
    
    def search_web(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Args:
            query: Search query
            num_results: Number of results to return (default: 5, max: 20)
            
        Returns:
            Dict with search results and summary
        """
        import asyncio
        
        try:
            # Run async search
            result = asyncio.run(self.search_service.search(query, num_results))
            
            if result.get("success"):
                return {
                    "success": True,
                    "query": result["query"],
                    "summary": result["summary"],
                    "results": result["results"],
                    "total_results": result["total_results"]
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Search failed")
                }
                
        except Exception as e:
            logger.error(f"Search tool error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Create toolkit instance
search_toolkit = SearchToolkit()

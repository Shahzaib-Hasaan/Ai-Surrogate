"""
Tools API routes.

Endpoints for task execution tools:
- POST /api/tools/search - Perform web search
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services.auth_service import get_current_user
from app.services.search_service import get_search_service

router = APIRouter(prefix="/api/tools", tags=["Tools"])


class SearchRequest(BaseModel):
    """Search request model."""
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    num_results: int = Field(5, ge=1, le=20, description="Number of results to return")


@router.post(
    "/search",
    summary="Perform web search",
    description="Search the web using Brave Search or SerpAPI"
)
async def search_web(
    request: SearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Perform web search.
    
    - **query**: Search query (1-500 characters)
    - **num_results**: Number of results (1-20, default: 5)
    
    Returns search results with summary.
    """
    try:
        search_service = get_search_service()
        result = await search_service.search(
            query=request.query,
            num_results=request.num_results
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Search failed")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing search: {str(e)}"
        )

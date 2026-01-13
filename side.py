import os
from typing import List
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from my_agent.utils import express_client


load_dotenv()


class HealthResponse(BaseModel):
    """Response body for the /health endpoint."""
    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")

class testResponse(BaseModel):
    '''Response body from express , i will edit based on what response i'm expecting'''
    success: bool
    message: str
    note: dict
    
class testRequest(BaseModel):
     '''Request body for express , i will edit based on what response i'm sending'''
     title: str 
     content: str 
     userId: str
     categoryId: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    print("server started")
    
    yield
    print("server shutdown")
    



# Create FastAPI app
app = FastAPI(
    title="Dummy server",
    description="Dummy server made for testing",
    version="1.0.0",
    lifespan=lifespan,
)



@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for Render and monitoring.
    """
    return HealthResponse(
        status="healthy",
        service="isolated-dummy-server-the-mage",
        version="1.0.0"
    )


@app.post("/test/", response_model=testResponse)
async def test_express_client(request: testRequest):
    """
    Test endpoint to verify express_client works independently.
    Calls Express's getNotesForAgent endpoint.
    
    Usage: GET /test/your_user_id_here?limit=10
    """
    try:
        # Call Express API (matches agentRoutes.js: GET /api/agent/notes/:userId)
        data = {
            "title": request.title,
            "content": request.content,
            "userId": request.userId,
            "categoryId": request.categoryId
        }
        result = await express_client.post(f"/api/agent/notes/create", data=data)
        
        # Unpack the dict into the Pydantic model
        return testResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Express client error: {str(e)}"
        )


# For local development
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "side:app",  # Changed from "main:app"
        host="0.0.0.0",
        port=port,
        reload=True,
    )

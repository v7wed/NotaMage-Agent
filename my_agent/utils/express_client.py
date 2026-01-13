"""
HTTP client for communicating with the Express.js backend.
"""

import os
import httpx
from typing import Any, Optional


class ExpressClient:
    """
    HTTP client for making authenticated requests to the Express server.
    All agent tools use this client to interact with the backend API.
    """
    
    def __init__(self):
        self.base_url = os.getenv("EXPRESS_SERVICE_URL")
        self.service_secret = os.getenv("SERVICE_SECRET")
        self.timeout = 20.0  
    
    def _get_headers(self) -> dict[str, str]:
        """Get headers with authentication."""
        return {
            "Authorization": f"Bearer {self.service_secret}",
            "Content-Type": "application/json",
        }
    
    async def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Make a GET request to the Express API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                params=params,
            )
            response.raise_for_status()
            return response.json()
    
    async def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Make a POST request to the Express API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
            )
            response.raise_for_status()
            return response.json()
    
    async def put(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Make a PUT request to the Express API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.put(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
            )
            response.raise_for_status()
            return response.json()
    
    async def delete(self, endpoint: str, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Make a DELETE request to the Express API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                "DELETE",
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
            )
            response.raise_for_status()
            return response.json()



express_client = ExpressClient()

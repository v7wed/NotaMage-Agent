"""
Note management tools for The Mage agent.
These tools call the Express API to perform CRUD operations on notes.

Tools use ToolRuntime to access user_id from graph state,
so the LLM doesn't need to pass it as a parameter.
"""

from typing import Optional
from langchain.tools import tool, ToolRuntime
from my_agent.utils.express_client import express_client


@tool
async def get_user_context(runtime: ToolRuntime) -> dict:
    """
    Get a summary of the user's notes and categories.
    Useful for understanding what the user has before taking actions.
    
    Returns:
        Dictionary containing user's note count, category count, recent notes, and category summary
    """
    try:
        user_id = runtime.state["user_id"]
        result = await express_client.get(f"/api/agent/context/{user_id}")
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def get_user_notes(limit: int = 10, runtime: ToolRuntime = None) -> dict:
    """
    Fetch all notes for a user.
    
    Args:
        limit: Maximum number of notes to fetch (default 10)
    
    Returns:
        Dictionary containing the user's notes
    """
    try:
        user_id = runtime.state["user_id"]
        params = {"limit": limit}
        result = await express_client.get(f"/api/agent/notes/{user_id}", params=params)
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def search_user_notes(query: str, limit: int = 10, runtime: ToolRuntime = None) -> dict:
    """
    Search notes by keyword for a user.
    
    Args:
        query: Search term to filter notes by title or content
        limit: Maximum number of results (default 10)
    
    Returns:
        Dictionary containing matching notes
    """
    try:
        user_id = runtime.state["user_id"]
        params = {"q": query, "limit": limit}
        result = await express_client.get(f"/api/agent/notes/{user_id}/search", params=params)
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def create_note(
    title: str,
    content: str,
    category_id: Optional[str] = None,
    runtime: ToolRuntime = None,
) -> dict:
    """
    Create a new note for the user.
    
    Args:
        title: The title of the note
        content: The content/body of the note
        category_id: Optional category ID to assign the note to
    
    Returns:
        Dictionary containing the created note details
    """
    try:
        user_id = runtime.state["user_id"]
        data = {
            "userId": user_id,
            "title": title,
            "content": content,
        }
        if category_id:
            data["categoryId"] = category_id
        
        result = await express_client.post("/api/agent/notes/create", data)
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def create_multiple_notes(
    notes: list[dict],
    runtime: ToolRuntime = None,
) -> dict:
    """
    Create multiple notes at once for the user.
    
    Args:
        notes: List of note objects, each with 'title', 'content', and optional 'categoryId'
    
    Returns:
        Dictionary containing the created notes details
    """
    try:
        user_id = runtime.state["user_id"]
        data = {
            "userId": user_id,
            "notes": notes,
        }
        result = await express_client.post("/api/agent/notes/batch-create", data)
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def update_note(
    note_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    category_id: Optional[str] = None
) -> dict:
    """
    Update an existing note.
    
    
    Args:
        note_id: The MongoDB note ID to update
        title: New title (optional, keeps existing if not provided)
        content: New content (optional, keeps existing if not provided)
        category_id: Category ID to assign (optional)
    
    Returns:
        Dictionary containing the updated note details
    """
    
    try:
        data = {}
        if title is not None:
            data["title"] = title
        if content is not None:
            data["content"] = content
        if category_id is not None:
            data["categoryId"] = category_id
        
        result = await express_client.put(f"/api/agent/notes/{note_id}", data)
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def delete_note(
    note_id: str
) -> dict:
    """
    Delete a note. 
    

    Args:
        note_id: The MongoDB note ID to delete
    
    Returns:
        Dictionary confirming deletion
    """
    
    try:
        result = await express_client.delete(
            f"/api/agent/notes/{note_id}"
        )
        return result
    except Exception as e:
        return {"error": str(e), "success": False}

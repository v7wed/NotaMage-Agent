"""
Category management tools for The Mage agent.
These tools call the Express API to perform CRUD operations on categories.

Tools use ToolRuntime to access user_id from graph state,
so the LLM doesn't need to pass it as a parameter.
"""

from langchain.tools import tool, ToolRuntime
from my_agent.utils.express_client import express_client


@tool
async def get_user_categories(runtime: ToolRuntime) -> dict:
    """
    Fetch all categories for a user.
    
    Returns:
        Dictionary containing the user's categories
    """
    try:
        user_id = runtime.state["user_id"]
        result = await express_client.get(f"/api/agent/categories/{user_id}")
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def create_category(
    name: str,
    runtime: ToolRuntime = None,
) -> dict:
    """
    Create a new category for the user.
    
    Args:
        name: The name of the category
    
    Returns:
        Dictionary containing the created category details
    """
    try:
        user_id = runtime.state["user_id"]
        data = {
            "userId": user_id,
            "name": name,
        }
        
        result = await express_client.post("/api/agent/categories/create", data)
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def update_category(
    category_id: str,
    name: str,
) -> dict:
    """
    Update an existing category (rename it).
    
    Args:
        category_id: The MongoDB category ID to update
        name: New name for the category
    
    Returns:
        Dictionary containing the updated category details
    """
    try:
        data = {"name": name}
        
        result = await express_client.put(f"/api/agent/categories/{category_id}", data)
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def delete_category(category_id: str) -> dict:
    """
    Delete a category. Notes in this category will become uncategorized.
    
    Args:
        category_id: The MongoDB category ID to delete
    
    Returns:
        Dictionary confirming deletion
    """
    try:
        result = await express_client.delete(f"/api/agent/categories/{category_id}")
        return result
    except Exception as e:
        return {"error": str(e), "success": False}


@tool
async def assign_notes_to_category(
    category_id: str,
    note_ids: list[str],
) -> dict:
    """
    Assign multiple notes to a category.
    
    Args:
        category_id: The MongoDB category ID to assign notes to, "null" to uncategorize
        note_ids: List of note IDs to assign to the category
    
    Returns:
        Dictionary confirming the assignment
    """
    try:
        data = {"noteIds": note_ids}
        result = await express_client.put(
            f"/api/agent/categories/{category_id}/assign",
            data
        )
        return result
    except Exception as e:
        return {"error": str(e), "success": False}

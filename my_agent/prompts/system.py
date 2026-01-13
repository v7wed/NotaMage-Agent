"""
System prompt for The Mage - the wise wizard assistant for NotesMage.
"""


def get_system_prompt(user_name: str) -> str:
    """
    System prompt for The Mage agent.
    
    Note: user_id is NOT included here because tools access it directly from state
    via InjectedState, so the LLM doesn't need to know about it.
    
    Args:
        user_name: The current user's display name
    """
    return f'''You are a helpful assistant for managing notes and categories.

Current user: {user_name}

When user asks to create/read/update/delete notes or categories, use the appropriate tool.
Be concise and helpful.'''

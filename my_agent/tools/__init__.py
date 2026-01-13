"""
Tools for The Mage agent.
"""

from my_agent.tools.notes import (
    get_user_context,
    get_user_notes,
    search_user_notes,
    create_note,
    create_multiple_notes,
    update_note,
    delete_note,
)
from my_agent.tools.categories import (
    get_user_categories,
    create_category,
    update_category,
    delete_category,
    assign_notes_to_category,
)

# All tools available to the agent
all_tools = [
    get_user_context,
    get_user_notes,
    search_user_notes,
    create_note,
    create_multiple_notes,
    update_note,
    delete_note,
    get_user_categories,
    create_category,
    update_category,
    delete_category,
    assign_notes_to_category,
]


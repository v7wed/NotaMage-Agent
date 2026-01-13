"""
State definition for The Mage agent.
"""

from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class MageState(TypedDict):
    """State for The Mage LangGraph agent."""
    
    # Conversation messages with add_messages reducer for proper message handling
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # User context (pre-validated by Express server)
    user_id: str
    user_name: str


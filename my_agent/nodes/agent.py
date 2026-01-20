"""
Agent node for The Mage - the main LLM-powered conversational node.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, AIMessage
from my_agent.state import MageState
from my_agent.prompts import get_system_prompt
from my_agent.tools import all_tools


def is_rate_limit_error(exception: Exception) -> bool:
    """
    Checks if an exception was due to a rate limit error (429).
    Handles various provider-specific exception types.
    """
    error_str = str(exception).lower()
    
    rate_limit_indicators = [
        "429",
        "rate limit",
        "rate_limit",
        "ratelimit",
        "too many requests",
        "quota exceeded",
        "resource exhausted",
        "resourceexhausted",
    ]
    
    for indicator in rate_limit_indicators:
        if indicator in error_str:
            return True
    
    if hasattr(exception, 'status_code') and exception.status_code == 429:
        return True
    
    if hasattr(exception, 'response') and hasattr(exception.response, 'status_code'):
        if exception.response.status_code == 429:
            return True
    
    return False


async def agent_node(state: MageState) -> MageState:
    """
    Main agent node - processes user messages through the LLM with tools.
    
    This node:
    1. Prepends the system prompt
    2. Invokes the LLM with the conversation history
    3. Returns the LLM's response (may include tool calls)
    4. Gracefully handles rate limit errors with a user-friendly message
    
    Note: user_id is accessed by tools via ToolRuntime.state, not passed through prompt.
    
    Args:
        state: The current MageState
    
    Returns:
        Updated state with the agent's response message
    """
    system_message = SystemMessage(content=get_system_prompt())
    messages = [system_message] + list(state["messages"])
    
    try:
        llm = ChatGoogleGenerativeAI(model='gemini-3-flash-preview', temperature=0.7)
        llm_with_tools = llm.bind_tools(all_tools)
        response = await llm_with_tools.ainvoke(messages)
    except Exception as e:
        if is_rate_limit_error(e):
            # Return a professional message explaining this is a demo project
            response = AIMessage(
                content=(
                    "**[429] Daily quota exceeded for this demo**\n\n"
                    "Thank you for visiting NotesMage! This live demo has received more requests than expected today and has reached its free tier quota limit.\n\n"
                    "**Important context:**\n"
                    "- This is an **open-source project** showcasing AI agent architecture and full-stack development\n"
                    "- The live demo runs on limited free-tier resources to demonstrate concept and functionality only\n"
                    "- For production use, NotesMage would utilize paid tiers with significantly higher quotas and better models\n\n"
                    "Please feel free to explore the [source code on GitHub](https://github.com/v7wed/Notamage) or try again tomorrow. "
                    "\n\n"
                    "Thank you for understanding! 🧙‍♂️"
                )
            )
        else:
            # Re-raise non-rate-limit errors
            raise
    
    return {"messages": [response]}

"""
Agent node for The Mage - the main LLM-powered conversational node.
"""
import asyncio
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, AIMessage
from my_agent.state import MageState
from my_agent.prompts import get_system_prompt
from my_agent.tools import all_tools


# Maximum number of providers to try before giving up
MAX_PROVIDERS = 5


def get_llm(judge: int):
    """Get LLM based on judge counter - cycles through providers on rate limits."""
    match judge:
        case 1:
            llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite', temperature=0.7)
        case 2:
            llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.7)
        case 3:
            llm = ChatGoogleGenerativeAI(model='gemini-3-flash', temperature=0.7)
        case 4:
            llm = ChatGroq(model='llama-3.3-70b-versatile', temperature=0.7)
        case _:
            llm = ChatDeepSeek(model='deepseek-chat', temperature=0.7)
    return llm


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
    4. Gracefully handles rate limits by switching to alternate providers
    
    Note: user_id is accessed by tools via ToolRuntime.state, not passed through prompt.
    
    Args:
        state: The current MageState
    
    Returns:
        Updated state with the agent's response message
    """

    
    user_name = state['user_name']
    
    system_message = SystemMessage(content=get_system_prompt(user_name))
    messages = [system_message] + list(state["messages"])
    
    judge = 1
    response = None

    while judge <= MAX_PROVIDERS:
        try:
            llm = get_llm(judge).bind_tools(all_tools)
            response = await llm.ainvoke(messages)
            # Success - break out of the retry loop
            break
        except Exception as e:
            if is_rate_limit_error(e):
                print(f"Rate limit hit on provider {judge}, switching to next provider...")
                judge += 1
                # Small delay before retrying with next provider
                await asyncio.sleep(0.5)
            else:
                # For non-rate-limit errors, re-raise
                raise
    
    # If all providers failed due to rate limits, gracefully returns a friendly message
    if response is None:
        response = AIMessage(
            content="I'm experiencing very high demand right now. Please try again in a different time"
        )
    
    return {"messages": [response]}

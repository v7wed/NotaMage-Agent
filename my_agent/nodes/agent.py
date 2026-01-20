"""
Agent node for The Mage - the main LLM-powered conversational node.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from my_agent.state import MageState
from my_agent.prompts import get_system_prompt
from my_agent.tools import all_tools


async def agent_node(state: MageState) -> MageState:
    """
    Main agent node - processes user messages through the LLM with tools.
    
    This node:
    1. Prepends the system prompt
    2. Invokes the LLM with the conversation history
    3. Returns the LLM's response (may include tool calls)
    
    Note: user_id is accessed by tools via ToolRuntime.state, not passed through prompt.
    
    Args:
        state: The current MageState
    
    Returns:
        Updated state with the agent's response message
    """
    system_message = SystemMessage(content=get_system_prompt())
    messages = [system_message] + list(state["messages"])
    
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.7)
    llm_with_tools = llm.bind_tools(all_tools)
    response = await llm_with_tools.ainvoke(messages)
    
    return {"messages": [response]}

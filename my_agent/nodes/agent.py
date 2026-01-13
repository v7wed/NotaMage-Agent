"""
Agent node for The Mage - the main LLM-powered conversational node.
"""
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage
from my_agent.state import MageState
from my_agent.prompts import get_system_prompt
from my_agent.tools import all_tools

def get_llm():
    llm = ChatDeepSeek(model='deepseek-chat', temperature=0.7)
    return llm



def agent_node(state: MageState) -> MageState:
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
    user_name = state['user_name']
    
    # Build the messages list with system prompt (no user_id needed)
    system_message = SystemMessage(content=get_system_prompt(user_name))
    messages = [system_message] + list(state["messages"])
    llm = get_llm().bind_tools(all_tools)
    # Invoke the LLM
    response = llm.invoke(messages)
    
    # Return the response to be added to messages
    return {"messages": [response]}

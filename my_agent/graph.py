"""
LangGraph graph definition for The Mage agent.
"""
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from my_agent.state import MageState
from my_agent.nodes import agent_node
from my_agent.tools import all_tools



def should_continue_after_agent(state: MageState) -> str:
    """
    Determine if the agent wants to use tools or end the flow.
    
    Returns:
        - "tools" if the last message has tool calls
        - "end" if no tool calls (response is complete)
    """
    messages = state.get("messages", [])
    if not messages:
        print("DEBUG: No messages in state, returning 'end'")
        return "end"
    
    last_message = messages[-1]
    
    # Check if the last message has tool calls
    has_tool_calls = hasattr(last_message, "tool_calls") and last_message.tool_calls

    
    
    if has_tool_calls:
        print('AI thinking messsage: ', last_message.content)
        for t in last_message.tool_calls:
            print("calling a tool: " , t['name'])
        return "tools"
    
    return "end"




# Create the graph with MageState
graph = StateGraph(MageState)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(all_tools))

# Set entry point
graph.add_edge(START, "agent")

# Add conditional edges from agent
graph.add_conditional_edges(
    "agent",
    should_continue_after_agent,
    {
        "tools": "tools",
        "end": END,
    }
)

# Tools always return to agent for processing results
graph.add_edge("tools", "agent")

# Compile the graph
mage_graph = graph.compile()

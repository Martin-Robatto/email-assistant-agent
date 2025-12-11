"""Agent graph construction."""

from langgraph.graph import StateGraph, START, END
from email_assistant.utils import GraphState
from email_assistant.nodes import triage_router, agent_node, should_respond, should_continue, tool_node


def create_graph():
    """Create and compile the agent graph.

    Returns:
        A compiled LangGraph graph.
    """
    # Create the graph
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("triage_router", triage_router)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    # Add edges
    # Start with triage to classify the email
    workflow.add_edge(START, "triage_router")
    
    # Add conditional edge based on should_respond function
    workflow.add_conditional_edges(
        "triage_router",
        should_respond,
        {
            True: "agent",
            False: END
        }
    )
    
    # Add conditional edge from agent to tools or end (ReAct loop)
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    # After tools execute, loop back to agent for next reasoning step
    workflow.add_edge("tools", "agent")

    # Compile the graph
    graph = workflow.compile()
    graph.get_graph().draw_mermaid_png(output_file_path="email_assistant/graph.png")

    return graph


# Create the graph instance
graph = create_graph()
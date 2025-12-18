"""HITL-enabled agent graph construction with conditional edges."""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from email_assistant_hitl.utils import GraphState
from email_assistant_hitl.nodes.triage_router import triage_router
from email_assistant_hitl.nodes.notify_handler_hitl import notify_handler_hitl
from email_assistant_hitl.nodes.agent_node_hitl import agent_node_hitl
from email_assistant_hitl.nodes.action_handler_hitl import action_handler_hitl


def should_respond(state: GraphState) -> Literal["agent_node_hitl", "review_notification", "__end__"]:
    """Route based on email classification.
    
    Args:
        state: The current graph state.
        
    Returns:
        The next node to route to based on classification.
    """
    classification = state["classification_decision"]
    
    if classification == "respond":
        return "agent_node_hitl"
    elif classification == "notify":
        return "review_notification"
    else:  # ignore
        return "__end__"


def should_continue_after_review(state: GraphState) -> Literal["agent_node_hitl", "__end__"]:
    """Route after notification review based on user response.
    
    If user provided feedback (messages were added), go to agent.
    If user ignored (no messages), end workflow.
    
    Args:
        state: The current graph state.
        
    Returns:
        The next node to route to.
    """
    # If messages were added by notification review, user wants to respond
    if state.get("messages"):
        return "agent_node_hitl"
    else:
        return "__end__"


def should_continue_drafting(state: GraphState) -> Literal["review_action", "__end__"]:
    """Determine if we should review the drafted action or end.
    
    Args:
        state: The current graph state.
        
    Returns:
        The next node to route to.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "Done":
                return "__end__"
        return "review_action"
    
    return "__end__"


def should_continue_after_action_review(state: GraphState) -> Literal["agent_node_hitl", "__end__"]:
    """Route after action review based on user response.
    
    If user ignored, workflow ends. Otherwise loop back to draft more actions.
    """
    if state.get("workflow_should_end"):
        return "__end__"
    else:
        return "agent_node_hitl"


def create_graph(checkpointer=None):
    """Create and compile the HITL-enabled agent graph.
    
    Uses conditional edges throughout for clear routing logic.
    Node names describe their purpose clearly.

    Returns:
        A compiled LangGraph graph with HITL capabilities.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add all nodes with descriptive names
    workflow.add_node("triage_router", triage_router)
    workflow.add_node("notify_handler_hitl", notify_handler_hitl)
    workflow.add_node("agent_node_hitl", agent_node_hitl)
    workflow.add_node("action_handler_hitl", action_handler_hitl)
    
    # Start by classifying the email
    workflow.add_edge(START, "triage_router")
    
    # From triage_router, route based on classification
    workflow.add_conditional_edges(
        "triage_router",
        should_respond,
        {
            "agent_node_hitl": "agent_node_hitl",
            "review_notification": "notify_handler_hitl",
            "__end__": END,
        },
    )
    
    # From notify_handler_hitl, route based on user response
    workflow.add_conditional_edges(
        "notify_handler_hitl",
        should_continue_after_review,
        {
            "agent_node_hitl": "agent_node_hitl",
            "__end__": END,
        },
    )
    
    # From agent_node_hitl, check if Done tool was called
    workflow.add_conditional_edges(
        "agent_node_hitl",
        should_continue_drafting,
        {
            "review_action": "action_handler_hitl",
            "__end__": END,
        },
    )
    
    # After review_action, check if user ignored or approved
    workflow.add_conditional_edges(
        "action_handler_hitl",
        should_continue_after_action_review,
        {
            "agent_node_hitl": "agent_node_hitl",
            "__end__": END,
        },
    )
    
    graph = workflow.compile(checkpointer=checkpointer)
    graph.get_graph().draw_mermaid_png(output_file_path="email_assistant_hitl/graph.png")
    
    return graph


# Create the HITL graph instance
graph = create_graph(checkpointer=None)

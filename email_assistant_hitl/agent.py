"""HITL-enabled agent graph construction with conditional edges."""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from email_assistant_hitl.utils import GraphState
from email_assistant_hitl.nodes.triage_router import triage_router as classify_email
from email_assistant_hitl.nodes.triage_interrupt_handler import triage_interrupt_handler as review_notification
from email_assistant_hitl.nodes.agent_node_hitl import agent_node_hitl as draft_response
from email_assistant_hitl.nodes.interrupt_handler import interrupt_handler as review_action


def should_respond(state: GraphState) -> Literal["draft_response", "review_notification", "__end__"]:
    """Route based on email classification.
    
    Args:
        state: The current graph state.
        
    Returns:
        The next node to route to based on classification.
    """
    classification = state["classification_decision"]
    
    if classification == "respond":
        return "draft_response"
    elif classification == "notify":
        return "review_notification"
    else:  # ignore
        return "__end__"


def should_continue_after_review(state: GraphState) -> Literal["draft_response", "__end__"]:
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
        return "draft_response"
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


def should_continue_after_action_review(state: GraphState) -> Literal["draft_response", "__end__"]:
    """Route after action review based on user response.
    
    If user ignored, workflow ends. Otherwise loop back to draft more actions.
    """
    if state.get("workflow_should_end"):
        return "__end__"
    else:
        return "draft_response"


def create_graph():
    """Create and compile the HITL-enabled agent graph.
    
    Uses conditional edges throughout for clear routing logic.
    Node names describe their purpose clearly.

    Returns:
        A compiled LangGraph graph with HITL capabilities.
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add all nodes with descriptive names
    workflow.add_node("classify_email", classify_email)
    workflow.add_node("review_notification", review_notification)
    workflow.add_node("draft_response", draft_response)
    workflow.add_node("review_action", review_action)
    
    # Start by classifying the email
    workflow.add_edge(START, "classify_email")
    
    # From classify_email, route based on classification
    workflow.add_conditional_edges(
        "classify_email",
        should_respond,
        {
            "draft_response": "draft_response",
            "review_notification": "review_notification",
            "__end__": END,
        },
    )
    
    # From review_notification, route based on user response
    workflow.add_conditional_edges(
        "review_notification",
        should_continue_after_review,
        {
            "draft_response": "draft_response",
            "__end__": END,
        },
    )
    
    # From draft_response, check if Done tool was called
    workflow.add_conditional_edges(
        "draft_response",
        should_continue_drafting,
        {
            "review_action": "review_action",
            "__end__": END,
        },
    )
    
    # After review_action, check if user ignored or approved
    workflow.add_conditional_edges(
        "review_action",
        should_continue_after_action_review,
        {
            "draft_response": "draft_response",
            "__end__": END,
        },
    )
    
    # Compile with memory
    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory)
    
    return graph


# Create the HITL graph instance
graph = create_graph()

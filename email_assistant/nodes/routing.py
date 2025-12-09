"""Routing functions for conditional edges in the graph."""

from email_assistant.utils.state import GraphState


def should_respond(state: GraphState) -> bool:
    """Check if the email should be responded to.
    
    Args:
        state: The current graph state.
        
    Returns:
        True if email requires response, False otherwise.
    """
    classification = state["classification_decision"]

    if classification == "respond":
        return True
    elif classification == "ignore":
        return False
    elif classification == "notify":
        return False
    else:
        raise ValueError(f"Invalid classification: {classification}")


def should_continue(state: GraphState) -> str:
    """Determine if we should continue to tools or end.
    
    Args:
        state: The current graph state.
    
    Returns:
        "tools" if there are tool calls to execute
        "end" if the agent is done
    """
    last_message = state["messages"][-1]
    
    # Check if the last message has tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return "end"
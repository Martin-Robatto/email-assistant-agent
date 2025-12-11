"""Triage interrupt handler node for HITL - simple version without Command."""

from langgraph.types import interrupt
from email_assistant_hitl.utils.state import GraphState
from email_assistant_hitl.helpers import parse_email, format_email_markdown


def notify_handler_hitl(state: GraphState) -> GraphState:
    """Handle interrupts from the triage step when email is classified as 'notify'.
    
    This node creates an interrupt to show the email to the user and allows them
    to decide whether to ignore it or provide feedback to respond.
    
    Args:
        state: The current graph state.
        
    Returns:
        Updated state with user response.
    """
    # Parse the email input
    author, to, subject, email_thread = parse_email(state["email_input"])
    
    # Create email markdown for display
    email_markdown = format_email_markdown(subject, author, to, email_thread)
    
    # Create interrupt request for Agent Inbox
    request = {
        "action_request": {
            "action": f"Email Assistant: {state['classification_decision']}",
            "args": {}
        },
        "config": {
            "allow_ignore": True,
            "allow_respond": True,
            "allow_edit": False,
            "allow_accept": False,
        },
        "description": email_markdown,
    }
    
    # Send interrupt and wait for user response
    response = interrupt([request])[0]
    
    # Process user response based on type
    if response["type"] == "response":
        # User wants to respond to the email
        user_input = response["args"]
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Email to notify user about: {email_markdown}"
                },
                {
                    "role": "user",
                    "content": f"User wants to reply to the email. Use this feedback to respond: {user_input}"
                }
            ]
        }
    else:
        # User ignored - return empty update (conditional edge will route to END)
        return {}

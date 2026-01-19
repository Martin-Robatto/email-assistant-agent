"""Triage interrupt handler node for HITL - simple version without Command."""

from langgraph.types import interrupt
from langgraph.store.base import BaseStore
from email_assistant_hitl.utils.state import GraphState
from email_assistant_hitl.utils.memory import update_memory
from email_assistant_hitl.prompts.defaults import MEMORY_UPDATE_INSTRUCTIONS_REINFORCEMENT
from email_assistant_hitl.helpers import parse_email, format_email_markdown


def notify_handler_hitl(state: GraphState, store: BaseStore) -> GraphState:
    """Handle interrupts from the triage step when email is classified as 'notify'.
    
    This node creates an interrupt to show the email to the user and allows them
    to decide whether to ignore it or provide feedback to respond.
    
    Args:
        state: The current graph state.
        
    Returns:
        Updated state with user response.
    """
    author, to, subject, email_thread = parse_email(state["email_input"])
    
    email_markdown = format_email_markdown(subject, author, to, email_thread)
    
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
    
    response = interrupt([request])[0]
    
    if response["type"] == "response":
        user_input = response["args"]
        update_memory(store, ("email_assistant", "triage_preferences"), [{
            "role": "user",
            "content": f"The user decided to respond to the email, so update the triage preferences to capture this. Follow all instructions above, and remember: {MEMORY_UPDATE_INSTRUCTIONS_REINFORCEMENT}."
        }] + [{"role": "user", "content": f"Email to notify user about: {email_markdown}"}, {"role": "user", "content": f"User wants to reply to the email. Use this feedback to respond: {user_input}"}])

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
        messages = [
            {"role": "user", "content": f"Email to notify user about: {email_markdown}"},
            {"role": "user", "content": "The user decided to ignore the email even though it was classified as notify. Update triage preferences to capture this."}
        ]
        update_memory(store, ("email_assistant", "triage_preferences"), messages)
        
        return {}

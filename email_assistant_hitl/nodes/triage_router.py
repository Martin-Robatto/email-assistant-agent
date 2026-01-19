"""Triage router node for HITL - simple version without Command."""

from langgraph.store.base import BaseStore
from email_assistant_hitl.utils.state import GraphState
from email_assistant_hitl.utils.router import llm_router
from email_assistant_hitl.utils.memory import get_memory
from email_assistant_hitl.helpers import parse_email, format_email_markdown
from email_assistant_hitl.prompts import (
    triage_system_prompt,
    triage_user_prompt,
    default_background,
    default_triage_instructions,
)


def triage_router(state: GraphState, store: BaseStore) -> GraphState:
    """Analyze email content to decide if we should respond, notify, or ignore.
    
    Args:
        state: The current graph state containing the email input.
        
    Returns:
        Updated state with classification and messages.
    """
    author, to, subject, email_thread = parse_email(state["email_input"])
    
    email_markdown = format_email_markdown(subject, author, to, email_thread)
    
    triage_instructions = get_memory(store, ("email_assistant", "triage_preferences"), default_triage_instructions)
    
    system_prompt = triage_system_prompt.format(
        background=default_background,
        triage_instructions=triage_instructions
    )
    
    user_prompt = triage_user_prompt.format(
        author=author, to=to, subject=subject, email_thread=email_thread
    )
    
    result = llm_router.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
    
    classification = result.classification
    
    update = {"classification_decision": classification}
    
    if classification == "respond":
        print("📧 Classification: RESPOND - This email requires a response")
        update["messages"] = [{
            "role": "user",
            "content": f"Respond to the email: {email_markdown}"
        }]
        
    elif classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
        
    elif classification == "notify":
        print("🔔 Classification: NOTIFY - This email contains important information")
        
    else:
        raise ValueError(f"Invalid classification: {classification}")
    
    return update

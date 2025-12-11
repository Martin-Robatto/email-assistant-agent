"""Triage router node for email classification."""

from email_assistant.utils.state import GraphState
from email_assistant.utils.router import get_llm_router
from email_assistant.helpers import parse_email, format_email_markdown
from email_assistant.prompts import (
    triage_system_prompt,
    triage_user_prompt,
    default_background,
    default_triage_instructions,
)


def triage_router(state: GraphState) -> GraphState:
    """Analyze email content to decide if we should respond, notify, or ignore.
    
    Args:
        state: The current graph state containing the email input.
        
    Returns:
        A dictionary with updated state including classification decision and messages.
    """
    author, to, subject, email_thread = parse_email(state["email_input"])
    system_prompt = triage_system_prompt.format(
        background=default_background, triage_instructions=default_triage_instructions
    )

    user_prompt = triage_user_prompt.format(
        author=author, to=to, subject=subject, email_thread=email_thread
    )

    result = get_llm_router().invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    # Store classification decision in state
    update = {"classification_decision": result.classification}

    if result.classification == "respond":
        print("📧 Classification: RESPOND - This email requires a response")
        update["messages"] = [
            {
                "role": "user",
                "content": f"Respond to the email: \n\n{format_email_markdown(subject, author, to, email_thread)}",
            }
        ]
    elif result.classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
    elif result.classification == "notify":
        print("🔔 Classification: NOTIFY - This email contains important information")
    else:
        raise ValueError(f"Invalid classification: {result.classification}")

    return update
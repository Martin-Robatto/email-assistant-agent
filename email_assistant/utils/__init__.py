"""Utilities for the agent graph."""

from email_assistant.utils.state import GraphState
from email_assistant.utils.nodes import triage_router, email_node, should_respond
from email_assistant.utils.tools import (
    write_email,
    schedule_meeting,
    check_calendar_availability,
)
from email_assistant.utils.router import RouterSchema, llm_router
from email_assistant.utils.helpers import parse_email, format_email_markdown
from email_assistant.utils.prompts import (
    default_background,
    default_triage_instructions,
    triage_system_prompt,
    triage_user_prompt,
)

__all__ = [
    "GraphState",
    "triage_router",
    "email_node",
    "should_respond",
    "write_email",
    "schedule_meeting",
    "check_calendar_availability",
    "RouterSchema",
    "llm_router",
    "parse_email",
    "format_email_markdown",
    "default_background",
    "default_triage_instructions",
    "triage_system_prompt",
    "triage_user_prompt",
]

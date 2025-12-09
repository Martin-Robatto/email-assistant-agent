"""Prompts for email triage and response generation."""

from email_assistant.prompts.defaults import (
    default_background,
    default_triage_instructions,
    default_response_preferences,
    default_cal_preferences,
)
from email_assistant.prompts.triage_prompts import (
    triage_system_prompt,
    triage_user_prompt,
)
from email_assistant.prompts.agent_prompts import (
    agent_system_prompt,
    AGENT_TOOLS_PROMPT,
)

__all__ = [
    "default_background",
    "default_triage_instructions",
    "default_response_preferences",
    "default_cal_preferences",
    "triage_system_prompt",
    "triage_user_prompt",
    "agent_system_prompt",
    "AGENT_TOOLS_PROMPT",
]
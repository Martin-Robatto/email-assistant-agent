"""Tools for the email assistant agent."""

from email_assistant.tools.email_tools import write_email
from email_assistant.tools.calendar_tools import (
    schedule_meeting,
    check_calendar_availability,
)

__all__ = [
    "write_email",
    "schedule_meeting",
    "check_calendar_availability",
]
"""Tools for the email assistant agent."""

from email_assistant.tools.email_tools import write_email, search_emails
from email_assistant.tools.calendar_tools import (
    schedule_meeting,
    check_calendar_availability,
    search_events,
    update_event,
)

__all__ = [
    "write_email",
    "search_emails",
    "schedule_meeting",
    "check_calendar_availability",
    "search_events",
    "update_event",
]
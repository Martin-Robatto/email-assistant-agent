"""Tool execution node."""

from langgraph.prebuilt import ToolNode
from email_assistant.tools import (
    write_email,
    search_emails,
    schedule_meeting,
    check_calendar_availability,
    search_events,
    update_event,
)


# Create the tool node for executing tools
tools = [
    write_email,
    search_emails,
    schedule_meeting,
    check_calendar_availability,
    search_events,
    update_event,
]
tool_node = ToolNode(tools)
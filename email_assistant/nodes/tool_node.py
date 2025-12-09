"""Tool execution node."""

from langgraph.prebuilt import ToolNode
from email_assistant.tools import write_email, schedule_meeting, check_calendar_availability


# Create the tool node for executing tools
tools = [write_email, schedule_meeting, check_calendar_availability]
tool_node = ToolNode(tools)
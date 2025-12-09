"""Prompts for the agent node that generates email responses."""

# Agent system prompt for response generation
agent_system_prompt = """
{background}

{tools_prompt}

## Response Preferences
{response_preferences}

## Calendar Preferences
{cal_preferences}

Use the available tools to help craft appropriate responses and manage calendar events.
"""

# Agent tools prompt
AGENT_TOOLS_PROMPT = """
You have access to the following tools:
- write_email: Compose and send email responses
- schedule_meeting: Schedule calendar meetings with attendees
- check_calendar_availability: Check available time slots
- Done: Mark the task as complete when finished

Use these tools to accomplish the user's request effectively.
"""
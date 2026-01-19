"""Agent node for HITL email response reasoning and tool calling."""

from email_assistant_hitl.utils.state import GraphState
from email_assistant_hitl.utils.router import llm_with_tools_hitl
from email_assistant_hitl.prompts import (
    agent_system_prompt,
    default_background,
    default_response_preferences,
    default_cal_preferences,
)


# HITL-specific tools prompt
# HITL-specific tools prompt
AGENT_TOOLS_PROMPT_HITL = """
You have access to the following tools to help respond to emails:

Email Tools:
- write_email: Compose and send email responses (use this to draft your final reply)
- search_emails: Search through past emails to find information, context, or previous conversations

Calendar Tools:
- search_events: Search for existing calendar events (use when rescheduling or checking existing meetings)
- update_event: Update an existing calendar event (use when rescheduling meetings)
- schedule_meeting: Schedule new calendar meetings with attendees
- check_calendar_availability: Check available time slots for a given day

Human Interaction Tools:
- Question: Ask the user a question when you need clarification or additional information

MANDATORY TOOL USAGE RULES:
1. Meeting reschedule requests: You MUST call search_events to find the current meeting, then update_event to reschedule it.
2. Status/information requests: You MUST call search_emails to find the requested information.
3. New meeting scheduling: You MUST call check_calendar_availability first, then schedule_meeting.
4. When you need clarification: Use the Question tool to ask the user.
5. Final step: NOTIFY THE USER. After you have successfully taken the action (sent email, scheduled meeting), you MUST respond with a concise text message confirming what you did.

NEVER provide a generic response without using tools first.

Think step-by-step:
- What information do I need? -> Use search_emails or search_events
- What action is requested? -> Use update_event, schedule_meeting, or check_calendar_availability
- Do I need clarification? -> Use Question
- Draft and send response -> Use write_email
- Signal completion -> Send a text response summarizing your action
"""


def agent_node_hitl(state: GraphState) -> GraphState:
    """Agent reasoning node for HITL where the LLM decides which actions to take.
    
    This version uses the HITL-specific LLM that includes Question and Done tools,
    and enforces tool usage.

    Args:
        state: The current graph state containing messages.

    Returns:
        A dictionary with the LLM's response message (may include tool calls).
    """
    # Build the system prompt with all preferences
    system_message = {
        "role": "system",
        "content": agent_system_prompt.format(
            tools_prompt=AGENT_TOOLS_PROMPT_HITL,
            background=default_background,
            response_preferences=default_response_preferences,
            cal_preferences=default_cal_preferences,
        ),
    }

    # Invoke the LLM with HITL tools
    response = llm_with_tools_hitl.invoke([system_message] + state["messages"])

    return {"messages": [response]}

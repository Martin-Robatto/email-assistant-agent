"""Agent node for email response reasoning and tool calling."""

from email_assistant.utils.state import GraphState
from email_assistant.utils.router import llm_with_tools
from email_assistant.prompts import (
    agent_system_prompt,
    AGENT_TOOLS_PROMPT,
    default_background,
    default_response_preferences,
    default_cal_preferences,
)


def agent_node(state: GraphState) -> GraphState:
    """Agent reasoning node where the LLM decides which actions to take.

    Args:
        state: The current graph state containing messages.

    Returns:
        A dictionary with the LLM's response message (may include tool calls).
    """
    # Build the system prompt with all preferences
    system_message = {
        "role": "system",
        "content": agent_system_prompt.format(
            tools_prompt=AGENT_TOOLS_PROMPT,
            background=default_background,
            response_preferences=default_response_preferences,
            cal_preferences=default_cal_preferences,
        ),
    }

    # Invoke the LLM with tools
    response = llm_with_tools.invoke([system_message] + state["messages"])

    return {"messages": [response]}
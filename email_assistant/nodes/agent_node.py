"""Agent node for email response reasoning and tool calling."""

from email_assistant.utils.state import GraphState
from email_assistant.utils.router import get_llm_router_with_tools, tools
from email_assistant.helpers import format_tools
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
    tools_prompt = AGENT_TOOLS_PROMPT.format(tools_descriptions=format_tools(tools))
    
    # Build the system prompt with all preferences
    system_message = {
        "role": "system",
        "content": agent_system_prompt.format(
            tools_prompt=tools_prompt,
            background=default_background,
            response_preferences=default_response_preferences,
            cal_preferences=default_cal_preferences,
        ),
    }

    llm_with_tools = get_llm_router_with_tools()
    response = llm_with_tools.invoke([system_message] + state["messages"])

    return {"messages": [response]}
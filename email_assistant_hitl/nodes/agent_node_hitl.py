"""Agent node for HITL email response reasoning and tool calling."""

from langgraph.store.base import BaseStore
from email_assistant_hitl.utils.state import GraphState
from email_assistant_hitl.utils.router import llm_with_tools_hitl
from email_assistant_hitl.utils.memory import get_memory
from email_assistant_hitl.prompts import (
    agent_system_prompt,
    default_background,
    default_response_preferences,
    default_cal_preferences,
    AGENT_TOOLS_PROMPT_HITL,
)


def agent_node_hitl(state: GraphState, store: BaseStore) -> GraphState:
    """Agent reasoning node for HITL where the LLM decides which actions to take.
    
    This version uses the HITL-specific LLM that includes Question and Done tools,
    and enforces tool usage.

    Args:
        state: The current graph state containing messages.

    Returns:
        A dictionary with the LLM's response message (may include tool calls).
    """
    cal_preferences = get_memory(store, ("email_assistant", "cal_preferences"), default_cal_preferences)
    
    response_preferences = get_memory(store, ("email_assistant", "response_preferences"), default_response_preferences)

    system_message = {
        "role": "system",
        "content": agent_system_prompt.format(
            tools_prompt=AGENT_TOOLS_PROMPT_HITL,
            background=default_background,
            response_preferences=response_preferences,
            cal_preferences=cal_preferences,
        ),
    }

    response = llm_with_tools_hitl.invoke([system_message] + state["messages"])

    return {"messages": [response]}

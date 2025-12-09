from email_assistant.utils.prompts import default_response_preferences, AGENT_TOOLS_PROMPT, agent_system_prompt, default_cal_preferences
from email_assistant.utils.state import GraphState
from email_assistant.utils.router import llm_router, llm_with_tools
from email_assistant.utils.helpers import parse_email, format_email_markdown
from email_assistant.utils.prompts import (
    triage_system_prompt,
    triage_user_prompt,
    default_background,
    default_triage_instructions,
)
from langgraph.prebuilt import ToolNode
from email_assistant.utils.tools import write_email, schedule_meeting, check_calendar_availability

# Create the tool node for executing tools
tools = [write_email, schedule_meeting, check_calendar_availability]
tool_node = ToolNode(tools)

def triage_router(state: GraphState) -> GraphState:
    """Analyze email content to decide if we should respond, notify, or ignore.
    
    Args:
        state: The current graph state containing the email input.
        
    Returns:
        A dictionary with updated state including classification decision and messages.
    """
    author, to, subject, email_thread = parse_email(state["email_input"])
    system_prompt = triage_system_prompt.format(
        background=default_background, triage_instructions=default_triage_instructions
    )

    user_prompt = triage_user_prompt.format(
        author=author, to=to, subject=subject, email_thread=email_thread
    )

    result = llm_router.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    # Store classification decision in state
    update = {"classification_decision": result.classification}

    if result.classification == "respond":
        print("📧 Classification: RESPOND - This email requires a response")
        update["messages"] = [
            {
                "role": "user",
                "content": f"Respond to the email: \n\n{format_email_markdown(subject, author, to, email_thread)}",
            }
        ]
    elif result.classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
    elif result.classification == "notify":
        print("🔔 Classification: NOTIFY - This email contains important information")
    else:
        raise ValueError(f"Invalid classification: {result.classification}")

    return update

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

def should_respond(state: GraphState) -> bool:
    """Check if the email should be responded to."""
    classification = state["classification_decision"]

    if classification == "respond":
        return True
    elif classification == "ignore":
        return False
    elif classification == "notify":
        return False
    else:
        raise ValueError(f"Invalid classification: {classification}")

def should_continue(state: GraphState) -> str:
    """Determine if we should continue to tools or end.
    
    Returns:
        "tools" if there are tool calls to execute
        "end" if the agent is done
    """
    last_message = state["messages"][-1]
    
    # Check if the last message has tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return "end"

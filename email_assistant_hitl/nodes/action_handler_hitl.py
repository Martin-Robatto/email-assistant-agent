"""Tool call interrupt handler for HITL."""

from langgraph.types import interrupt
from email_assistant_hitl.utils.state import GraphState
from email_assistant_hitl.helpers import parse_email, format_email_markdown
from email_assistant_hitl.helpers.hitl_helpers import format_tool_call_for_display
from email_assistant_hitl.tools import (
    write_email,
    schedule_meeting,
    check_calendar_availability,
    search_emails,
    search_events,
    update_event,
    Question,
)


# Create a tools dictionary for easy lookup
tools_by_name = {
    "write_email": write_email,
    "schedule_meeting": schedule_meeting,
    "check_calendar_availability": check_calendar_availability,
    "search_emails": search_emails,
    "search_events": search_events,
    "update_event": update_event,
    "Question": Question,
}


def action_handler_hitl(state: GraphState) -> GraphState:
    """Handle interrupts for tool calls that require human review.
    
    This node examines tool calls from the agent and:
    1. Executes low-risk tools directly (like check_calendar_availability)
    2. Creates interrupts for high-risk tools (write_email, schedule_meeting, Question)
    3. Processes user responses (accept, edit, ignore, or respond with feedback)
    
    Args:
        state: The current graph state containing messages with tool calls.
        
    Returns:
        Updated state with tool results and optional workflow_should_end flag.
    """
    # Store messages/results
    result = []
    
    # Track if user ignored and we should end
    should_end_workflow = False
    
    # Iterate over tool calls in the last message
    for tool_call in state["messages"][-1].tool_calls:
        
        # Tools that require human review
        hitl_tools = ["write_email", "schedule_meeting", "Question"]
        
        # If tool doesn't require HITL, execute directly
        if tool_call["name"] not in hitl_tools:
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append({
                "role": "tool",
                "content": observation,
                "tool_call_id": tool_call["id"]
            })
            continue
        
        # Get original email for context
        email_input = state["email_input"]
        author, to, subject, email_thread = parse_email(email_input)
        original_email_markdown = format_email_markdown(subject, author, to, email_thread)
        
        # Format tool call for display
        tool_display = format_tool_call_for_display(tool_call)
        description = original_email_markdown + "\n---\n" + tool_display
        
        # Configure allowed actions based on tool type
        if tool_call["name"] == "write_email":
            config = {
                "allow_ignore": True,
                "allow_respond": True,
                "allow_edit": True,
                "allow_accept": True,
            }
        elif tool_call["name"] == "schedule_meeting":
            config = {
                "allow_ignore": True,
                "allow_respond": True,
                "allow_edit": True,
                "allow_accept": True,
            }
        elif tool_call["name"] == "Question":
            config = {
                "allow_ignore": True,
                "allow_respond": True,
                "allow_edit": False,
                "allow_accept": False,
            }
        else:
            raise ValueError(f"Unknown HITL tool: {tool_call['name']}")
        
        # Create interrupt request
        request = {
            "action_request": {
                "action": tool_call["name"],
                "args": tool_call["args"]
            },
            "config": config,
            "description": description,
        }
        
        # Send interrupt and wait for user response
        response = interrupt([request])[0]
        
        # Process user response
        if response["type"] == "accept":
            # Execute tool with original args
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append({
                "role": "tool",
                "content": observation,
                "tool_call_id": tool_call["id"]
            })
            
        elif response["type"] == "edit":
            # Get edited args from user
            tool = tools_by_name[tool_call["name"]]
            edited_args = response["args"]["args"]
            
            # Update the AI message's tool call with edited content
            ai_message = state["messages"][-1]
            current_id = tool_call["id"]
            
            # Create updated tool calls list
            updated_tool_calls = [
                tc for tc in ai_message.tool_calls if tc["id"] != current_id
            ] + [
                {
                    "type": "tool_call",
                    "name": tool_call["name"],
                    "args": edited_args,
                    "id": current_id
                }
            ]
            
            # Create new message with updated tool calls
            result.append(ai_message.model_copy(update={"tool_calls": updated_tool_calls}))
            
            # Execute tool with edited args
            observation = tool.invoke(edited_args)
            result.append({
                "role": "tool",
                "content": observation,
                "tool_call_id": current_id
            })
            
        elif response["type"] == "ignore":
            # Don't execute tool, provide feedback to agent
            if tool_call["name"] == "write_email":
                content = "User ignored this email draft. Ignore this email and end the workflow."
            elif tool_call["name"] == "schedule_meeting":
                content = "User ignored this calendar meeting draft. Ignore this email and end the workflow."
            elif tool_call["name"] == "Question":
                content = "User ignored this question. Ignore this email and end the workflow."
            else:
                content = "User ignored this action. End the workflow."
            
            result.append({
                "role": "tool",
                "content": content,
                "tool_call_id": tool_call["id"]
            })
            should_end_workflow = True
            
        elif response["type"] == "response":
            # User provided feedback
            user_feedback = response["args"]
            
            if tool_call["name"] == "write_email":
                content = f"User gave feedback, which we can incorporate into the email. Feedback: {user_feedback}"
            elif tool_call["name"] == "schedule_meeting":
                content = f"User gave feedback, which we can incorporate into the meeting request. Feedback: {user_feedback}"
            elif tool_call["name"] == "Question":
                content = f"User answered the question, which we can use for any follow up actions. Feedback: {user_feedback}"
            else:
                content = f"User provided feedback: {user_feedback}"
            
            result.append({
                "role": "tool",
                "content": content,
                "tool_call_id": tool_call["id"]
            })
            
        else:
            raise ValueError(f"Invalid response type: {response['type']}")
    
    # Update state with results
    update = {"messages": result}
    
    # If user ignored, add flag so conditional edge routes to END
    if should_end_workflow:
        update["workflow_should_end"] = True
    
    return update

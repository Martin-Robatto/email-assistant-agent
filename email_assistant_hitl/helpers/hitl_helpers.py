"""Helper functions for Human-in-the-Loop functionality."""

from typing import Any


def format_tool_call_for_display(tool_call: dict[str, Any]) -> str:
    """Format a tool call for display in interrupts.
    
    Args:
        tool_call: The tool call dictionary containing name, args, and id.
        
    Returns:
        A formatted markdown string showing the tool call details.
    """
    name = tool_call.get("name", "Unknown")
    args = tool_call.get("args", {})
    
    # Format arguments nicely
    args_str = "\n".join([f"- **{key}**: {value}" for key, value in args.items()])
    
    return f"""
## Proposed Action: {name}

### Arguments:
{args_str}
"""

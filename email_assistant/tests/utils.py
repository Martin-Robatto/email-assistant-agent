"""Utility functions for testing."""

from typing import List


def extract_tool_calls(messages: list) -> List[str]:
    """Extract all tool names called in a message history.
    
    Args:
        messages: List of message dicts from agent execution
        
    Returns:
        List of tool names that were called (lowercase)
    """
    tool_calls = []
    for message in messages:
        # Check for tool_calls in message
        if isinstance(message, dict) and "tool_calls" in message:
            for tool_call in message["tool_calls"]:
                tool_calls.append(tool_call["name"].lower())
        
        # Also check if message has a 'name' field (ToolMessage)
        if isinstance(message, dict) and message.get("type") == "tool":
            tool_name = message.get("name", "")
            if tool_name:
                tool_calls.append(tool_name.lower())
    
    return list(set(tool_calls))  # Remove duplicates


def format_messages_string(messages: list) -> str:
    """Format message history for LLM judge evaluation.
    
    Args:
        messages: List of message dicts
        
    Returns:
        Formatted string representation of conversation
    """
    formatted = []
    for msg in messages:
        if hasattr(msg, 'content'):
            role = msg.__class__.__name__.replace('Message', '').upper()
            content = msg.content
        else:
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")
        
        if content:
            formatted.append(f"{role}: {content}")
    
    return "\n\n".join(formatted)


def count_tool_invocations(messages: list, tool_name: str) -> int:
    """Count how many times a specific tool was invoked.
    
    Args:
        messages: List of message dicts from agent execution
        tool_name: Name of the tool to count
        
    Returns:
        Number of times the tool was called
    """
    count = 0
    tool_name_lower = tool_name.lower()
    
    for message in messages:
        if isinstance(message, dict) and "tool_calls" in message:
            for tool_call in message["tool_calls"]:
                if tool_call["name"].lower() == tool_name_lower:
                    count += 1
        
        if isinstance(message, dict) and message.get("type") == "tool":
            if message.get("name", "").lower() == tool_name_lower:
                count += 1
    
    return count


def has_all_required_tools(messages: list, required_tools: List[str]) -> bool:
    """Check if all required tools were called.
    
    Args:
        messages: List of message dicts from agent execution
        required_tools: List of required tool names
        
    Returns:
        True if all required tools were called, False otherwise
    """
    extracted_tools = extract_tool_calls(messages)
    return all(tool.lower() in extracted_tools for tool in required_tools)


def get_missing_tools(messages: list, expected_tools: List[str]) -> List[str]:
    """Get list of expected tools that were not called.
    
    Args:
        messages: List of message dicts from agent execution
        expected_tools: List of expected tool names
        
    Returns:
        List of tools that were expected but not called
    """
    extracted_tools = extract_tool_calls(messages)
    return [tool for tool in expected_tools if tool.lower() not in extracted_tools]
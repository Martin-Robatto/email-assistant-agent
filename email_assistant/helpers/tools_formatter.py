def format_tools(tools):
    """Format tools into a string for the prompt."""
    formatted_tools = []
    for tool in tools:
        description = tool.description.split("\n")[0].strip()
        formatted_tools.append(f"- {tool.name}: {description}")
    return "\n".join(formatted_tools)

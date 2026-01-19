"""Human-in-the-Loop specific tools."""

from pydantic import BaseModel
from langchain_core.tools import tool


@tool
class Question(BaseModel):
    """Question to ask user.
    
    Use this tool when you need clarification or additional information
    from the user before proceeding with an action.
    """
    content: str




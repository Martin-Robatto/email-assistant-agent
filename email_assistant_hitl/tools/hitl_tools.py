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


@tool
class Done(BaseModel):
    """Signal that the email workflow is complete.
    
    Use this tool when you have finished all actions (sent email,
    scheduled meetings, etc.) and the workflow should end.
    """
    done: bool

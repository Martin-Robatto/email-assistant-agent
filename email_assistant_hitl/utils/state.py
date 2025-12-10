from typing import Literal, Optional
from langgraph.graph import MessagesState

class GraphState(MessagesState):
    """
    Represents the state of the graph at any given time.

    Attributes:
    email_input: email input
    classification_decision: classification decision
    workflow_should_end: flag set by interrupt_handler when user ignores
    """
    email_input: dict
    classification_decision: Literal["ignore", "respond", "notify"]
    workflow_should_end: Optional[bool] = None
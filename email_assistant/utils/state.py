from typing import Literal
from langgraph.graph import MessagesState

class GraphState(MessagesState):
    """
    Represents the state of the graph at any given time.

    Attributes:
    email_input: email input
    classification_decision: classification decision
    """
    email_input: dict
    classification_decision: Literal["ignore", "respond", "notify"]
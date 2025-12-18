"""Router schema and LLM initialization for email triage."""
from langchain_openai import ChatOpenAI
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from email_assistant.tools import (
    write_email,
    schedule_meeting,
    check_calendar_availability,
    search_events,
    update_event,
    search_emails,
)

load_dotenv()


class RouterSchema(BaseModel):
    """Analyze the unread email and route it according to its content."""

    reasoning: str = Field(
        description="Step-by-step reasoning behind the classification."
    )
    classification: Literal["ignore", "respond", "notify"] = Field(
        description="The classification of an email: 'ignore' for irrelevant emails, "
        "'notify' for important information that doesn't need a response, "
        "'respond' for emails that need a reply",
    )
    
tools = [
    write_email,
    search_emails,
    schedule_meeting,
    check_calendar_availability,
    search_events,
    update_event,
]

def create_router(model_cls, model_name: str = "gpt-4o-mini"):
    """
    Wraps a ChatOpenAI model with structured output using the given Pydantic schema.
    
    Args:
        model_cls: A Pydantic BaseModel class defining the output schema.
        model_name: Which OpenAI model to use (default: gpt-4o-mini)
        
    Returns:
        A ChatOpenAI instance that enforces the structured output.
    """
    llm = ChatOpenAI(model=model_name)
    return llm.with_structured_output(model_cls)


def get_llm_router():
    """Get the router LLM instance."""
    return create_router(RouterSchema)

def get_llm_router_with_tools(model_name: str = "gpt-4o-mini"):
    """Get the router LLM instance with tools."""
    llm = ChatOpenAI(model=model_name)
    return llm.bind_tools(tools)



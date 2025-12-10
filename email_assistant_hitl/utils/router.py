"""Router schema and LLM initialization for email triage HITL."""
from langchain_openai import ChatOpenAI
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from email_assistant_hitl.tools import (
    write_email,
    schedule_meeting,
    check_calendar_availability,
    search_events,
    update_event,
    search_emails,
    Question,
    Done,
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


# Initialize the router LLM with structured output for email classification
llm_router = ChatOpenAI(model="gpt-4o-mini").with_structured_output(RouterSchema)

# Initialize the HITL LLM with additional tools (Question, Done)
tools_hitl = [
    write_email,
    search_emails,
    schedule_meeting,
    check_calendar_availability,
    search_events,
    update_event,
    Question,
    Done,
]

llm_with_tools_hitl = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools_hitl, tool_choice="required")

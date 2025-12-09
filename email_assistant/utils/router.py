"""Router schema and LLM initialization for email triage."""
from langchain_openai import ChatOpenAI
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from email_assistant.utils.tools import write_email, schedule_meeting, check_calendar_availability  

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
llm_router = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
    RouterSchema
)

# Initialize the main LLM with tools for email response generation
tools = [write_email, schedule_meeting, check_calendar_availability]
llm_with_tools = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

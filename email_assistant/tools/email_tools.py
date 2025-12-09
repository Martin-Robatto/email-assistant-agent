"""Email-related tools."""

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def write_email(to: str, subject: str, content: str) -> str:
    """Write and send an email.
    
    Args:
        to: Email recipient address
        subject: Email subject line
        content: Email body content
        
    Returns:
        Confirmation message
    """
    # Placeholder response - in real app would send email
    return f"Email sent to {to} with subject '{subject}' and content: {content}"
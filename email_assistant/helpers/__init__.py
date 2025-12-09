"""Helper functions for email processing."""

from email_assistant.helpers.email_parser import parse_email
from email_assistant.helpers.email_formatter import format_email_markdown

__all__ = [
    "parse_email",
    "format_email_markdown",
]
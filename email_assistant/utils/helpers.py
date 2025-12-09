"""Helper functions for email processing."""

from typing import Tuple


def parse_email(email_input: dict) -> Tuple[str, str, str, str]:
    """Parse email input dictionary into components.

    Args:
        email_input: Dictionary containing email data with keys:
            - author: Email sender
            - to: Email recipient(s)
            - subject: Email subject line
            - body or thread: Email content

    Returns:
        Tuple of (author, to, subject, email_thread)
    """
    author = email_input.get("author", "Unknown")
    to = email_input.get("to", "Unknown")
    subject = email_input.get("subject", "No Subject")
    email_thread = email_input.get("body") or email_input.get("thread", "")

    return author, to, subject, email_thread


def format_email_markdown(subject: str, author: str, to: str, email_thread: str) -> str:
    """Format email components as markdown.

    Args:
        subject: Email subject line
        author: Email sender
        to: Email recipient(s)
        email_thread: Email content/thread

    Returns:
        Formatted markdown string
    """
    return f"""**Subject:** {subject}
**From:** {author}
**To:** {to}

---

{email_thread}
"""

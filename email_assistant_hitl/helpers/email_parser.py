"""Email parsing utilities."""

from typing import Tuple


def parse_email(email_input: dict) -> Tuple[str, str, str, str]:
    """Parse email input dictionary into components.

    Args:
        email_input: Dictionary containing email data with keys:
            - author: Email sender
            - to: Email recipient(s)
            - subject: Email subject line
            - body or thread or email_thread: Email content

    Returns:
        Tuple of (author, to, subject, email_thread)
    """
    author = email_input.get("author", "Unknown")
    to = email_input.get("to", "Unknown")
    subject = email_input.get("subject", "No Subject")
    email_thread = (
        email_input.get("email_thread") 
        or email_input.get("body") 
        or email_input.get("thread", "")
    )

    return author, to, subject, email_thread
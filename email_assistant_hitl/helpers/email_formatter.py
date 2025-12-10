"""Email formatting utilities."""


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
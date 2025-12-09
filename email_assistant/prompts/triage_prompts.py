"""Prompts for email triage and classification."""

# System prompt for triage
triage_system_prompt = """
{background}

{triage_instructions}

Provide your reasoning and classification.
"""

# User prompt for triage
triage_user_prompt = """
From: {author}
To: {to}
Subject: {subject}

Email Thread:
{email_thread}
"""
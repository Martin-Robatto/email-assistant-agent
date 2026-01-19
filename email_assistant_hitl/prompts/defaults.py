"""Default configuration values for prompts."""

# Default background information about the user
default_background = """
You are an AI assistant helping to manage emails for a professional.
"""

# Default triage instructions
default_triage_instructions = """
Analyze the email and classify it into one of three categories:
- 'ignore': Spam, promotional emails, newsletters, auto-replies, or irrelevant content
- 'notify': URGENT alerts, sensitive/HR/personal matters, or complex issues requiring human judgment/attention before any action is taken
- 'respond': Routine emails that require a reply (questions, scheduling, status requests) where you can safely draft a response

Key guidelines:
- If the email is sensitive, personal, confidential, or from HR/Leadership -> 'notify'
- If it's urgent but requires human eyes first -> 'notify'
- If it's a routine request for action/info -> 'respond'
- If it's promotional or informational only -> 'ignore'
"""

# Default response preferences
default_response_preferences = """
- Keep responses professional and concise
- Match the tone of the incoming email
- Be helpful and actionable
"""

# Default calendar preferences
default_cal_preferences = """
- Prefer morning meetings (9 AM - 12 PM)
- Avoid scheduling back-to-back meetings
- Leave buffer time between meetings
"""
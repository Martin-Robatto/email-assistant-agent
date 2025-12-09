"""Default configuration values for prompts."""

# Default background information about the user
default_background = """
You are an AI assistant helping to manage emails for a professional.
"""

# Default triage instructions
default_triage_instructions = """
Analyze the email and classify it into one of three categories:
- 'ignore': Spam, promotional emails, or irrelevant content
- 'notify': Important information that doesn't require a response (newsletters, updates, FYI emails)
- 'respond': Emails that require a reply (questions, requests, important conversations)
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
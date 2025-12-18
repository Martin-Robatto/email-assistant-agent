"""Test data for email assistant testing."""

email_inputs = [
    {
        "author": "john.doe@company.com",
        "to": "assistant@company.com",
        "subject": "Meeting Reschedule Request",
        "email_thread": "Hi, I need to reschedule our 1:1 meeting scheduled for tomorrow. Can we move it to next Thursday? Thanks!"
    },
    {
        "author": "ops@company.com",
        "to": "assistant@company.com",
        "subject": "URGENT: Production Server Down",
        "email_thread": "Our production server is experiencing downtime. Multiple customers are affected. Need immediate attention!"
    },
    {
        "author": "marketing@random-company.com",
        "to": "assistant@company.com",
        "subject": "Amazing Deals on Software Licenses!",
        "email_thread": "Get 50% off on all software licenses this week only! Click here to claim your discount now!"
    },
    {
        "author": "manager@company.com",
        "to": "assistant@company.com",
        "subject": "Project Status Update",
        "email_thread": "Can you provide me with the latest status on Project Alpha? Need it for tomorrow's board meeting."
    },
    {
        "author": "newsletter@tech-updates.com",
        "to": "assistant@company.com",
        "subject": "Weekly Tech Newsletter",
        "email_thread": "This week's top technology news and trends..."
    },
    {
        "author": "colleague@company.com",
        "to": "assistant@company.com",
        "subject": "Auto-reply: Out of Office",
        "email_thread": "Thank you for your email. I am currently out of office and will return on Monday."
    },
    {
        "author": "hr@company.com",
        "to": "assistant@company.com",
        "subject": "Action Required: Complete Annual Review by Friday",
        "email_thread": "Please complete your annual performance review by end of day Friday. This is mandatory for all employees."
    },
]

triage_classifications = [
    "respond",
    "notify",
    "ignore",
    "respond",
    "ignore",
    "ignore",
    "respond",
]

expected_tool_calls = [
    ["search_events", "update_event"],
    [],
    [],
    ["search_emails"],
    [],
    [],
    [],
]

def get_test_email(index: int) -> dict:
    """Get a test email by index.
    
    Args:
        index: Index of the email in test_data
        
    Returns:
        Email dictionary with author, to, subject, and email_thread
    """
    return email_inputs[index]


def get_expected_classification(index: int) -> str:
    """Get expected classification for a test email.
    
    Args:
        index: Index of the email in test_data
        
    Returns:
        Expected classification: "respond", "notify", or "ignore"
    """
    return triage_classifications[index]


def get_expected_tools(index: int) -> list:
    """Get expected tool calls for a test email.
    
    Args:
        index: Index of the email in test_data
        
    Returns:
        List of expected tool names
    """
    return expected_tool_calls[index]


# Create tuples for pytest parametrize
email_classification_pairs = list(zip(email_inputs, triage_classifications))

# Only include emails that should get responses
emails_requiring_response = [
    (email_inputs[i], expected_tool_calls[i])
    for i in range(len(email_inputs))
    if triage_classifications[i] == "respond"
]
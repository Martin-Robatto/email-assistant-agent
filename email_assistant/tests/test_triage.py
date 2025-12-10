"""Tests for email triage classification."""

import pytest
from langsmith import testing as t

from email_assistant.tests.test_data import email_classification_pairs


@pytest.mark.langsmith
@pytest.mark.parametrize("email_input,expected_classification", email_classification_pairs)
def test_triage_classification(email_agent, thread_config, email_input, expected_classification):
    """Test if triage correctly classifies emails.
    
    This test verifies that the triage router accurately classifies emails
    into one of three categories: respond, notify, or ignore.
    
    Args:
        email_agent: The email assistant graph (from fixture)
        thread_config: Thread configuration for stateful execution
        email_input: Email data dictionary with author, to, subject, email_thread
        expected_classification: Expected classification (respond/notify/ignore)
    """
    # Invoke the graph with the email input
    result = email_agent.invoke({"email_input": email_input}, config=thread_config)
    
    # Extract the classification decision
    actual_classification = result.get("classification_decision", "").lower()
    
    # Log results for LangSmith
    t.log_outputs({
        "email_subject": email_input.get("subject"),
        "email_author": email_input.get("author"),
        "expected": expected_classification,
        "actual": actual_classification,
        "match": actual_classification == expected_classification.lower()
    })
    
    # Assert classification matches expected
    assert actual_classification == expected_classification.lower(), (
        f"Expected '{expected_classification}' but got '{actual_classification}' "
        f"for email: {email_input.get('subject')}"
    )


@pytest.mark.langsmith
def test_triage_spam_detection(email_agent, thread_config):
    """Test that spam emails are correctly identified and ignored."""
    spam_emails = [
        {
            "author": "promotions@spam.com",
            "to": "assistant@company.com",
            "subject": "You've won a million dollars!",
            "email_thread": "Click here to claim your prize now!"
        },
        {
            "author": "marketing@ads.com",
            "to": "assistant@company.com",
            "subject": "Limited time offer - 90% OFF!",
            "email_thread": "Don't miss this amazing deal!"
        }
    ]
    
    for email in spam_emails:
        result = email_agent.invoke({"email_input": email}, config=thread_config)
        classification = result.get("classification_decision", "").lower()
        
        t.log_outputs({
            "email_subject": email["subject"],
            "classification": classification
        })
        
        assert classification == "ignore", (
            f"Spam email should be ignored: {email['subject']}"
        )


@pytest.mark.langsmith
def test_triage_urgent_emails(email_agent, thread_config):
    """Test that urgent emails are properly flagged for notification."""
    urgent_emails = [
        {
            "author": "ops@company.com",
            "to": "assistant@company.com",
            "subject": "URGENT: System Alert",
            "email_thread": "Critical system alert requires immediate attention!"
        },
        {
            "author": "security@company.com",
            "to": "assistant@company.com",
            "subject": "Security Breach Detected",
            "email_thread": "Potential security breach detected in production environment."
        }
    ]
    
    for email in urgent_emails:
        result = email_agent.invoke({"email_input": email}, config=thread_config)
        classification = result.get("classification_decision", "").lower()
        
        t.log_outputs({
            "email_subject": email["subject"],
            "classification": classification
        })
        
        # Urgent emails should either be responded to or notified
        assert classification in ["notify", "respond"], (
            f"Urgent email should be 'notify' or 'respond': {email['subject']}"
        )

@pytest.mark.langsmith
def test_triage_returns_valid_classification(email_agent, thread_config):
    """Test that triage always returns one of the valid classifications."""
    test_email = {
        "author": "test@company.com",
        "to": "assistant@company.com",
        "subject": "Test Email",
        "email_thread": "This is a test email."
    }
    
    result = email_agent.invoke({"email_input": test_email}, config=thread_config)
    classification = result.get("classification_decision", "").lower()
    
    valid_classifications = ["respond", "notify", "ignore"]
    assert classification in valid_classifications, (
        f"Classification '{classification}' is not valid. "
        f"Must be one of: {valid_classifications}"
    )
"""Tests for the agent's overall behavior and tool usage."""

import pytest
from langsmith import testing as t

from email_assistant.tests.test_data import emails_requiring_response, get_test_email
from email_assistant.tests.utils import extract_tool_calls, get_missing_tools, format_messages_string


@pytest.mark.langsmith
@pytest.mark.parametrize("email_input,expected_tools", emails_requiring_response)
def test_agent_tool_calling(email_agent, thread_config, email_input, expected_tools):
    """Test if agent calls the expected tools when responding to emails.
    
    This test verifies that the agent invokes the correct tools based on
    the email content and required actions.
    
    Args:
        email_agent: The email assistant graph
        thread_config: Thread configuration for stateful execution
        email_input: Email data dictionary
        expected_tools: List of expected tool names
        quality_criteria: (unused in this test, but part of parametrize)
    """
    # Skip if no tools are expected
    if not expected_tools:
        pytest.skip("No tools expected for this email")
    
    # Invoke the agent
    result = email_agent.invoke({"email_input": email_input}, config=thread_config)
    
    # Extract tool calls from messages
    messages = result.get("messages", [])
    actual_tools = extract_tool_calls(messages)
    missing_tools = get_missing_tools(messages, expected_tools)
    
    # Log results
    t.log_outputs({
        "email_subject": email_input.get("subject"),
        "expected_tools": expected_tools,
        "actual_tools": actual_tools,
        "missing_tools": missing_tools,
        "all_tools_called": len(missing_tools) == 0
    })
    
    # Assert all expected tools were called
    assert len(missing_tools) == 0, (
        f"Missing tool calls for email '{email_input.get('subject')}': {missing_tools}. "
        f"Expected: {expected_tools}, Got: {actual_tools}"
    )


@pytest.mark.langsmith
def test_agent_generates_response(email_agent, thread_config):
    """Test that agent generates a response for emails classified as 'respond'."""
    email_input = get_test_email(0)  # Meeting reschedule email
    
    result = email_agent.invoke({"email_input": email_input}, config=thread_config)
    
    # Check that messages were added
    messages = result.get("messages", [])
    assert len(messages) > 0, "Agent should generate messages when responding"
    
    # Check that there's actual content in the messages
    has_content = any(
        (isinstance(msg, dict) and msg.get("content")) or
        (hasattr(msg, 'content') and msg.content)
        for msg in messages
    )
    
    t.log_outputs({
        "email_subject": email_input.get("subject"),
        "message_count": len(messages),
        "has_content": has_content,
        "messages_preview": format_messages_string(messages[:3])  # First 3 messages
    })
    
    assert has_content, "Agent response should contain actual content"


@pytest.mark.langsmith
def test_agent_does_not_respond_to_ignored_emails(email_agent, thread_config):
    """Test that agent doesn't generate responses for emails classified as 'ignore'."""
    spam_email = get_test_email(2)  # Spam email
    
    result = email_agent.invoke({"email_input": spam_email}, config=thread_config)
    
    classification = result.get("classification_decision", "").lower()
    messages = result.get("messages", [])
    
    t.log_outputs({
        "email_subject": spam_email.get("subject"),
        "classification": classification,
        "message_count": len(messages)
    })
    
    # Should be classified as ignore
    assert classification == "ignore", "Spam should be ignored"
    
    # Should not have generated response messages
    assert len(messages) == 0 or all(
        not ((isinstance(msg, dict) and msg.get("content")) or (hasattr(msg, 'content') and msg.content))
        for msg in messages
    ), "Ignored emails should not generate responses"

@pytest.mark.langsmith
def test_agent_handles_multiple_emails(email_agent):
    """Test that agent can process multiple emails sequentially."""
    test_emails = [get_test_email(i) for i in [0, 3, 4]]  # Mix of email types
    
    results = []
    for email in test_emails:
        # Use different thread_id for each to avoid state conflicts
        config = {"configurable": {"thread_id": f"test-{email['subject'][:10]}"}}
        result = email_agent.invoke({"email_input": email}, config=config)
        results.append(result)
    
    assert len(results) == len(test_emails), "Should process all emails"
    
    # All should have classifications
    for i, result in enumerate(results):
        assert "classification_decision" in result, (
            f"Email {i} should have classification"
        )


@pytest.mark.langsmith
def test_agent_meeting_request_handling(email_agent, thread_config):
    """Test specific behavior for meeting requests."""
    meeting_email = get_test_email(0)  # Meeting reschedule request
    
    result = email_agent.invoke({"email_input": meeting_email}, config=thread_config)
    
    classification = result.get("classification_decision", "").lower()
    messages = result.get("messages", [])
    tools_called = extract_tool_calls(messages)
    
    t.log_outputs({
        "email_subject": meeting_email.get("subject"),
        "classification": classification,
        "tools_called": tools_called,
        "response": format_messages_string(messages)
    })
    
    # Should be classified as respond
    assert classification == "respond", "Meeting requests should get responses"
    
    # Should call event-related tools
    event_tools = ["search_events", "update_event", "create_event"]
    has_event_tool = any(tool in tools_called for tool in event_tools)
    
    assert has_event_tool, (
        f"Should call at least one event tool for meeting requests. "
        f"Tools called: {tools_called}"
    )
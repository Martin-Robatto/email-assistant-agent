"""Pytest configuration and fixtures."""

import pytest
import uuid
from email_assistant.agent import graph


@pytest.fixture
def email_agent():
    """Fixture to provide the email assistant graph.
    
    Returns:
        Compiled LangGraph graph instance
    """
    return graph


@pytest.fixture
def thread_config():
    """Fixture to provide thread configuration for stateful execution.
    
    Each test gets a unique thread_id to avoid state contamination.
    
    Returns:
        Configuration dict with unique thread_id
    """
    return {"configurable": {"thread_id": f"test-thread-{uuid.uuid4()}"}}
"""Test script for HITL implementation."""

import uuid
from langgraph.checkpoint.memory import MemorySaver
from email_assistant_hitl.agent import create_graph

email_input = {
    "to": "John Doe <john.doe@company.com>",
    "author": "Alice Smith <alice.smith@company.com>",
    "subject": "Quick question about API documentation",
    "email_thread": (
        "Hi John,\n\n"
        "I was reviewing the API documentation for the new authentication service "
        "and noticed a few endpoints seem to be missing from the specs. "
        "Could you help clarify if this was intentional or if we should update the docs?\n\n"
        "Specifically, I'm looking at:\n"
        "- /auth/refresh\n"
        "- /auth/validate\n\n"
        "Thanks!\n"
        "Alice"
    )
}

thread_id = uuid.uuid4()
thread_config = {"configurable": {"thread_id": thread_id}}

# Create the graph with a memory saver for local testing
graph = create_graph(checkpointer=MemorySaver())

response = graph.invoke({"email_input": email_input}, config=thread_config)
print("\nGraph execution completed.")
print("Response:", response["messages"])
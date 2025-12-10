"""Test script for HITL implementation."""

import uuid
from email_assistant_hitl import graph

# Test email that should trigger HITL
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

# Create a thread config
thread_id = uuid.uuid4()
thread_config = {"configurable": {"thread_id": thread_id}}

print("Testing HITL Email Assistant")
print("=" * 50)
print("\nStarting graph execution...")
print("This will pause at interrupts for human review.")
print("\nTo test with LangGraph Studio:")
print("1. Run: langgraph dev")
print("2. Select 'agent_hitl' in Studio")
print("3. Submit the email input above")
print("\nOr connect to Agent Inbox at: https://dev.agentinbox.ai/")
print("  - Graph name: agent_hitl")
print("  - Graph URL: http://127.0.0.1:2024/")
print("\n" + "=" * 50)

# To run this interactively, you would use:
# for chunk in graph.stream({"email_input": email_input}, config=thread_config):
#     if '__interrupt__' in chunk:
#         print("\n🛑 INTERRUPT DETECTED!")
#         print(f"Interrupt details: {chunk['__interrupt__']}")

response = graph_hitl.invoke({"email_input": email_input}, config=thread_config)
print("\nGraph execution completed.")
print("Response:", response["messages"])
"""Test script for HITL implementation."""

import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uuid
from langgraph.checkpoint.memory import MemorySaver
from email_assistant_hitl.agent import create_graph
from langgraph.types import Command
from langgraph.types import Command

email_input = {
    "to": "Martin Robatto <martin.robatto@company.com>",
    "author": "Sarah Jenkins <sarah.jenkins@company.com>",
    "subject": "Sensitive: Meeting Request regarding Q4 Review",
    "email_thread": (
        "Hi Martin,\n\n"
        "I need to discuss some sensitive matters regarding the upcoming Q4 performance reviews "
        "and potential restructuring in the engineering team. This is not something I can "
        "discuss over email or Slack.\n\n"
        "Can you please make time for a 30-minute private meeting tomorrow morning?\n"
        "It is rather urgent.\n\n"
        "Best,\n"
        "Sarah"
    )
}

thread_id = uuid.uuid4()
thread_config = {"configurable": {"thread_id": thread_id}}

# Create the graph with a memory saver for local testing
graph = create_graph(checkpointer=MemorySaver())

response = graph.invoke({"email_input": email_input}, config=thread_config)

# Loop to handle multiple interrupts (e.g. Triage -> Action Review)
while True:
    # Check state after invoke/resume
    state = graph.get_state(thread_config)

    if not state.next:
        print("\n✅ Graph finished.")
        print("Result:", state.values["messages"][-1].content)
        break

    print(f"\n⏸️ Graph paused at: {state.next}")
    
    if state.tasks and state.tasks[0].interrupts:
        print("\n🔔 Interrupt caught!")
        interrupt_value = state.tasks[0].interrupts[0].value
        print("Interrupt payload:", interrupt_value)
        
        print("\n👇 ENTER YOUR ACTION BELOW 👇")
        print("Options: 'response <text>', 'accept', 'ignore'")
        print("Tip: Type 'schedule meeting for tomorrow at 10am' to test the flow")
        user_input_raw = input("Your action: ")
        print(f"DEBUG: You entered '{user_input_raw}'")
        
        
        if user_input_raw.lower() == "accept":
             resume_payload = {"type": "accept"}
        elif user_input_raw.lower() == "ignore":
             resume_payload = {"type": "ignore"}
        else:
             # Default to response
             text = user_input_raw.replace("response ", "", 1) if user_input_raw.startswith("response") else user_input_raw
             resume_payload = {
                "type": "response",
                "args": text
             }
        
        print(f"\n▶️ Resuming with: {resume_payload}...")
        
        # Resume the graph
        res = graph.invoke(
            Command(resume=[resume_payload]), 
            config=thread_config
        )
        print("DEBUG: Resume complete.")
    else:
        # If paused but no interrupt, it might be a breakpoint or just end of step
        # Just continue to next step (shouldn't happen in this graph config but good safety)
        print("Paused but no interrupt details found. Stopping.")
        break
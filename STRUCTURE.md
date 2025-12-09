# Email Assistant Project Structure

This document describes the organized structure of the email assistant project.

## Directory Structure

```
email-assistant/
├── __init__.py                 # Package initialization, exports graph
├── agent.py                    # Graph construction with triage router
├── utils/                      # Utilities for the agent graph
│   ├── __init__.py            # Exports all utilities
│   ├── state.py               # State definition with email_input and classification
│   ├── nodes.py               # Node functions (triage_router, agent_node, tool_node)
│   ├── tools.py               # Tools (write_email, schedule_meeting, etc.)
│   ├── router.py              # RouterSchema and LLM initialization
│   ├── helpers.py             # Helper functions (parse_email, format_email_markdown)
│   └── prompts.py             # Prompt templates for triage
├── .env                        # Environment variables
├── langgraph.json             # LangGraph configuration
└── requirements.txt           # Package dependencies
```

## File Descriptions

### Core Files

- **[`agent.py`](email-assistant/agent.py:1)**: Constructs the LangGraph workflow with nodes for triage routing, response generation, and tool execution.

- **[`utils/state.py`](email-assistant/utils/state.py:1)**: Defines the `State` class that extends `MessagesState` with:
  - `email_input`: Dictionary containing email data
  - `classification_decision`: Literal type for "ignore", "respond", or "notify"

### Node Functions

- **[`utils/nodes.py`](email-assistant/utils/nodes.py:1)**: Contains node functions:
  - `triage_router()`: Analyzes emails and routes them based on classification
  - `agent_node()`: Main agent processing node
  - `tool_node()`: Executes tools

### Supporting Modules

- **[`utils/router.py`](email-assistant/utils/router.py:1)**: 
  - `RouterSchema`: Pydantic model for structured output with reasoning and classification
  - `llm_router`: Initialized LLM with structured output

- **[`utils/helpers.py`](email-assistant/utils/helpers.py:1)**:
  - `parse_email()`: Extracts email components from input dictionary
  - `format_email_markdown()`: Formats email as markdown

- **[`utils/prompts.py`](email-assistant/utils/prompts.py:1)**:
  - System and user prompts for email triage
  - Default background and instructions

- **[`utils/tools.py`](email-assistant/utils/tools.py:1)**:
  - `write_email()`: Tool for sending emails
  - `schedule_meeting()`: Tool for scheduling meetings
  - `check_calendar_availability()`: Tool for checking calendar
  - `Done`: Completion marker

## Graph Flow

1. **START** → `triage_router`
2. `triage_router` analyzes email and routes to:
   - `response_agent` (if classification = "respond")
   - `__end__` (if classification = "ignore" or "notify")
3. `response_agent` → `tools` → **END**

## Key Features

- **Email Classification**: Automatically categorizes emails as ignore, notify, or respond
- **Structured Output**: Uses Pydantic models for type-safe LLM responses
- **Modular Design**: Separated concerns across multiple files
- **Tool Integration**: Ready for email sending and calendar management
- **State Management**: Tracks email data and classification decisions
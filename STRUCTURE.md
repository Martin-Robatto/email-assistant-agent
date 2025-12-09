# Email Assistant Project Structure

This document describes the refactored project structure with organized folders for better maintainability.

## Project Layout

```
email_assistant/
├── __init__.py              # Main package exports
├── agent.py                 # Graph construction and compilation
│
├── nodes/                   # Graph nodes (one file per node)
│   ├── __init__.py         # Node exports
│   ├── triage_router.py    # Email classification node
│   ├── agent_node.py       # Agent reasoning node (LLM + tools)
│   ├── tool_node.py        # Tool execution node
│   └── routing.py          # Routing functions (should_respond, should_continue)
│
├── prompts/                 # Prompt templates
│   ├── __init__.py         # Prompt exports
│   ├── defaults.py         # Default configuration values
│   ├── triage_prompts.py   # Triage classification prompts
│   └── agent_prompts.py    # Agent response generation prompts
│
├── tools/                   # LangChain tools
│   ├── __init__.py         # Tool exports
│   ├── email_tools.py      # Email-related tools (write_email)
│   └── calendar_tools.py   # Calendar tools (schedule_meeting, check_availability)
│
├── helpers/                 # Helper utilities
│   ├── __init__.py         # Helper exports
│   ├── email_parser.py     # Email parsing functions
│   └── email_formatter.py  # Email formatting functions
│
└── utils/                   # Core utilities
    ├── __init__.py         # Utility exports
    ├── state.py            # Graph state definition
    └── router.py           # LLM initialization and routing schema
```

## Architecture Overview

### Graph Flow

1. **START** → `triage_router` → Classifies email (respond/notify/ignore)
2. `triage_router` → `agent` (if respond) or **END** (if notify/ignore)
3. `agent` → LLM reasoning (decides which tools to call)
4. `agent` → `tools` (if tool calls exist) or **END** (if done)
5. `tools` → Executes tools → back to `agent` (ReAct loop)
6. Loop continues until agent marks task as complete

### Key Components

#### Nodes (`email_assistant/nodes/`)
- **`triage_router.py`**: Analyzes incoming emails and classifies them
- **`agent_node.py`**: Main reasoning node where LLM decides actions
- **`tool_node.py`**: Executes tools (email sending, calendar operations)
- **`routing.py`**: Contains routing logic for conditional edges

#### Prompts (`email_assistant/prompts/`)
- **`defaults.py`**: Default configuration values (background, preferences)
- **`triage_prompts.py`**: Prompts for email classification
- **`agent_prompts.py`**: Prompts for response generation

#### Tools (`email_assistant/tools/`)
- **`email_tools.py`**: Email operations (write_email)
- **`calendar_tools.py`**: Calendar operations (schedule_meeting, check_availability)

#### Helpers (`email_assistant/helpers/`)
- **`email_parser.py`**: Parse email data structures
- **`email_formatter.py`**: Format emails as markdown

#### Utils (`email_assistant/utils/`)
- **`state.py`**: GraphState definition (extends MessagesState)
- **`router.py`**: LLM instances (llm_router, llm_with_tools) and RouterSchema

## Benefits of This Structure

1. **Modularity**: Each component has a single responsibility
2. **Scalability**: Easy to add new nodes, tools, or prompts
3. **Maintainability**: Clear organization makes code easier to understand
4. **Testability**: Individual components can be tested in isolation
5. **Reusability**: Components can be imported and used independently

## Usage

```python
from email_assistant import graph

# Run the email assistant
result = graph.invoke(
    {"email_input": email_data},
    config={"configurable": {"thread_id": "test-1"}}
)
```

## Adding New Components

### Adding a New Node
1. Create `email_assistant/nodes/new_node.py`
2. Implement node function(s)
3. Export in `email_assistant/nodes/__init__.py`
4. Wire it in `email_assistant/agent.py`

### Adding a New Tool
1. Create tool in appropriate file under `email_assistant/tools/`
2. Export in `email_assistant/tools/__init__.py`
3. Add to tools list in `email_assistant/nodes/tool_node.py`
4. Update `email_assistant/utils/router.py` tool bindings if needed

### Adding New Prompts
1. Add prompts to appropriate file under `email_assistant/prompts/`
2. Export in `email_assistant/prompts/__init__.py`
3. Use in relevant node files

## Model Configuration

- **gpt-4o-mini**: Used for triage (fast, cheap classification)
- **gpt-4o**: Used for agent reasoning (quality responses, reliable tool calling)

See `email_assistant/utils/router.py` for model initialization.
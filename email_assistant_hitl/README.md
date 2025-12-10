# Email Assistant with Human-in-the-Loop (HITL)

This is a separate, self-contained package that implements the email assistant with Human-in-the-Loop features.

## Structure

```
email_assistant_hitl/
├── __init__.py          # Package exports
├── agent.py             # Main graph definition (uses conditional edges)
├── helpers/             # Email parsing and formatting
├── nodes/               # Graph nodes (triage, agent, interrupt handlers)
├── prompts/             # System and user prompts
├── tools/               # Tools (including Question and Done)
└── utils/               # State and router configuration
```

## Key Differences from Regular Email Assistant

| Feature | email_assistant | email_assistant_hitl |
|---------|----------------|---------------------|
| Tools | 6 standard tools | 8 tools (+ Question, Done) |
| Interrupts | None | Triage + Tool call interrupts |
| User control | Fully autonomous | Supervised with approval |
| Graph nodes | 3 nodes | 4 nodes |
| Routing | Conditional edges | Conditional edges |
| LLM binding | Standard | tool_choice="required" |

## Usage

### Import the graph

```python
from email_assistant_hitl import graph
```

### Run with LangGraph Studio

1. Start: `langgraph dev`
2. Select `agent_hitl` in the dropdown
3. Submit email input
4. Review interrupts and respond

### Connect to Agent Inbox

1. Go to: https://dev.agentinbox.ai/
2. Connect with:
   - Graph name: `agent_hitl`
   - Graph URL: `http://127.0.0.1:2024/`

## Graph Flow (All Conditional Edges)

The graph uses conditional edges throughout for clear routing:

```
START → triage_router
         ↓
    (classification?)
         ↓
    ├─ respond → agent ←──┐
    ├─ notify → triage_   │
    │           interrupt_ │
    │           handler    │
    │              ↓       │
    │         (user?)      │
    │              ↓       │
    │         respond      │
    │           or         │
    │          END         │
    └─ ignore → END        │
                           │
    agent → (Done tool?)   │
         ↓                 │
    ├─ No → interrupt_    │
    │       handler ───────┘
    └─ Yes → END
```

## Nodes

1. **triage_router** - Classifies emails (respond/notify/ignore)
2. **triage_interrupt_handler** - Handles "notify" interrupts
3. **agent** - LLM reasoning with HITL tools
4. **interrupt_handler** - Reviews tool calls before execution

## Conditional Edge Functions

1. **should_respond** - Routes from triage_router based on classification
2. **should_continue_after_triage_interrupt** - Routes from triage_interrupt_handler based on user response
3. **should_continue_agent** - Routes from agent based on Done tool check

## Tools Requiring Human Review

- `write_email` - Before sending emails
- `schedule_meeting` - Before scheduling meetings
- `Question` - When asking user questions

## Response Types

Users can respond to interrupts with:
- **accept** - Execute as proposed
- **edit** - Modify details before execution
- **respond** - Provide feedback for redraft
- **ignore** - Cancel the action

## Configuration

The package is configured in `langgraph.json`:

```json
{
  "graphs": {
    "agent_hitl": "./email_assistant_hitl/agent.py:graph"
  }
}
```

## Data Flow

1. Email input → **triage_router**
2. Conditional edge:
   - If "respond" → **agent**
   - If "notify" → **triage_interrupt_handler** → PAUSE → conditional edge: respond → **agent** or ignore → END
   - If "ignore" → END
3. **Agent** proposes tools → conditional edge: check for Done tool
4. If not Done → **interrupt_handler** → PAUSE → loop back to **agent**
5. If Done → END

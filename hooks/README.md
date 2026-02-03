# ADX Toolkit Hooks

Hooks extend Claude Code by running scripts at specific events. All hooks are registered in `settings.json`.

## Prerequisites

- Python 3.8+ (3.11+ recommended)
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Hook Events

| Event | When | Purpose |
|-------|------|---------|
| `UserPromptSubmit` | User sends a message | Inject context, detect patterns |
| `PreToolUse` | Before tool execution | Monitor, validate |
| `PostToolUse` | After tool execution | Track, log |
| `Stop` | Conversation ends | Persist state, cleanup |
| `SubagentStop` | Subagent completes | Track subagent results |
| `PreCompact` | Before context compaction | Preserve important info |
| `Notification` | System notifications | Desktop alerts |

## Hooks Reference

### UserPromptSubmit Hooks

| Hook | Purpose | Output |
|------|---------|--------|
| `dev_standards_loader.py` | Load CLAUDE.md standards | Context injection |
| `context_loader.py` | Load session context from `.claude/context/` | Context injection |
| `state_loader.py` | Load state tracking from `.claude/state/` | State banner |
| `smart_context_loader.py` | Detect task type, suggest skills | Context hints |
| `skill-activation-prompt.py` | Auto-activate skills for detected patterns | Skill injection |
| `circuit_breaker.py` | Detect repeated failures, suggest alternatives | Warning banner |
| `ship_loader.py` | Inject /ship workflow state | Phase tracking |
| `checkpoint.py` | Handle `--status`, `--continue`, `--rollback` flags | Checkpoint info |
| `user_prompt_submit.py` | Log prompts (with `--log-only`) | Session log |
| `knowledge_loader.py` | Semantic knowledge retrieval | Knowledge injection |

### Stop Hooks

| Hook | Purpose | Output |
|------|---------|--------|
| `context_updater.py` | Save session context to `.claude/context/` | Persisted context |
| `cost_tracker.py` | Track token usage and costs | Cost log |
| `memory_updater.py` | Prompt for memory updates after significant work | Memory prompt |
| `state_updater.py` | Update state tracking files | Persisted state |
| `ship_updater.py` | Update /ship workflow state | Ship log |
| `stop.py` | Chat completion, summary generation | Session summary |
| `knowledge_ingestor.py` | Extract and store learned knowledge | New fragments |

### Other Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `pre_tool_use.py` | PreToolUse | Tool execution monitoring |
| `post_tool_use.py` | PostToolUse | Tool result tracking |
| `subagent_stop.py` | SubagentStop | Subagent result aggregation |
| `pre_compact.py` | PreCompact | Context preservation |
| `notification.py` | Notification | Desktop notifications |

### Standalone Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `ship_state.py` | Ship state CLI | `uv run hooks/ship_state.py start/phase_done/status/abort` |

## Utilities (`hooks/utils/`)

| Module | Purpose |
|--------|---------|
| `constants.py` | Shared paths, session management |
| `knowledge_store.py` | TF-IDF indexed fragment storage |
| `knowledge_retriever.py` | Context-aware knowledge retrieval |
| `llm/oai.py` | OpenAI API wrapper |
| `llm/anth.py` | Anthropic API wrapper |

## Directory Structure

```
hooks/
├── checkpoint.py             # Ship checkpoint management
├── circuit_breaker.py        # Failure detection and recovery
├── context_loader.py         # Session context injection
├── context_updater.py        # Session context persistence
├── cost_tracker.py           # Usage and cost tracking
├── dev_standards_loader.py   # CLAUDE.md standards loading
├── knowledge_loader.py       # Knowledge retrieval
├── knowledge_ingestor.py     # Knowledge extraction
├── memory_updater.py         # Memory update prompts
├── notification.py           # Desktop notifications
├── post_tool_use.py          # Post-tool logging
├── pre_tool_use.py           # Pre-tool logging
├── pre_compact.py            # Context compaction handler
├── ship_loader.py            # /ship state injection
├── ship_state.py             # Ship state CLI
├── ship_updater.py           # /ship state persistence
├── skill-activation-prompt.py # Skill detection
├── smart_context_loader.py   # Context pattern detection
├── state_loader.py           # State tracking injection
├── state_updater.py          # State tracking persistence
├── stop.py                   # Session stop handler
├── subagent_stop.py          # Subagent stop handler
├── user_prompt_submit.py     # Prompt logging
├── utils/
│   ├── constants.py          # Shared constants
│   ├── knowledge_store.py    # TF-IDF fragment storage
│   ├── knowledge_retriever.py # Knowledge retrieval engine
│   └── llm/
│       ├── anth.py           # Anthropic API helper
│       └── oai.py            # OpenAI API helper
└── README.md
```

## Error Handling Pattern

All hooks follow the same pattern:

```python
def main():
    try:
        input_data = json.load(sys.stdin)
        # ... hook logic ...
        sys.exit(0)
    except Exception:
        sys.exit(0)  # Never block Claude
```

External registration uses `|| true`:
```json
{
  "type": "command",
  "command": "uv run hooks/my_hook.py || true"
}
```

## Data Flow

```
User Prompt
     │
     ▼
UserPromptSubmit hooks
     │ (context injection)
     ▼
Claude processes
     │
     ▼
PreToolUse → Tool → PostToolUse
     │
     ▼
Stop hooks
     │ (persistence)
     ▼
Session End
```

## Logging

Hooks log to `logs/{session_id}/` directory, creating JSON files for each event type:
- `user_prompt_submit.json`
- `skill_activation.json`
- `pre_tool_use.json`
- `post_tool_use.json`
- `notification.json`
- `stop.json`
- `subagent_stop.json`
- `pre_compact.json`
- `chat.json` (when `--chat` flag is used)
- `smart_context.json`
- `cost_tracking.json`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_HOOKS_LOG_DIR` | Base directory for logs | `logs` |
| `CLAUDE_PROJECT_DIR` | Project directory for skill rules | `~/project` |
| `ANTHROPIC_API_KEY` | API key for Anthropic LLM helpers | - |
| `OPENAI_API_KEY` | API key for OpenAI LLM helpers | - |
| `ENGINEER_NAME` | Name for personalized messages | - |

## Command Line Options

### user_prompt_submit.py
- `--validate` - Enable prompt validation against blocked patterns
- `--log-only` - Only log prompts, no validation

### stop.py / subagent_stop.py
- `--chat` - Save conversation transcript
- `--summary` - Generate session summary

### notification.py
- `--notify` - Enable desktop notifications

## Adding a New Hook

1. Create `hooks/my_hook.py` with the standard pattern
2. Register in `settings.json` under the appropriate event
3. Use `|| true` suffix for silent failures
4. Read JSON from stdin, print output to stdout

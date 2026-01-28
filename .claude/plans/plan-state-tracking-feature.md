# Implementation Plan: STATE Tracking Feature

## Overview

Add persistent STATE tracking to ADX toolkit as an **optional feature** during setup. This enables persistent progress tracking, session handoffs, and "Where am I? What's next?" awareness across sessions.

## Research Summary

### GSD's STATE System
- **STATE.md** - Decisions, blockers, current position (always loaded)
- **ROADMAP.md** - Phases with completion status
- **REQUIREMENTS.md** - Scoped v1/v2/vN requirements
- **PROJECT.md** - Project vision and context
- Commands: `/gsd:pause-work`, `/gsd:resume-work`, `/gsd:progress`

### ADX Current State
- Already has: `session_context.json`, checkpoints, memory system
- Missing: Formal phase tracking, pause/resume, progress command

---

## Implementation Tasks

### 1. Create State Templates

**Files to create in `state/` directory:**

#### `state/PROJECT.md`
```markdown
# Project: [Project Name]

## Vision
[One paragraph describing what this project does and why]

## Tech Stack
- Frontend: [framework]
- Backend: [framework]
- Database: [type]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Out of Scope
- [What this project will NOT do]
```

#### `state/STATE.md`
```markdown
# Current State

## Position
- **Current Phase:** [Phase number and name]
- **Current Task:** [What's being worked on]
- **Last Updated:** [ISO timestamp]

## Decisions Made
| Decision | Rationale | Date |
|----------|-----------|------|
| [Decision] | [Why] | [Date] |

## Blockers
- [ ] [Blocker 1]
- [ ] [Blocker 2]

## Context for Next Session
[What Claude needs to know to continue]
```

#### `state/ROADMAP.md`
```markdown
# Roadmap

## Current Milestone: [Name]

### Phase 1: [Name]
- [ ] Task 1.1
- [ ] Task 1.2
Status: `pending` | `in_progress` | `completed`

### Phase 2: [Name]
- [ ] Task 2.1
Status: `pending`

## Completed Phases
- [x] Phase 0: Initial Setup (2024-01-15)
```

#### `state/REQUIREMENTS.md`
```markdown
# Requirements

## v1 (MVP)
- [ ] [Core feature 1]
- [ ] [Core feature 2]

## v2 (Enhanced)
- [ ] [Enhancement 1]
- [ ] [Enhancement 2]

## Future / Out of Scope
- [ ] [Future feature]
```

---

### 2. Create New Commands

#### `commands/progress.md`
Shows current position and next action by reading STATE.md and ROADMAP.md.

```markdown
# /adx:progress

## Purpose
Answer "Where am I? What's next?" by reading state files.

## Output
- Current phase and task
- Completion percentage
- Next recommended action
- Any blockers
```

#### `commands/pause.md`
Create handoff documentation when stopping mid-work.

```markdown
# /adx:pause

## Purpose
Save session state for seamless resume later.

## Actions
1. Read current work context
2. Update STATE.md with:
   - Current position
   - Work in progress
   - Context for next session
3. Commit state changes (optional)
```

#### `commands/resume.md`
Restore from last session.

```markdown
# /adx:resume

## Purpose
Continue where you left off.

## Actions
1. Read STATE.md and ROADMAP.md
2. Show last session summary
3. Suggest next action
```

#### `commands/init-state.md`
Initialize state tracking for an existing project.

```markdown
# /adx:init-state

## Purpose
Set up state tracking for a project interactively.

## Flow
1. Ask about project vision
2. Define initial phases/milestones
3. Scope v1 requirements
4. Create state files
```

---

### 3. Create Hooks

#### `hooks/state_loader.py`
Load STATE.md content on session start.

```python
#!/usr/bin/env python3
"""Load project state on session start."""

import json
from pathlib import Path

def main():
    state_file = Path(".claude/state/STATE.md")
    roadmap_file = Path(".claude/state/ROADMAP.md")

    if not state_file.exists():
        return  # State tracking not enabled

    context_parts = []

    if state_file.exists():
        context_parts.append(f"<project-state>\n{state_file.read_text()}\n</project-state>")

    if roadmap_file.exists():
        context_parts.append(f"<project-roadmap>\n{roadmap_file.read_text()}\n</project-roadmap>")

    if context_parts:
        print(json.dumps({
            "message": "\n\n".join(context_parts)
        }))

if __name__ == "__main__":
    main()
```

#### `hooks/state_updater.py`
Prompt to update STATE.md on session end.

```python
#!/usr/bin/env python3
"""Update project state on session end."""

import json
from pathlib import Path
from datetime import datetime

def main():
    state_file = Path(".claude/state/STATE.md")

    if not state_file.exists():
        return

    print(json.dumps({
        "message": """
<state-update-reminder>
Before ending this session, consider updating your project state:
- What phase/task are you on?
- Any decisions made?
- Any blockers discovered?
- What context does the next session need?

Use `/adx:pause` to save your progress, or manually update .claude/state/STATE.md
</state-update-reminder>
"""
    }))

if __name__ == "__main__":
    main()
```

---

### 4. Update setup.sh

Add state tracking as optional feature in Step 3:

```bash
# In ask_features() function, add:

# State Tracking
echo -e "${CYAN}State Tracking${NC} - persistent progress tracking (phases, decisions, blockers)"
INSTALL_STATE=$(ask_yes_no "  Install state tracking?" "no")
[ "$INSTALL_STATE" = "yes" ] && success "State: enabled" || info "State: disabled"
echo ""
```

Add installation logic:

```bash
# In install_files() function, add:

# Install state tracking
if [ "$INSTALL_STATE" = "yes" ]; then
    mkdir -p "$PROJECT_DIR/.claude/state"
    cp -r "$SCRIPT_DIR/state/"* "$PROJECT_DIR/.claude/state/" 2>/dev/null || true
    success "Installed state tracking templates"
fi
```

Update settings.json to include state hooks when enabled.

---

### 5. Update settings.json Template

Add state-related hooks to the default configuration:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "python3 .claude/hooks/state_loader.py",
        "condition": "test -f .claude/state/STATE.md"
      }
    ],
    "Stop": [
      {
        "command": "python3 .claude/hooks/state_updater.py",
        "condition": "test -f .claude/state/STATE.md"
      }
    ]
  }
}
```

---

## File Structure After Implementation

```
adx-toolkit/
├── state/                      # NEW: State templates
│   ├── PROJECT.md
│   ├── STATE.md
│   ├── ROADMAP.md
│   └── REQUIREMENTS.md
├── commands/
│   ├── progress.md             # NEW
│   ├── pause.md                # NEW
│   ├── resume.md               # NEW
│   └── init-state.md           # NEW
├── hooks/
│   ├── state_loader.py         # NEW
│   └── state_updater.py        # NEW
└── setup.sh                    # MODIFIED
```

---

## Implementation Order

1. **Create state templates** (`state/` directory)
2. **Create hooks** (`state_loader.py`, `state_updater.py`)
3. **Create commands** (`progress.md`, `pause.md`, `resume.md`, `init-state.md`)
4. **Update setup.sh** (add state option)
5. **Update plugin.json** (register new commands)
6. **Test end-to-end**

---

## Usage After Implementation

```bash
# During setup (new option)
./setup.sh
# Step 3 now includes: "State Tracking - persistent progress tracking? [y/N]"

# Initialize state for existing project
/adx:init-state

# Check progress
/adx:progress
# Output: "Phase 2/5: User Authentication | 40% complete | Next: Implement JWT tokens"

# Before ending session
/adx:pause
# Saves current context to STATE.md

# Starting new session
/adx:resume
# Shows last session context and suggests next action
```

---

## Integration with Existing Features

- **Works with `/ship`**: Progress command reads checkpoint status
- **Works with `/plan`**: Plans link to ROADMAP phases
- **Works with memory system**: Decisions in STATE.md complement decisions.md
- **Non-breaking**: Optional feature, existing projects unaffected

---

## Differences from GSD

| Feature | GSD | ADX Implementation |
|---------|-----|-------------------|
| Location | `.planning/` | `.claude/state/` |
| Phase planning | `/gsd:discuss-phase` | Manual or `/plan` |
| Research | Parallel agents | `/adx:discover` |
| Execution | Wave-based | `/ship` pipeline |

ADX adapts the STATE concept while keeping its own workflow intact.

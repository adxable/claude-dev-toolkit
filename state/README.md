# State Tracking

Persistent progress tracking for long-running projects. Maintains continuity across sessions with phase-based roadmaps, decision logs, and session handoffs.

## Files

| File | Purpose |
|------|---------|
| `PROJECT.md` | Project vision, tech stack, constraints |
| `STATE.md` | Current position, decisions, blockers |
| `ROADMAP.md` | Phases with tasks and progress |
| `REQUIREMENTS.md` | Scoped v1/v2/vN requirements |

## Commands

| Command | Description |
|---------|-------------|
| `/adx:init-state` | Initialize state tracking interactively |
| `/adx:progress` | Show current position and next action |
| `/adx:pause` | Save session state before ending |
| `/adx:resume` | Restore context from last session |

## Quick Start

1. Run `/adx:init-state` to set up your project
2. Work normally - state is loaded automatically
3. Before ending, run `/adx:pause` to save context
4. Next session, run `/adx:resume` to continue

## How It Works

**On session start:**
- `state_loader.py` hook injects STATE.md and ROADMAP.md into context
- Claude knows your current position and recent decisions

**On session end:**
- `state_updater.py` hook reminds you to save progress
- `/adx:pause` captures work-in-progress context

**Checking progress:**
- `/adx:progress` reads all state files
- Shows completion %, blockers, and next actions

## Integration

Works alongside existing ADX features:
- **Memory system** - decisions.md complements STATE.md
- **Checkpoints** - `/ship` checkpoints are separate from state
- **Plans** - `.claude/plans/` can reference ROADMAP phases

## Example Workflow

```bash
# Start of project
/adx:init-state
# > Set up project vision, phases, requirements

# During development
/adx:progress
# > Phase 2/4 - User Auth | 40% complete | Next: JWT implementation

# Before ending session
/adx:pause
# > Saved: Working on JWT refresh tokens, decided on 7-day expiry

# Next day
/adx:resume
# > Context restored: Continue JWT refresh token implementation
```

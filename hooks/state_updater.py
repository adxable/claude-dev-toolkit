#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Remind to update project state on session end.

Prompts the user to save their progress before ending the session,
ensuring continuity across context windows.
"""

import json
import sys
from pathlib import Path


def check_state_initialized() -> bool:
    """Check if state files have been initialized (not just templates)."""
    state_file = Path(".claude/state/STATE.md")
    if not state_file.exists():
        return False

    content = state_file.read_text()
    # Check if it's still the template
    return "[Phase number" not in content


def main():
    """Main entry point."""
    state_dir = Path(".claude/state")

    # Only run if state tracking is enabled
    if not state_dir.exists():
        return

    # Check if state has been initialized
    if not check_state_initialized():
        print(json.dumps({
            "message": """
<state-reminder>
State tracking is enabled but not yet initialized.
Run `/adx:init-state` to set up project tracking, or manually edit:
- .claude/state/PROJECT.md - Project vision
- .claude/state/STATE.md - Current position
- .claude/state/ROADMAP.md - Phases and progress
</state-reminder>
"""
        }))
        return

    # Remind to update state
    print(json.dumps({
        "message": """
<state-update-reminder>
Before ending this session, consider saving your progress:

**Quick save:** Run `/adx:pause` to capture current context

**Manual update:** Edit `.claude/state/STATE.md`:
- Current phase/task position
- Decisions made this session
- Blockers discovered
- Context needed for next session
</state-update-reminder>
"""
    }))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Update ship state on session end.

Reminds to save progress and provides state management utilities.
This hook runs on Stop events.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

SHIP_STATE_FILE = Path(".claude/ship/current.json")
SHIP_DIR = Path(".claude/ship")

PHASES = ["plan", "implement", "verify", "review", "commit", "pr"]


def load_ship_state() -> Optional[dict]:
    """Load active ship state if it exists."""
    if not SHIP_STATE_FILE.exists():
        return None
    try:
        return json.loads(SHIP_STATE_FILE.read_text())
    except (json.JSONDecodeError, IOError):
        return None


def get_incomplete_phase(state: dict) -> Optional[str]:
    """Get the current incomplete phase."""
    phases = state.get("phases", {})
    current = state.get("current_phase", "plan")

    current_data = phases.get(current, {})
    if current_data.get("status") != "done":
        return current

    return None


def format_progress_reminder(state: dict) -> str:
    """Format a reminder about ship progress."""
    description = state.get("description", "unknown")
    current = state.get("current_phase", "plan")
    ship_id = state.get("id", "unknown")

    phases = state.get("phases", {})
    completed = [p for p in PHASES if phases.get(p, {}).get("status") == "done"]

    incomplete_phase = get_incomplete_phase(state)

    return f"""
<ship-session-end>
SHIP IN PROGRESS: {ship_id}
Feature: {description}

Completed: {len(completed)}/7 phases
Current: {current.upper()}

{"Phase " + incomplete_phase.upper() + " is incomplete." if incomplete_phase else "Ready for next phase."}

To resume later: /ship --continue
To check status: /ship --status
</ship-session-end>
"""


def main():
    """Main entry point."""
    state = load_ship_state()

    if not state:
        return

    # Skip if ship is completed
    if state.get("status") == "completed":
        return

    reminder = format_progress_reminder(state)
    print(json.dumps({"message": reminder}))


if __name__ == "__main__":
    main()

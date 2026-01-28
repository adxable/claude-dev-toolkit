#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Load ship state on every prompt.

Injects current ship phase and progress into every prompt,
ensuring Claude maintains awareness even after context compaction.
"""

import json
import sys
from pathlib import Path
from typing import Optional

SHIP_STATE_FILE = Path(".claude/ship/current.json")

PHASES = ["plan", "implement", "verify", "review", "commit", "pr"]


def load_ship_state() -> Optional[dict]:
    """Load active ship state if it exists."""
    if not SHIP_STATE_FILE.exists():
        return None
    try:
        return json.loads(SHIP_STATE_FILE.read_text())
    except (json.JSONDecodeError, IOError):
        return None


def get_phase_status(state: dict) -> str:
    """Generate phase status display."""
    phases = state.get("phases", {})
    current = state.get("current_phase", "plan")

    lines = []
    for i, phase in enumerate(PHASES, 1):
        phase_data = phases.get(phase, {})
        status = phase_data.get("status", "pending")

        if phase == current and status != "done":
            marker = "→"
            status_text = "IN PROGRESS"
        elif status == "done":
            marker = "✓"
            status_text = "done"
        else:
            marker = "○"
            status_text = "pending"

        lines.append(f"  {marker} {i}. {phase.upper()}: {status_text}")

    return "\n".join(lines)


def get_next_action(state: dict) -> str:
    """Determine what Claude should do next."""
    current = state.get("current_phase", "plan")
    phases = state.get("phases", {})
    current_data = phases.get(current, {})

    if current_data.get("status") == "done":
        # Move to next phase
        idx = PHASES.index(current)
        if idx + 1 < len(PHASES):
            next_phase = PHASES[idx + 1]
            return f"Phase {current} complete. Start {next_phase.upper()} phase now."
        else:
            return "All phases complete! Output the final summary."

    return f"Continue with {current.upper()} phase. Follow ship.md instructions for this phase."


def format_ship_context(state: dict) -> str:
    """Format the ship state for injection."""
    description = state.get("description", "unknown feature")
    current = state.get("current_phase", "plan")
    ship_id = state.get("id", "unknown")

    phase_status = get_phase_status(state)
    next_action = get_next_action(state)

    return f"""<ship-state>
ACTIVE SHIP: {ship_id}
Feature: {description}

Current Phase: {current.upper()} ({PHASES.index(current) + 1}/7)

Progress:
{phase_status}

NEXT ACTION: {next_action}

IMPORTANT:
- After completing current phase, run: ship_phase_done {current}
- On failure, the checkpoint allows resume with: /ship --continue
- Do NOT skip phases. Follow ship.md instructions exactly.
</ship-state>"""


def main():
    """Main entry point."""
    state = load_ship_state()

    if not state:
        return

    # Check if ship is still active (not completed)
    if state.get("status") == "completed":
        return

    context = format_ship_context(state)
    print(json.dumps({"message": context}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Ship state management CLI.

Commands for Claude to manage ship workflow state.

Usage:
    ship_state start "feature description"  - Start a new ship
    ship_state phase_done <phase>           - Mark phase as complete
    ship_state status                       - Show current status
    ship_state complete                     - Mark ship as completed
    ship_state abort                        - Abort current ship
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

SHIP_DIR = Path(".claude/ship")
SHIP_STATE_FILE = SHIP_DIR / "current.json"

PHASES = ["plan", "implement", "verify", "review", "commit", "pr"]


def get_git_sha() -> str:
    """Get current git SHA."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()[:7] if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def load_state() -> Optional[dict]:
    """Load current ship state."""
    if not SHIP_STATE_FILE.exists():
        return None
    try:
        return json.loads(SHIP_STATE_FILE.read_text())
    except (json.JSONDecodeError, IOError):
        return None


def save_state(state: dict):
    """Save ship state."""
    SHIP_DIR.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now().isoformat()
    SHIP_STATE_FILE.write_text(json.dumps(state, indent=2))


def cmd_start(description: str):
    """Start a new ship workflow."""
    existing = load_state()
    if existing and existing.get("status") != "completed":
        print(f"ERROR: Ship already in progress: {existing.get('description')}")
        print("Use 'ship_state abort' to cancel, or 'ship_state status' to check progress.")
        sys.exit(1)

    ship_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    state = {
        "id": ship_id,
        "description": description,
        "status": "active",
        "current_phase": "plan",
        "started": datetime.now().isoformat(),
        "phases": {
            "plan": {"status": "in_progress", "started": datetime.now().isoformat()}
        }
    }
    save_state(state)

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 SHIP STARTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID: {ship_id}
Feature: {description}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Starting with Phase 1: PLAN
""")


def cmd_phase_done(phase: str):
    """Mark a phase as complete and advance to next."""
    state = load_state()
    if not state:
        print("ERROR: No active ship. Run 'ship_state start \"description\"' first.")
        sys.exit(1)

    if state.get("status") == "completed":
        print("ERROR: Ship already completed.")
        sys.exit(1)

    phase = phase.lower()
    if phase not in PHASES:
        print(f"ERROR: Invalid phase '{phase}'. Valid: {', '.join(PHASES)}")
        sys.exit(1)

    current = state.get("current_phase")
    if phase != current:
        print(f"WARNING: Marking '{phase}' done but current phase is '{current}'.")

    # Update phase status
    git_sha = get_git_sha()
    state["phases"][phase] = {
        "status": "done",
        "completed": datetime.now().isoformat(),
        "git_sha": git_sha
    }

    # Advance to next phase
    phase_idx = PHASES.index(phase)
    if phase_idx + 1 < len(PHASES):
        next_phase = PHASES[phase_idx + 1]
        state["current_phase"] = next_phase
        state["phases"][next_phase] = {
            "status": "in_progress",
            "started": datetime.now().isoformat()
        }
        save_state(state)
        print(f"""
[checkpoint] ✓ {phase.upper()} complete (git: {git_sha})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step {phase_idx + 2}/6: {next_phase.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    else:
        state["current_phase"] = "pr"
        save_state(state)
        print(f"""
[checkpoint] ✓ {phase.upper()} complete (git: {git_sha})

All phases complete! Output the final summary.
""")


def cmd_status():
    """Show current ship status."""
    state = load_state()
    if not state:
        print("No active ship.")
        return

    description = state.get("description", "unknown")
    current = state.get("current_phase", "plan")
    ship_id = state.get("id", "unknown")
    status = state.get("status", "unknown")

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 SHIP STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID: {ship_id}
Feature: {description}
Status: {status}
Current Phase: {current.upper()}

Progress:""")

    phases = state.get("phases", {})
    for i, phase in enumerate(PHASES, 1):
        phase_data = phases.get(phase, {})
        phase_status = phase_data.get("status", "pending")
        git_sha = phase_data.get("git_sha", "")

        if phase == current and phase_status != "done":
            marker = "→"
        elif phase_status == "done":
            marker = "✓"
        else:
            marker = "○"

        sha_str = f" (git: {git_sha})" if git_sha else ""
        print(f"  {marker} {i}. {phase.upper()}: {phase_status}{sha_str}")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


def cmd_complete():
    """Mark ship as successfully completed."""
    state = load_state()
    if not state:
        print("ERROR: No active ship.")
        sys.exit(1)

    state["status"] = "completed"
    state["completed"] = datetime.now().isoformat()
    save_state(state)

    # Archive the ship
    archive_dir = SHIP_DIR / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_file = archive_dir / f"{state['id']}.json"
    archive_file.write_text(json.dumps(state, indent=2))

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ SHIP COMPLETED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Feature: {state.get('description')}
Archived: {archive_file}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def cmd_abort():
    """Abort current ship."""
    state = load_state()
    if not state:
        print("No active ship to abort.")
        return

    state["status"] = "aborted"
    state["aborted"] = datetime.now().isoformat()
    save_state(state)

    print(f"Ship aborted: {state.get('description')}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 3:
            print("Usage: ship_state start \"feature description\"")
            sys.exit(1)
        cmd_start(" ".join(sys.argv[2:]))

    elif command == "phase_done":
        if len(sys.argv) < 3:
            print("Usage: ship_state phase_done <phase>")
            sys.exit(1)
        cmd_phase_done(sys.argv[2])

    elif command == "status":
        cmd_status()

    elif command == "complete":
        cmd_complete()

    elif command == "abort":
        cmd_abort()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Load project state on session start.

Injects STATE.md and ROADMAP.md content into the session context
so Claude maintains awareness of current position and progress.
"""

import json
import sys
from pathlib import Path


def load_state_files() -> list[str]:
    """Load state files if they exist."""
    state_dir = Path(".claude/state")
    context_parts = []

    # Load STATE.md (current position, decisions, blockers)
    state_file = state_dir / "STATE.md"
    if state_file.exists():
        content = state_file.read_text().strip()
        if content and "[Phase number" not in content:  # Skip if template not filled
            context_parts.append(f"<project-state>\n{content}\n</project-state>")

    # Load ROADMAP.md (phases and progress)
    roadmap_file = state_dir / "ROADMAP.md"
    if roadmap_file.exists():
        content = roadmap_file.read_text().strip()
        if content and "[Milestone Name]" not in content:  # Skip if template not filled
            context_parts.append(f"<project-roadmap>\n{content}\n</project-roadmap>")

    return context_parts


def main():
    """Main entry point."""
    state_dir = Path(".claude/state")

    # Only run if state tracking is enabled
    if not state_dir.exists():
        return

    context_parts = load_state_files()

    if context_parts:
        message = "\n\n".join(context_parts)
        print(json.dumps({"message": message}))


if __name__ == "__main__":
    main()

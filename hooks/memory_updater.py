#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Prompt for memory updates after significant sessions.
Suggests updates to decisions.md and lessons.md.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

DECISIONS_FILE = Path('.claude/memory/decisions.md')
LESSONS_FILE = Path('.claude/memory/lessons.md')
REVIEWS_DIR = Path('.claude/reviews')


def check_for_review_findings() -> list:
    """Check if recent review has significant findings."""
    if not REVIEWS_DIR.exists():
        return []

    findings = []

    # Get most recent review
    reviews = sorted(REVIEWS_DIR.glob('*.md'), key=lambda x: x.stat().st_mtime, reverse=True)
    if not reviews:
        return []

    recent_review = reviews[0]
    content = recent_review.read_text()

    # Check for critical/important issues
    if 'CRITICAL' in content or 'Critical' in content:
        findings.append('Critical issues found in review')
    if 'pattern' in content.lower() and ('inconsistent' in content.lower() or 'duplicate' in content.lower()):
        findings.append('Pattern inconsistencies detected')

    return findings


def format_memory_prompt(findings: list) -> str:
    """Format the memory update prompt."""

    output = """
──────────────────────────────────────────────────
📝 SESSION COMPLETE - Consider Memory Updates
──────────────────────────────────────────────────

"""

    if findings:
        output += "Review findings that might be worth remembering:\n"
        for finding in findings:
            output += f"  • {finding}\n"
        output += "\n"

    output += """Consider updating:

  decisions.md - New architectural or pattern decisions?
    Example: "Use queryOptions factory for all TanStack Query"
    Add with: /memory decision "description"

  lessons.md - Problems solved worth remembering?
    Example: "Zustand without useShallow causes infinite loops"
    Add with: /memory lesson "description"

To skip: Just continue with your next task.
──────────────────────────────────────────────────
"""

    return output


def main():
    """Hook entry point - runs on Stop event."""
    try:
        input_data = json.load(sys.stdin)

        # Check if session had significant activity
        session_commands = input_data.get('commands', [])

        # Only prompt after certain commands
        significant_commands = ['/ship', '/review', '/implement', '/refactor']
        had_significant = any(cmd in str(session_commands) for cmd in significant_commands)

        if not had_significant:
            sys.exit(0)

        # Check for review findings
        findings = check_for_review_findings()

        # Output prompt
        print(format_memory_prompt(findings))

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()

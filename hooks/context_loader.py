#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Load and inject session context into prompts.
Provides continuity across sessions.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

CONTEXT_FILE = Path('.claude/context/session_context.json')


def load_context() -> dict:
    """Load session context if exists."""
    if CONTEXT_FILE.exists():
        return json.loads(CONTEXT_FILE.read_text())
    return {}


def save_context(context: dict):
    """Save updated context."""
    CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    context['lastUpdated'] = datetime.now().isoformat()
    CONTEXT_FILE.write_text(json.dumps(context, indent=2))


def format_context_summary(context: dict) -> str:
    """Format context for injection into prompt."""
    if not context:
        return ""

    output_parts = []

    # Recent plans
    plans = context.get('previousPlans', [])[-3:]  # Last 3
    if plans:
        output_parts.append("Recent Plans:")
        for plan in plans:
            status = plan.get('status', 'unknown')
            summary = plan.get('summary', 'No summary')
            output_parts.append(f"  • {summary} ({status})")

    # Key decisions
    decisions = context.get('decisions', [])[-5:]  # Last 5
    if decisions:
        output_parts.append("\nKey Decisions:")
        for d in decisions:
            decision = d.get('decision', '')
            reason = d.get('reason', '')
            output_parts.append(f"  • {decision}: {reason}")

    # Established patterns
    patterns = context.get('patterns', {})
    if patterns:
        output_parts.append("\nEstablished Patterns:")
        for name, pattern in patterns.items():
            output_parts.append(f"  • {name}: {pattern}")

    # Blocked patterns
    blocked = context.get('blockedPatterns', [])
    if blocked:
        output_parts.append("\nDo NOT use:")
        for b in blocked:
            pattern = b.get('pattern', '')
            reason = b.get('reason', '')
            output_parts.append(f"  • {pattern} ({reason})")

    # Recent lessons
    lessons = context.get('recentLessons', [])[-3:]  # Last 3
    if lessons:
        output_parts.append("\nRecent Lessons:")
        for lesson in lessons:
            output_parts.append(f"  • {lesson.get('lesson', '')}")

    if not output_parts:
        return ""

    header = "\n" + "─" * 50 + "\n"
    header += "📚 SESSION CONTEXT (from previous sessions)\n"
    header += "─" * 50 + "\n"

    return header + "\n".join(output_parts) + "\n" + "─" * 50 + "\n"


def main():
    """Hook entry point - inject context on UserPromptSubmit."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '').lower()

        # Only show context for planning/implementation commands
        relevant_keywords = [
            'plan', 'implement', 'create', 'add', 'build', 'feature',
            '/ship', '/plan', '/implement'
        ]

        if not any(kw in prompt for kw in relevant_keywords):
            sys.exit(0)

        context = load_context()
        if context:
            output = format_context_summary(context)
            if output:
                print(output)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()

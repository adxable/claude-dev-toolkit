#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Update session context after significant events.
Runs on Stop event to capture session learnings.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

CONTEXT_FILE = Path('.claude/context/session_context.json')
PLANS_DIR = Path('.claude/plans')


def load_context() -> dict:
    """Load existing context."""
    if CONTEXT_FILE.exists():
        return json.loads(CONTEXT_FILE.read_text())
    return {
        'version': '1.0',
        'previousPlans': [],
        'decisions': [],
        'patterns': {},
        'blockedPatterns': [],
        'recentLessons': []
    }


def save_context(context: dict):
    """Save context."""
    CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    context['lastUpdated'] = datetime.now().isoformat()
    CONTEXT_FILE.write_text(json.dumps(context, indent=2))


def update_plans(context: dict):
    """Update plan list from plans directory."""
    if not PLANS_DIR.exists():
        return

    existing_files = {p['file'] for p in context.get('previousPlans', [])}

    for plan_file in PLANS_DIR.glob('*.md'):
        file_path = str(plan_file)
        if file_path not in existing_files:
            # New plan found
            context['previousPlans'].append({
                'file': file_path,
                'created': datetime.now().isoformat(),
                'status': 'created',
                'summary': plan_file.stem.replace('plan-', '').replace('-', ' ')
            })

    # Keep last 10 plans
    context['previousPlans'] = context['previousPlans'][-10:]


def add_decision(context: dict, decision: str, reason: str, plan_context: str = ''):
    """Add a decision to context."""
    context['decisions'].append({
        'decision': decision,
        'reason': reason,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'context': plan_context
    })
    # Keep last 20 decisions
    context['decisions'] = context['decisions'][-20:]


def add_pattern(context: dict, name: str, pattern: str):
    """Add or update an established pattern."""
    context['patterns'][name] = pattern


def add_blocked_pattern(context: dict, pattern: str, reason: str):
    """Add a pattern to avoid."""
    # Check if already blocked
    existing = [b for b in context.get('blockedPatterns', []) if b['pattern'] == pattern]
    if not existing:
        context['blockedPatterns'].append({
            'pattern': pattern,
            'reason': reason,
            'since': datetime.now().strftime('%Y-%m-%d')
        })


def add_lesson(context: dict, lesson: str, lesson_context: str = ''):
    """Add a lesson learned."""
    context['recentLessons'].append({
        'lesson': lesson,
        'learned': datetime.now().strftime('%Y-%m-%d'),
        'context': lesson_context
    })
    # Keep last 10 lessons
    context['recentLessons'] = context['recentLessons'][-10:]


def main():
    """Hook entry point."""
    try:
        context = load_context()
        update_plans(context)
        save_context(context)
        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()

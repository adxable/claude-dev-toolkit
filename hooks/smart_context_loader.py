#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Smart Context Loader Hook

Analyzes user prompts and automatically suggests relevant skills/context
based on detected patterns. Runs on UserPromptSubmit.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from utils.constants import ensure_session_log_dir


# Context detection rules
# Each rule has: keywords, patterns, and associated skills/context
# Skills reference: frontend-design, webapp-testing, tdd, browser-testing
CONTEXT_RULES: List[Dict[str, Any]] = [
    {
        "name": "forms",
        "keywords": ["form", "input", "validation", "submit", "field", "react-hook-form", "formik", "zod"],
        "patterns": [
            r"create.*form",
            r"add.*form",
            r"form.*validation",
            r"validate.*input",
            r"handle.*submit",
        ],
        "skills": [],
        "context": "Form handling - use React Hook Form + Zod, consider error states and accessibility",
        "priority": "high"
    },
    {
        "name": "api",
        "keywords": ["api", "fetch", "query", "mutation", "endpoint", "tanstack", "react-query", "swr"],
        "patterns": [
            r"fetch.*data",
            r"api.*call",
            r"create.*query",
            r"use.*query",
            r"mutation",
        ],
        "skills": [],
        "context": "Data fetching - use TanStack Query with useSuspenseQuery, consider loading/error states",
        "priority": "high"
    },
    {
        "name": "styling",
        "keywords": ["style", "css", "tailwind", "design", "layout", "responsive", "animation", "ui"],
        "patterns": [
            r"style.*component",
            r"add.*styling",
            r"make.*responsive",
            r"update.*design",
            r"tailwind",
        ],
        "skills": ["frontend-design"],
        "context": "Styling work - use Tailwind + shadcn/ui, follow design system, ensure responsiveness",
        "priority": "medium"
    },
    {
        "name": "components",
        "keywords": ["component", "modal", "dialog", "button", "table", "list", "card"],
        "patterns": [
            r"create.*component",
            r"add.*component",
            r"build.*modal",
            r"implement.*dialog",
        ],
        "skills": ["frontend-design"],
        "context": "Component creation - consider reusability, props interface, and composition",
        "priority": "high"
    },
    {
        "name": "performance",
        "keywords": ["performance", "optimize", "slow", "memo", "usememo", "usecallback", "lazy", "suspense"],
        "patterns": [
            r"optimize.*",
            r"improve.*performance",
            r"reduce.*render",
            r"code.*split",
        ],
        "skills": [],
        "context": "Performance optimization - use performance-auditor agent, profile first then optimize",
        "priority": "high"
    },
    {
        "name": "typescript",
        "keywords": ["type", "interface", "generic", "typescript", "ts", "typing"],
        "patterns": [
            r"add.*types?",
            r"fix.*type",
            r"type.*error",
            r"generic.*",
        ],
        "skills": [],
        "context": "TypeScript work - ensure strict typing, avoid 'any', see CLAUDE.md conventions",
        "priority": "medium"
    },
    {
        "name": "testing",
        "keywords": ["test", "spec", "jest", "vitest", "playwright", "e2e", "unit"],
        "patterns": [
            r"write.*test",
            r"add.*test",
            r"test.*component",
            r"e2e.*test",
        ],
        "skills": ["webapp-testing", "tdd"],
        "context": "Testing - follow TDD workflow, use Playwright for e2e, test behavior not implementation",
        "priority": "medium"
    },
    {
        "name": "browser",
        "keywords": ["browser", "visual", "ui test", "screenshot", "chrome", "verify ui"],
        "patterns": [
            r"verify.*ui",
            r"check.*browser",
            r"visual.*test",
            r"test.*ui",
        ],
        "skills": ["browser-testing"],
        "context": "Browser verification - use /review --browser for visual testing with Chrome extension",
        "priority": "medium"
    },
    {
        "name": "refactoring",
        "keywords": ["refactor", "clean", "simplify", "extract", "reorganize"],
        "patterns": [
            r"refactor.*",
            r"clean.*up",
            r"simplify.*",
            r"extract.*",
        ],
        "skills": [],
        "context": "Refactoring - ensure tests pass before and after, use refactorer agent if needed",
        "priority": "medium"
    },
    {
        "name": "state",
        "keywords": ["state", "zustand", "redux", "context", "store", "global"],
        "patterns": [
            r"manage.*state",
            r"global.*state",
            r"add.*store",
            r"state.*management",
        ],
        "skills": [],
        "context": "State management - use Zustand with useShallow for UI state, TanStack Query for server state",
        "priority": "medium"
    },
    {
        "name": "routing",
        "keywords": ["route", "router", "navigation", "page", "redirect", "link"],
        "patterns": [
            r"add.*route",
            r"create.*page",
            r"navigation.*",
            r"redirect.*",
        ],
        "skills": [],
        "context": "Routing - use TanStack Router or React Router v7, consider loading states and error boundaries",
        "priority": "low"
    },
]


def match_keywords(prompt: str, keywords: List[str]) -> bool:
    """Check if any keyword matches the prompt (case-insensitive)"""
    prompt_lower = prompt.lower()
    return any(kw.lower() in prompt_lower for kw in keywords)


def match_patterns(prompt: str, patterns: List[str]) -> bool:
    """Check if any regex pattern matches the prompt"""
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)


def detect_contexts(prompt: str) -> List[Dict[str, Any]]:
    """Detect all matching contexts from the prompt"""
    matched = []

    for rule in CONTEXT_RULES:
        keywords_match = match_keywords(prompt, rule["keywords"])
        patterns_match = match_patterns(prompt, rule.get("patterns", []))

        if keywords_match or patterns_match:
            matched.append({
                "name": rule["name"],
                "skills": rule["skills"],
                "context": rule["context"],
                "priority": rule["priority"],
                "match_type": "keyword" if keywords_match else "pattern"
            })

    return matched


def format_output(contexts: List[Dict[str, Any]]) -> str:
    """Format the context detection output"""
    if not contexts:
        return ""

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    contexts.sort(key=lambda x: priority_order.get(x["priority"], 3))

    output = "\n" + "─" * 50 + "\n"
    output += "📋 SMART CONTEXT DETECTED\n"
    output += "─" * 50 + "\n\n"

    # Collect all skills
    all_skills = []
    for ctx in contexts:
        all_skills.extend(ctx["skills"])
    all_skills = list(dict.fromkeys(all_skills))  # Remove duplicates, preserve order

    if all_skills:
        output += "💡 Suggested Skills:\n"
        for skill in all_skills:
            output += f"   → {skill}\n"
        output += "\n"

    output += "📝 Context Notes:\n"
    for ctx in contexts:
        priority_icon = {"high": "❗", "medium": "•", "low": "○"}.get(ctx["priority"], "•")
        output += f"   {priority_icon} [{ctx['name'].upper()}] {ctx['context']}\n"

    output += "\n" + "─" * 50 + "\n"

    return output


def log_context_detection(session_id: str, prompt: str, contexts: List[Dict[str, Any]]):
    """Log context detection to session directory"""
    try:
        log_dir = ensure_session_log_dir(session_id)
        log_file = log_dir / 'smart_context.json'

        # Read existing log data
        if log_file.exists():
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt[:200] + '...' if len(prompt) > 200 else prompt,
            'detected_contexts': [
                {
                    'name': ctx['name'],
                    'skills': ctx['skills'],
                    'priority': ctx['priority'],
                    'match_type': ctx['match_type']
                }
                for ctx in contexts
            ],
            'total_matches': len(contexts)
        }

        log_data.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    except Exception:
        pass  # Don't fail the hook if logging fails


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        session_id = input_data.get('session_id', 'unknown')
        prompt = input_data.get('prompt', '')

        if not prompt:
            sys.exit(0)

        # Detect contexts
        contexts = detect_contexts(prompt)

        # Log detection
        log_context_detection(session_id, prompt, contexts)

        # Output if contexts found
        if contexts:
            output = format_output(contexts)
            print(output)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"Error in smart_context_loader: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()

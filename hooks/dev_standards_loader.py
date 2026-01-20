#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Development Standards Loader Hook

Loads configured development standards and detects project stack.
Runs on UserPromptSubmit to inject relevant guidelines into context.

Reads from:
- .claude/config/code-quality.json
- .claude/config/project-structure.json
- .claude/config/frontend-guidelines.json
- package.json (for stack detection)
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Set


def find_project_root() -> Path:
    """Find project root by looking for package.json or .git"""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / 'package.json').exists() or (parent / '.git').exists():
            return parent
    return current


def load_json_file(path: Path) -> Optional[Dict[str, Any]]:
    """Load JSON file if it exists"""
    if path.exists():
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def detect_stack(package_json: Dict[str, Any]) -> Dict[str, str]:
    """Detect frontend stack from package.json dependencies"""
    deps = {
        **package_json.get('dependencies', {}),
        **package_json.get('devDependencies', {})
    }

    stack = {}

    # State management
    if 'zustand' in deps:
        stack['state'] = 'zustand'
    elif '@reduxjs/toolkit' in deps:
        stack['state'] = 'redux-toolkit'
    elif 'jotai' in deps:
        stack['state'] = 'jotai'
    elif 'mobx' in deps:
        stack['state'] = 'mobx'

    # Server state
    if '@tanstack/react-query' in deps:
        stack['serverState'] = 'tanstack-query'
    elif 'swr' in deps:
        stack['serverState'] = 'swr'

    # Forms
    if 'react-hook-form' in deps:
        stack['forms'] = 'react-hook-form'
        if 'zod' in deps:
            stack['forms'] += '+zod'
    elif 'formik' in deps:
        stack['forms'] = 'formik'
        if 'yup' in deps:
            stack['forms'] += '+yup'

    # Styling
    if 'tailwindcss' in deps:
        stack['styling'] = 'tailwind'
        if 'class-variance-authority' in deps:
            stack['styling'] += '+cva'
    elif 'styled-components' in deps:
        stack['styling'] = 'styled-components'
    elif '@emotion/react' in deps:
        stack['styling'] = 'emotion'

    # UI library
    if any(k.startswith('@radix-ui/') for k in deps):
        stack['ui'] = 'radix-ui'
    elif any(k.startswith('@mui/') for k in deps):
        stack['ui'] = 'mui'
    elif any(k.startswith('@chakra-ui/') for k in deps):
        stack['ui'] = 'chakra-ui'

    # Framework/Router
    if 'next' in deps:
        stack['framework'] = 'nextjs'
    elif '@remix-run/react' in deps:
        stack['framework'] = 'remix'
    elif '@tanstack/react-router' in deps:
        stack['router'] = 'tanstack-router'
    elif 'react-router' in deps or 'react-router-dom' in deps:
        stack['router'] = 'react-router'

    return stack


def get_stack_rules(stack: Dict[str, str]) -> List[str]:
    """Get applicable rules based on detected stack"""
    rules = []

    if stack.get('state') == 'zustand':
        rules.append("ZUSTAND: Always use `useShallow` for object/array selectors to prevent infinite re-renders")

    if stack.get('serverState') == 'tanstack-query':
        rules.append("TANSTACK QUERY: Use queryOptions() factory pattern in api/queries.ts")
        rules.append("TANSTACK QUERY: Prefer useSuspenseQuery with Suspense boundaries at layout level")

    if 'react-hook-form' in stack.get('forms', ''):
        rules.append("FORMS: Use zodResolver with React Hook Form, infer types with z.infer<typeof schema>")

    if 'tailwind' in stack.get('styling', ''):
        rules.append("TAILWIND: Use cn() helper from @/lib/utils for conditional classes")

    if stack.get('framework') == 'nextjs':
        rules.append("NEXT.JS: Keep app/ for routing only, business logic in src/features/")
        rules.append("NEXT.JS: Server Components are default, add 'use client' only when needed")

    return rules


def format_config_summary(
    code_quality: Optional[Dict],
    project_structure: Optional[Dict],
    frontend: Optional[Dict],
    stack: Dict[str, str],
    stack_rules: List[str],
    autonomous: bool = False
) -> str:
    """Format configuration summary for output"""

    output_parts = []

    # Autonomous mode indicator
    if autonomous:
        output_parts.append("MODE: Autonomous (suggestions bypassed)")
        output_parts.append("")

    # Stack detection
    if stack:
        stack_items = [f"{k}: {v}" for k, v in stack.items()]
        output_parts.append(f"Detected Stack: {', '.join(stack_items)}")

    # Code quality config
    if code_quality:
        strictness = code_quality.get('strictness', 'not set')
        abstraction = code_quality.get('abstractionRule', 'rule-of-three')
        output_parts.append(f"Code Quality: {strictness} | Abstraction: {abstraction}")

    # Project structure config
    if project_structure:
        org = project_structure.get('enforced', {}).get('organization', 'not set')
        naming = project_structure.get('enforced', {}).get('naming', 'not set')
        output_parts.append(f"Structure: {org} | Naming: {naming}")

    # Stack-specific rules
    if stack_rules:
        output_parts.append("")
        output_parts.append("Active Rules:")
        for rule in stack_rules:
            output_parts.append(f"  • {rule}")

    if not output_parts:
        return ""

    header = "\n" + "─" * 50 + "\n"
    header += "⚙️  DEV STANDARDS LOADED\n"
    header += "─" * 50 + "\n"

    return header + "\n".join(output_parts) + "\n" + "─" * 50 + "\n"


def is_autonomous_mode(prompt: str) -> bool:
    """Check if running in autonomous mode (ship/ralph)"""
    prompt_lower = prompt.lower()
    autonomous_commands = ['/ship', '/ralph', '/adx:ship', '/adx:ralph']
    return any(cmd in prompt_lower for cmd in autonomous_commands)


def should_show_config(prompt: str) -> bool:
    """Determine if config should be shown based on prompt content"""
    # Show for implementation-related prompts
    implementation_keywords = [
        'implement', 'create', 'add', 'build', 'make', 'write',
        'fix', 'update', 'refactor', 'component', 'hook', 'feature',
        '/plan', '/implement', '/ship', '/refactor', '/review'
    ]

    prompt_lower = prompt.lower()
    return any(kw in prompt_lower for kw in implementation_keywords)


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '')

        if not prompt or not should_show_config(prompt):
            sys.exit(0)

        # Check if autonomous mode
        autonomous = is_autonomous_mode(prompt)

        # Find project root
        root = find_project_root()
        config_dir = root / '.claude' / 'config'

        # Load configurations
        code_quality = load_json_file(config_dir / 'code-quality.json')
        project_structure = load_json_file(config_dir / 'project-structure.json')
        frontend = load_json_file(config_dir / 'frontend-guidelines.json')

        # Detect stack from package.json
        package_json = load_json_file(root / 'package.json')
        stack = detect_stack(package_json) if package_json else {}

        # Get stack-specific rules
        stack_rules = get_stack_rules(stack)

        # Only output if we have something to show
        has_config = any([code_quality, project_structure, frontend])
        has_stack = bool(stack)

        if has_config or has_stack:
            output = format_config_summary(
                code_quality, project_structure, frontend, stack, stack_rules,
                autonomous=autonomous
            )
            if output:
                print(output)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        # Don't fail the hook, just exit silently
        sys.exit(0)


if __name__ == '__main__':
    main()

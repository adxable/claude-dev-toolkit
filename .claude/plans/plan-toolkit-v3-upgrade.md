# ADX Toolkit v3.0 Implementation Plan

**Created:** 2026-01-20
**Status:** Ready for implementation
**Scope:** Critical gaps + modern patterns + discovery system

---

## Overview

This plan upgrades the ADX toolkit with:
1. **Critical fixes** - Testing in verify, security, error recovery
2. **Subagent orchestration** - Agents spawning other agents
3. **Checkpoint system** - Rollback points in /ship
4. **Cost tracking** - Token usage visibility
5. **Context persistence** - Remember across sessions
6. **Memory auto-update** - Prompt for lessons.md updates
7. **Circuit breaker** - Safety limits for autonomous loops
8. **Discovery system** - Web search for latest patterns

---

## Phase 1: Critical Gaps

### 1.1 Extend `/verify` with Testing (Optional)

**Why:** Testing should be part of verification, not a separate step. Auto-detect if tests exist.

**File:** `commands/verify.md` (updated)

```markdown
# Verify

Type check, lint, build, and optionally run tests.

## Arguments

- `$ARGUMENTS` - Optional: "--skip-tests" or "--tests-only"

## Instructions

### 1. Detect Test Framework

Check for test configuration:
```bash
# Check package.json for test scripts
cat package.json | grep -E '"test":|"vitest"|"jest"'

# Check for test config files
ls vitest.config.* jest.config.* playwright.config.* 2>/dev/null
```

If tests detected, set `HAS_TESTS=true`

### 2. Run Static Checks

```bash
# Type checking
npx tsc --noEmit

# Linting
npm run lint || npx eslint .

# Build
npm run build
```

### 3. Run Tests (If Detected)

**Only if HAS_TESTS=true AND --skip-tests not passed:**

```bash
# Unit tests
npm test

# If playwright detected and --e2e flag
npx playwright test
```

### 4. Handle Failures

For each failure type:

**Type errors:**
- List errors with file:line
- Attempt auto-fix (max 3 iterations)

**Lint errors:**
- Run `npm run lint:fix` if available
- Manual fix remaining

**Test failures:**
- Show failed test names
- Ask: "Fix failing tests? [Y/n]"
- If yes, analyze and fix (max 3 iterations)

**Build errors:**
- Analyze error output
- Suggest fixes

### 5. Output Summary

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ VERIFICATION COMPLETE                                    │
├─────────────────────────────────────────────────────────────┤
│  Type Check:  ✓ Pass (0 errors)                             │
│  Lint:        ✓ Pass (2 warnings)                           │
│  Build:       ✓ Pass                                        │
│  Tests:       ✓ Pass (45/45) [optional - if detected]       │
│               ○ Skipped (no tests detected)                 │
└─────────────────────────────────────────────────────────────┘
```

## Flags

- `--skip-tests` - Skip test execution even if detected
- `--tests-only` - Run only tests, skip type/lint/build
- `--e2e` - Include E2E tests (Playwright/Cypress)
- `--fix` - Auto-fix all fixable issues

## Workflow Position

/plan → /implement → /refactor → **/verify** → /review → /commit → /pr
                                    ↑
                        Now includes testing!
```

**File:** `agents/verifier.md` (new)

```yaml
---
name: verifier
description: Run type checks, linting, build, and tests with auto-fix capabilities
tools: Read, Bash, Grep, Glob, Edit, Write
model: sonnet
---

# Verifier Agent

You verify code quality through static analysis, building, and testing.

## Capabilities

1. **Type Checking** - Run TypeScript compiler, fix type errors
2. **Linting** - Run ESLint, auto-fix where possible
3. **Building** - Run build process, resolve build errors
4. **Testing** - Run detected test suite, fix failing tests

## Test Detection

Before running tests, detect if they exist:

```bash
# Check for test framework
grep -E '"vitest"|"jest"|"@testing-library"' package.json

# Check for test files
find src -name "*.test.*" -o -name "*.spec.*" | head -5

# Check for test script
npm run test --dry-run 2>/dev/null
```

If no tests found:
- Output: "No tests detected - skipping test phase"
- Continue to next verification step

## Auto-Fix Strategy

For each error type:

1. **Analyze error** - Parse error message
2. **Locate source** - Find file and line
3. **Determine fix** - Is it auto-fixable?
4. **Apply fix** - Edit file
5. **Re-run check** - Verify fix worked
6. **Max 3 iterations** - Prevent infinite loops

## Terminal Output

```
[verifier] Starting verification...
[verifier] ✓ TypeScript: 0 errors
[verifier] ⚠ ESLint: 3 errors (auto-fixing...)
[verifier] ✓ ESLint: Fixed 3 errors
[verifier] ✓ Build: Success
[verifier] Tests detected: vitest
[verifier] Running tests...
[verifier] ✓ Tests: 45/45 passed
[verifier] ✓ Verification complete
```
```

---

### 1.2 Add Security Auditor Agent

**Why:** No scanning for secrets, vulnerabilities, or dangerous patterns.

**File:** `agents/security-auditor.md`

```yaml
---
name: security-auditor
description: Scan for security vulnerabilities, hardcoded secrets, and dangerous patterns
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Security Auditor

You scan code for security vulnerabilities and sensitive data exposure.

## Scan Categories

### 1. Hardcoded Secrets

Search patterns:
```regex
# API Keys
(api[_-]?key|apikey)\s*[:=]\s*['"][^'"]+['"]

# Tokens
(token|bearer|auth)\s*[:=]\s*['"][^'"]+['"]

# Passwords
(password|passwd|pwd)\s*[:=]\s*['"][^'"]+['"]

# AWS
(AKIA|ASIA)[A-Z0-9]{16}

# Private keys
-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----
```

### 2. Dangerous Patterns

```javascript
// XSS vulnerabilities
innerHTML\s*=
dangerouslySetInnerHTML
document\.write\(

// Code injection
eval\(
new Function\(
setTimeout\([^,]+,\s*['"]

// SQL injection (if backend)
query\([^)]*\+|execute\([^)]*\+
```

### 3. Configuration Issues

- `.env` files committed (check .gitignore)
- Sensitive files in public directories
- Debug mode enabled in production configs
- CORS set to `*`

### 4. Dependency Vulnerabilities

```bash
# Check for known vulnerabilities
npm audit --json
```

## Output Format

```
┌─────────────────────────────────────────────────────────────┐
│  🔒 SECURITY AUDIT REPORT                                   │
├─────────────────────────────────────────────────────────────┤
│  CRITICAL: 0                                                │
│  HIGH: 1                                                    │
│  MEDIUM: 2                                                  │
│  LOW: 3                                                     │
├─────────────────────────────────────────────────────────────┤
│  [HIGH] Hardcoded API key                                   │
│  File: src/config.ts:15                                     │
│  Fix: Move to environment variable                          │
│                                                             │
│  [MEDIUM] innerHTML usage                                   │
│  File: src/components/RichText.tsx:42                       │
│  Fix: Use DOMPurify or React's dangerouslySetInnerHTML     │
│       with sanitization                                     │
└─────────────────────────────────────────────────────────────┘
```

## Integration

Run as part of `/review` alongside code-reviewer:
- Parallel execution for speed
- Results merged into review report
- Critical issues block PR creation
```

---

### 1.3 Error Recovery with Checkpoints

**Why:** `/ship` stops on error with no guidance.

**File:** `hooks/checkpoint.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Checkpoint system for /ship command.
Creates restore points after each phase for rollback/resume.
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

CHECKPOINT_DIR = Path('.claude/checkpoints')

class CheckpointManager:
    """Manage checkpoints for /ship workflow."""

    def __init__(self, ship_id: str):
        self.ship_id = ship_id
        self.checkpoint_file = CHECKPOINT_DIR / f'{ship_id}.json'

    def save(self, phase: str, state: Dict[str, Any]):
        """Save checkpoint after successful phase completion."""
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

        checkpoint = self.load() or {
            'ship_id': self.ship_id,
            'started': datetime.now().isoformat(),
            'phases': {}
        }

        # Save git state for potential rollback
        git_sha = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True, text=True
        ).stdout.strip()

        checkpoint['phases'][phase] = {
            'completed': datetime.now().isoformat(),
            'git_sha': git_sha,
            'state': state
        }
        checkpoint['last_phase'] = phase
        checkpoint['last_updated'] = datetime.now().isoformat()

        self.checkpoint_file.write_text(json.dumps(checkpoint, indent=2))

        print(f"[checkpoint] ✓ Saved after {phase} (git: {git_sha[:7]})")

    def load(self) -> Optional[Dict[str, Any]]:
        """Load existing checkpoint."""
        if self.checkpoint_file.exists():
            return json.loads(self.checkpoint_file.read_text())
        return None

    def get_resume_point(self) -> Optional[str]:
        """Get the phase to resume from."""
        checkpoint = self.load()
        if not checkpoint:
            return None

        phases_order = ['plan', 'implement', 'refactor', 'verify', 'review', 'commit', 'pr']
        last_phase = checkpoint.get('last_phase')

        if last_phase in phases_order:
            idx = phases_order.index(last_phase)
            if idx + 1 < len(phases_order):
                return phases_order[idx + 1]

        return None

    def rollback(self, phase: str) -> bool:
        """Rollback to checkpoint state."""
        checkpoint = self.load()
        if not checkpoint or phase not in checkpoint.get('phases', {}):
            return False

        git_sha = checkpoint['phases'][phase]['git_sha']

        print(f"[checkpoint] Rolling back to {phase} (git: {git_sha[:7]})")
        result = subprocess.run(
            ['git', 'reset', '--hard', git_sha],
            capture_output=True
        )

        return result.returncode == 0

    def list_checkpoints(self) -> Dict[str, str]:
        """List all saved checkpoints."""
        checkpoint = self.load()
        if not checkpoint:
            return {}

        return {
            phase: data['completed']
            for phase, data in checkpoint.get('phases', {}).items()
        }

    def clear(self):
        """Clear checkpoint after successful completion."""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()


def format_checkpoint_status(manager: CheckpointManager) -> str:
    """Format checkpoint status for display."""
    checkpoints = manager.list_checkpoints()

    if not checkpoints:
        return "No checkpoints saved"

    output = "\n─" * 50 + "\n"
    output += "📍 CHECKPOINTS\n"
    output += "─" * 50 + "\n\n"

    phases_order = ['plan', 'implement', 'refactor', 'verify', 'review', 'commit', 'pr']

    for phase in phases_order:
        if phase in checkpoints:
            output += f"  ✓ {phase}: {checkpoints[phase]}\n"
        else:
            output += f"  ○ {phase}: not reached\n"

    resume_point = manager.get_resume_point()
    if resume_point:
        output += f"\n  → Resume from: {resume_point}\n"
        output += f"  → Command: /ship --continue\n"

    output += "\n" + "─" * 50 + "\n"

    return output


def main():
    """Hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        # Hook logic would go here
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
```

**Update `commands/ship.md`:**

```markdown
## Checkpoint System

Each phase saves a checkpoint for recovery:

```
/ship "add feature"
    ├─ CHECKPOINT: after /plan
    │   └─ Can rollback: git state + plan file
    ├─ CHECKPOINT: after /implement
    │   └─ Can rollback: git state before changes
    ├─ CHECKPOINT: after /refactor
    ├─ CHECKPOINT: after /verify
    ├─ CHECKPOINT: after /review
    └─ Complete: checkpoint cleared
```

## Recovery Flags

- `--continue` - Resume from last successful checkpoint
- `--from <phase>` - Start from specific phase
- `--rollback <phase>` - Rollback to checkpoint state
- `--status` - Show checkpoint status

## On Failure

When a phase fails:
1. Checkpoint is saved
2. Error details logged
3. Recovery options displayed:

```
┌─────────────────────────────────────────────────────────────┐
│  ❌ SHIP FAILED at verify phase                             │
├─────────────────────────────────────────────────────────────┤
│  Error: Type check failed (3 errors)                        │
│                                                             │
│  Checkpoints saved:                                         │
│  ✓ plan      (10:15:00)                                     │
│  ✓ implement (10:22:00)                                     │
│  ✓ refactor  (10:25:00)                                     │
│  ✗ verify    (failed)                                       │
│                                                             │
│  Options:                                                   │
│  • /ship --continue     Resume from verify                  │
│  • /ship --from verify  Retry verify phase                  │
│  • /ship --rollback implement  Undo and retry               │
│  • Fix manually, then /ship --from verify                   │
└─────────────────────────────────────────────────────────────┘
```
```

---

## Phase 2: Subagent Orchestration

### 2.1 Enable Agents to Spawn Other Agents

**Why:** Agents work independently. Modern pattern: agents can verify uncertainties by spawning specialized agents.

**Update `agents/code-reviewer.md`:**

```yaml
---
name: code-reviewer
description: Reviews code for quality, patterns, and potential issues. Can spawn explorer for verification.
tools: Read, Grep, Glob, Bash, Task
model: opus
---

# Code Reviewer

You review code for quality, patterns, and potential issues.

## Subagent Orchestration

When uncertain about a pattern or convention, **spawn the explorer agent** to verify:

### When to Spawn Explorer

1. **Pattern verification** - "Is this pattern used elsewhere?"
2. **Convention checking** - "What's the existing convention for X?"
3. **Impact analysis** - "What else uses this function?"
4. **Consistency check** - "Are similar components structured this way?"

### How to Spawn

Use the Task tool with subagent_type=explorer:

```
When reviewing UserCard.tsx and seeing an unusual pattern:

Think: "This uses a custom hook pattern. Let me verify if this is consistent."

Action: Spawn explorer agent
Task: "Search for other custom hooks in this codebase.
       How are they typically structured?
       Does useUserData follow the same pattern?"

Use result to inform review comment.
```

### Examples

**Example 1: Verify naming convention**
```
[code-reviewer] Reviewing: src/features/orders/OrderCard.tsx
[code-reviewer] → Uncertain: Component uses 'handleClick' naming
[code-reviewer] → Spawning explorer to verify convention...

[explorer] Searching for event handler naming patterns...
[explorer] Found: 85% use 'handleX' pattern, 15% use 'onX'
[explorer] Convention: 'handleX' for internal, 'onX' for props

[code-reviewer] ✓ Naming follows project convention
```

**Example 2: Check for existing utility**
```
[code-reviewer] Reviewing: src/utils/formatDate.ts
[code-reviewer] → New utility added, checking for duplicates...
[code-reviewer] → Spawning explorer...

[explorer] Searching for date formatting functions...
[explorer] Found: src/lib/dateUtils.ts has formatDate()
[explorer] Potential duplicate!

[code-reviewer] ⚠ Duplicate utility detected
[code-reviewer] → Recommend: Use existing src/lib/dateUtils.ts
```

## Review Process

1. **Initial scan** - Read changed files
2. **Pattern analysis** - Identify patterns used
3. **Verification** - Spawn explorer if uncertain
4. **Issue categorization** - Critical/Important/Minor
5. **Report generation** - Markdown report with findings

## Output

Include verification notes in report:

```markdown
## Verification Notes

These findings were verified by spawning explorer agent:
- ✓ Naming convention matches project standard (verified 85% consistency)
- ✓ No duplicate utilities found
- ⚠ Similar component exists: consider consolidation
```
```

**Update `agents/refactorer.md`:**

```yaml
---
name: refactorer
description: Cleans code and applies patterns. Can spawn explorer to find similar code.
tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: opus
---

# Refactorer

You clean code, remove technical debt, and apply consistent patterns.

## Subagent Orchestration

Before refactoring, **spawn explorer** to understand existing patterns:

### When to Spawn Explorer

1. **Before extracting utility** - "Are there similar utilities I should consolidate?"
2. **Before renaming** - "What's the naming convention for this type?"
3. **Before restructuring** - "How are similar modules organized?"

### Examples

**Example: Extract shared logic**
```
[refactorer] Found duplicate date formatting in 3 files
[refactorer] → Spawning explorer to find existing utilities...

[explorer] Searching src/lib and src/utils for date functions...
[explorer] Found: src/lib/utils.ts has formatDate (different implementation)

[refactorer] Decision: Consolidate into src/lib/utils.ts
[refactorer] → Will update 3 files + enhance existing utility
```
```

---

## Phase 3: Cost Tracking

### 3.1 Token Usage Visibility

**File:** `hooks/cost_tracker.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Track token usage and estimated costs per session/command.
Logs to .claude/metrics/ for analysis.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, Optional

METRICS_DIR = Path('.claude/metrics')
DAILY_LOG = METRICS_DIR / 'daily'
SUMMARY_FILE = METRICS_DIR / 'usage_summary.json'

# Approximate costs per 1M tokens (adjust as needed)
PRICING = {
    'claude-3-haiku': {'input': 0.25, 'output': 1.25},
    'claude-3-5-sonnet': {'input': 3.0, 'output': 15.0},
    'claude-3-opus': {'input': 15.0, 'output': 75.0},
    'claude-sonnet-4': {'input': 3.0, 'output': 15.0},
    'claude-opus-4': {'input': 15.0, 'output': 75.0},
}


class CostTracker:
    """Track and log token usage costs."""

    def __init__(self):
        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        DAILY_LOG.mkdir(parents=True, exist_ok=True)

    def log_session(self, session_data: Dict[str, Any]):
        """Log a session's usage."""
        today = date.today().isoformat()
        daily_file = DAILY_LOG / f'{today}.json'

        # Load existing daily data
        if daily_file.exists():
            daily_data = json.loads(daily_file.read_text())
        else:
            daily_data = {'date': today, 'sessions': [], 'totals': {}}

        # Add session
        daily_data['sessions'].append({
            'session_id': session_data.get('session_id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'commands': session_data.get('commands', []),
            'duration_seconds': session_data.get('duration', 0),
        })

        # Save
        daily_file.write_text(json.dumps(daily_data, indent=2))

    def get_daily_summary(self, day: Optional[str] = None) -> Dict[str, Any]:
        """Get usage summary for a day."""
        day = day or date.today().isoformat()
        daily_file = DAILY_LOG / f'{day}.json'

        if not daily_file.exists():
            return {'date': day, 'sessions': 0, 'commands': []}

        data = json.loads(daily_file.read_text())
        return {
            'date': day,
            'sessions': len(data.get('sessions', [])),
            'commands': self._count_commands(data),
        }

    def get_monthly_report(self) -> str:
        """Generate monthly usage report."""
        current_month = date.today().strftime('%Y-%m')

        total_sessions = 0
        command_counts: Dict[str, int] = {}
        days_active = 0

        for daily_file in DAILY_LOG.glob(f'{current_month}-*.json'):
            days_active += 1
            data = json.loads(daily_file.read_text())
            total_sessions += len(data.get('sessions', []))

            for cmd, count in self._count_commands(data).items():
                command_counts[cmd] = command_counts.get(cmd, 0) + count

        report = f"""
──────────────────────────────────────────────────
📊 MONTHLY USAGE REPORT - {current_month}
──────────────────────────────────────────────────

Days Active:    {days_active}
Total Sessions: {total_sessions}

Command Usage:
"""
        for cmd, count in sorted(command_counts.items(), key=lambda x: -x[1]):
            report += f"  • {cmd}: {count}\n"

        report += """
──────────────────────────────────────────────────
"""
        return report

    def _count_commands(self, data: Dict) -> Dict[str, int]:
        """Count commands in daily data."""
        counts: Dict[str, int] = {}
        for session in data.get('sessions', []):
            for cmd in session.get('commands', []):
                counts[cmd] = counts.get(cmd, 0) + 1
        return counts


def format_usage_output(tracker: CostTracker) -> str:
    """Format usage for display."""
    summary = tracker.get_daily_summary()

    output = "\n" + "─" * 50 + "\n"
    output += "📊 TODAY'S USAGE\n"
    output += "─" * 50 + "\n"
    output += f"Sessions: {summary['sessions']}\n"

    if summary['commands']:
        output += "Commands:\n"
        for cmd, count in summary['commands'].items():
            output += f"  • {cmd}: {count}\n"

    output += "─" * 50 + "\n"

    return output


def main():
    """Hook entry point - runs on Stop event."""
    try:
        input_data = json.load(sys.stdin)

        tracker = CostTracker()

        # Log session
        tracker.log_session({
            'session_id': input_data.get('session_id', 'unknown'),
            'commands': input_data.get('commands', []),
            'duration': input_data.get('duration', 0),
        })

        # Output daily summary
        print(format_usage_output(tracker))

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
```

**Add command for viewing costs:**

**File:** `commands/costs.md`

```markdown
# Costs

View token usage and cost estimates.

## Arguments

- `$ARGUMENTS` - "today", "week", "month", or specific date (YYYY-MM-DD)

## Instructions

### Today's Usage
```bash
cat .claude/metrics/daily/$(date +%Y-%m-%d).json
```

### Weekly Summary
Read last 7 daily files and aggregate.

### Monthly Report
Read all daily files for current month.

## Output

```
┌─────────────────────────────────────────────────────────────┐
│  📊 USAGE REPORT                                            │
├─────────────────────────────────────────────────────────────┤
│  Period: January 2026                                       │
│                                                             │
│  Sessions: 45                                               │
│  Days Active: 15                                            │
│                                                             │
│  Top Commands:                                              │
│  • /ship: 12                                                │
│  • /plan: 18                                                │
│  • /review: 15                                              │
│                                                             │
│  Estimated Cost: ~$XX.XX                                    │
│  (Based on average tokens per command)                      │
└─────────────────────────────────────────────────────────────┘
```
```

---

## Phase 4: Context Persistence

### 4.1 Cross-Session Context

**Why:** Each `/plan` starts fresh, losing previous decisions and patterns.

**File:** `.claude/context/session_context.json` (structure)

```json
{
  "version": "1.0",
  "lastUpdated": "2026-01-20T10:00:00Z",

  "previousPlans": [
    {
      "file": ".claude/plans/plan-user-auth.md",
      "created": "2026-01-18T10:00:00Z",
      "status": "implemented",
      "summary": "Added user authentication with JWT"
    },
    {
      "file": ".claude/plans/plan-dashboard.md",
      "created": "2026-01-19T14:00:00Z",
      "status": "implemented",
      "summary": "Created dashboard with charts"
    }
  ],

  "decisions": [
    {
      "decision": "Use feature-based structure",
      "reason": "Better scalability for growing team",
      "date": "2026-01-15",
      "context": "During /plan for user-auth feature"
    },
    {
      "decision": "Zustand over Redux",
      "reason": "Simpler API, less boilerplate",
      "date": "2026-01-16",
      "context": "State management discussion"
    }
  ],

  "patterns": {
    "dataFetching": "TanStack Query with queryOptions factory",
    "stateManagement": "Zustand with useShallow",
    "forms": "React Hook Form + Zod",
    "styling": "Tailwind + cn() helper",
    "testing": "Vitest + React Testing Library"
  },

  "blockedPatterns": [
    {
      "pattern": "Redux",
      "reason": "Project uses Zustand",
      "since": "2026-01-16"
    },
    {
      "pattern": "CSS Modules",
      "reason": "Project uses Tailwind",
      "since": "2026-01-10"
    }
  ],

  "recentLessons": [
    {
      "lesson": "Always check for existing utilities before creating new ones",
      "learned": "2026-01-19",
      "context": "Found 3 duplicate date formatters"
    }
  ]
}
```

**File:** `hooks/context_loader.py`

```python
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
            output_parts.append(f"  • {plan['summary']} ({plan['status']})")

    # Key decisions
    decisions = context.get('decisions', [])[-5:]  # Last 5
    if decisions:
        output_parts.append("\nKey Decisions:")
        for d in decisions:
            output_parts.append(f"  • {d['decision']}: {d['reason']}")

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
            output_parts.append(f"  • {b['pattern']} ({b['reason']})")

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

        # Only show context for planning/implementation
        relevant_keywords = ['plan', 'implement', 'create', 'add', 'build', 'feature']
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
```

**File:** `hooks/context_updater.py`

```python
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
```

---

## Phase 5: Memory Auto-Update

### 5.1 Prompt for Lessons After Sessions

**Why:** `decisions.md` and `lessons.md` require manual updates.

**File:** `hooks/memory_updater.py`

```python
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
```

**File:** `commands/memory.md`

```markdown
# Memory

Manage project memory (decisions and lessons).

## Arguments

- `decision "description"` - Add a new decision
- `lesson "description"` - Add a new lesson
- `show` - Show current memory
- `skip` - Dismiss memory update prompt

## Instructions

### Add Decision

Append to `.claude/memory/decisions.md`:

```markdown
## {date} - {description}

Context: {current task/feature}
Reason: {why this decision was made}
```

### Add Lesson

Append to `.claude/memory/lessons.md`:

```markdown
## {date} - {description}

Context: {what happened}
Solution: {how it was resolved}
Prevention: {how to avoid in future}
```

### Show Memory

Display current contents of:
- `.claude/memory/decisions.md`
- `.claude/memory/lessons.md`
- `.claude/context/session_context.json` (patterns)

## Output

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Memory updated                                           │
├─────────────────────────────────────────────────────────────┤
│  Added to decisions.md:                                     │
│  "Use feature-based structure for new modules"              │
│                                                             │
│  Total: 15 decisions, 8 lessons                             │
└─────────────────────────────────────────────────────────────┘
```
```

---

## Phase 6: Circuit Breaker (Safety)

### 6.1 Safety Limits for `/ralph`

**File:** `hooks/circuit_breaker.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Circuit breaker for autonomous loops.
Prevents runaway execution and API budget burn.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple

# Configuration (can be overridden via flags)
DEFAULT_MAX_ITERATIONS = 50
DEFAULT_MAX_CALLS_PER_HOUR = 100
STAGNATION_THRESHOLD = 3  # Loops with no file changes
ERROR_REPEAT_THRESHOLD = 5  # Same error repeated

STATE_FILE = Path('.claude/circuit_breaker_state.json')


class CircuitBreaker:
    """
    Three-state circuit breaker:
    - CLOSED: Normal operation
    - HALF_OPEN: Testing recovery
    - OPEN: Stopped, requires reset
    """

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
        return self._initial_state()

    def _initial_state(self) -> dict:
        return {
            'status': 'CLOSED',
            'iterations': 0,
            'calls_this_hour': 0,
            'hour_started': datetime.now().isoformat(),
            'consecutive_no_changes': 0,
            'last_error': None,
            'error_repeat_count': 0,
            'trip_reason': None,
            'history': []
        }

    def _save_state(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(self.state, indent=2))

    def should_continue(self, max_iterations: int = DEFAULT_MAX_ITERATIONS) -> Tuple[bool, Optional[str]]:
        """Check if execution should continue."""

        # Circuit open
        if self.state['status'] == 'OPEN':
            return False, f"Circuit OPEN: {self.state.get('trip_reason', 'Manual stop')}"

        # Iteration limit
        if self.state['iterations'] >= max_iterations:
            self._trip(f"Max iterations ({max_iterations}) reached")
            return False, f"Max iterations ({max_iterations}) reached"

        # Rate limit (hourly reset)
        hour_start = datetime.fromisoformat(self.state['hour_started'])
        if datetime.now() - hour_start > timedelta(hours=1):
            self.state['calls_this_hour'] = 0
            self.state['hour_started'] = datetime.now().isoformat()

        if self.state['calls_this_hour'] >= DEFAULT_MAX_CALLS_PER_HOUR:
            return False, f"Rate limit ({DEFAULT_MAX_CALLS_PER_HOUR}/hour) - resets in {60 - (datetime.now() - hour_start).seconds // 60} min"

        # Stagnation detection
        if self.state['consecutive_no_changes'] >= STAGNATION_THRESHOLD:
            self._trip(f"Stagnation: {STAGNATION_THRESHOLD} loops with no changes")
            return False, f"Stagnation detected ({STAGNATION_THRESHOLD} loops with no file changes)"

        # Repeated errors
        if self.state['error_repeat_count'] >= ERROR_REPEAT_THRESHOLD:
            self._trip(f"Repeated error: {self.state['last_error'][:50]}")
            return False, f"Same error repeated {ERROR_REPEAT_THRESHOLD} times"

        return True, None

    def record_iteration(self, files_changed: int, error: Optional[str] = None):
        """Record iteration result."""
        self.state['iterations'] += 1
        self.state['calls_this_hour'] += 1

        # Track stagnation
        if files_changed == 0:
            self.state['consecutive_no_changes'] += 1
        else:
            self.state['consecutive_no_changes'] = 0

        # Track repeated errors
        if error:
            if error == self.state['last_error']:
                self.state['error_repeat_count'] += 1
            else:
                self.state['last_error'] = error
                self.state['error_repeat_count'] = 1
        else:
            self.state['last_error'] = None
            self.state['error_repeat_count'] = 0

        # History (last 50)
        self.state['history'].append({
            'iteration': self.state['iterations'],
            'files_changed': files_changed,
            'error': error[:100] if error else None,
            'timestamp': datetime.now().isoformat()
        })
        self.state['history'] = self.state['history'][-50:]

        self._save_state()

    def _trip(self, reason: str):
        """Open the circuit breaker."""
        self.state['status'] = 'OPEN'
        self.state['trip_reason'] = reason
        self._save_state()

    def reset(self):
        """Reset circuit breaker."""
        self.state = self._initial_state()
        self._save_state()

    def get_status(self) -> str:
        """Get formatted status."""
        return f"""
──────────────────────────────────────────────────
🔌 CIRCUIT BREAKER STATUS
──────────────────────────────────────────────────
Status:         {self.state['status']}
Iterations:     {self.state['iterations']}
Calls/Hour:     {self.state['calls_this_hour']}/{DEFAULT_MAX_CALLS_PER_HOUR}
No-Change Runs: {self.state['consecutive_no_changes']}/{STAGNATION_THRESHOLD}
Error Repeats:  {self.state['error_repeat_count']}/{ERROR_REPEAT_THRESHOLD}
{f"Trip Reason:    {self.state['trip_reason']}" if self.state['trip_reason'] else ""}
──────────────────────────────────────────────────
"""


def main():
    """Hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '').lower()

        # Only apply to /ralph
        if '/ralph' not in prompt and '/adx:ralph' not in prompt:
            sys.exit(0)

        # Check for reset flag
        if '--reset' in prompt:
            cb = CircuitBreaker()
            cb.reset()
            print("[circuit-breaker] Reset complete")
            sys.exit(0)

        # Check for status flag
        if '--status' in prompt:
            cb = CircuitBreaker()
            print(cb.get_status())
            sys.exit(0)

        # Normal check
        cb = CircuitBreaker()
        can_continue, reason = cb.should_continue()

        if not can_continue:
            print(f"""
──────────────────────────────────────────────────
🛑 CIRCUIT BREAKER TRIGGERED
──────────────────────────────────────────────────
{reason}

Options:
  /ralph --status   View detailed status
  /ralph --reset    Reset and retry
  Fix issues manually, then /ralph --reset
──────────────────────────────────────────────────
""")
            sys.exit(1)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
```

---

## Phase 7: Discovery System

### 7.1 `/discover` Command

**File:** `commands/discover.md`

```markdown
# Discover

Research latest Claude Code patterns and suggest toolkit improvements.

## Arguments

- `$ARGUMENTS` - Focus: "hooks", "agents", "workflows", "security", "all"

## Instructions

Use the pattern-researcher agent to:

1. **Search official sources**
   - Anthropic docs and blog
   - Claude Code repository

2. **Search community sources**
   - awesome-claude-code
   - GitHub claude-code topic

3. **Compare with current toolkit**
   - What's missing?
   - What's outdated?

4. **Generate report**
   - New patterns found
   - Recommendations
   - Implementation effort

## Output

Save report to `.claude/discovery/report-{date}.md`
```

### 7.2 Pattern Researcher Agent

**File:** `agents/pattern-researcher.md`

```yaml
---
name: pattern-researcher
description: Research Claude Code ecosystem for new patterns and improvements
tools: WebSearch, WebFetch, Read, Grep, Glob
model: sonnet
---

# Pattern Researcher

Research the Claude Code ecosystem to discover improvements for this toolkit.

## Sources

**Official:**
- https://docs.anthropic.com/en/docs/claude-code
- https://www.anthropic.com/engineering
- https://github.com/anthropics/claude-code

**Community:**
- https://github.com/hesreallyhim/awesome-claude-code
- https://github.com/topics/claude-code

## Process

1. Fetch latest from sources
2. Extract patterns/features
3. Compare with: commands/*.md, agents/*.md, hooks/*.py
4. Assess applicability
5. Generate prioritized recommendations

## Output Format

For each pattern:
- Name and source
- Already implemented? (Yes/No/Partial)
- Should add? (Yes/No + reason)
- Effort: Low/Medium/High
```

---

## Phase 8: Integration

### 8.1 Update `settings.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {"type": "command", "command": "uv run hooks/dev_standards_loader.py || true"},
          {"type": "command", "command": "uv run hooks/context_loader.py || true"},
          {"type": "command", "command": "uv run hooks/plan_first_enforcer.py || true"},
          {"type": "command", "command": "uv run hooks/smart_context_loader.py || true"},
          {"type": "command", "command": "uv run hooks/circuit_breaker.py || true"}
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {"type": "command", "command": "uv run hooks/context_updater.py || true"},
          {"type": "command", "command": "uv run hooks/cost_tracker.py || true"},
          {"type": "command", "command": "uv run hooks/memory_updater.py || true"},
          {"type": "command", "command": "uv run hooks/stop.py --chat --summary || true"}
        ]
      }
    ]
  }
}
```

### 8.2 Updated `/ship` Workflow

```
/ship "description"
    ├─ CHECKPOINT: start
    ↓
Step 1: PLAN (read-only)
    ├─ CHECKPOINT: after plan
    ↓
Step 2: IMPLEMENT (write access)
    ├─ CHECKPOINT: after implement
    ↓
Step 3: REFACTOR
    ├─ CHECKPOINT: after refactor
    ↓
Step 4: VERIFY (includes tests if detected)
    ├─ Type check → Lint → Build → Tests (optional)
    ├─ CHECKPOINT: after verify
    ↓
Step 5: REVIEW (parallel)
    ├─ code-reviewer (with explorer spawning)
    ├─ security-auditor
    ├─ performance-auditor
    ├─ Optional: browser-tester
    ↓
Step 6: COMMIT
    ↓
Step 7: PR
    ↓
✓ SHIPPED (checkpoint cleared)
```

---

## Implementation Order

| Week | Phase | Items |
|------|-------|-------|
| 1 | Critical | `/verify` with tests, security-auditor, checkpoints |
| 2 | Orchestration | Subagent spawning in code-reviewer, refactorer |
| 3 | Persistence | Context loader/updater, cost tracking |
| 4 | Memory | Memory auto-update, `/memory` command |
| 5 | Safety | Circuit breaker for `/ralph` |
| 6 | Discovery | `/discover` command, pattern-researcher |
| 7 | Integration | Hook updates, testing, version bump |

---

## Files to Create

```
commands/
├── verify.md          # Updated with testing
├── memory.md          # Memory management
├── costs.md           # Usage viewing
├── discover.md        # Pattern discovery

agents/
├── verifier.md        # Verify + test agent
├── security-auditor.md
├── pattern-researcher.md

hooks/
├── checkpoint.py      # Rollback points
├── circuit_breaker.py # Safety limits
├── context_loader.py  # Load session context
├── context_updater.py # Update session context
├── cost_tracker.py    # Token usage
├── memory_updater.py  # Prompt for lessons
├── plan_first_enforcer.py

.claude/
├── context/
│   └── session_context.json
├── memory/
│   ├── decisions.md
│   └── lessons.md
├── metrics/
│   └── daily/
```

---

## Success Criteria

- [ ] `/verify` runs tests when detected, skips gracefully when not
- [ ] Security auditor catches hardcoded secrets
- [ ] `/ship --continue` resumes from checkpoint
- [ ] code-reviewer spawns explorer for verification
- [ ] Cost tracking logs daily usage
- [ ] Context persists across sessions
- [ ] Memory update prompt appears after `/review`
- [ ] Circuit breaker stops runaway `/ralph`
- [ ] `/discover` finds and reports new patterns

---

## Sources

- [RIPER-5 Workflow](https://github.com/tony/claude-code-riper-5)
- [Ralph Claude Code](https://github.com/frankbria/ralph-claude-code)
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

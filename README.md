# ADX Toolkit v3.0

A Claude Code plugin for React/TypeScript frontend development with autonomous agentic workflows.

> **Plugin ID:** `adx-toolkit`
> **Commands:** `adx:plan`, `adx:ship`, `adx:review`, `adx:ralph`, etc.

## What's New in v3.0

- **Testing Integration** - `/verify` now auto-detects and runs tests
- **Security Auditing** - New `security-auditor` agent scans for vulnerabilities
- **Checkpoint System** - `/ship` can resume from failures with `--continue`
- **Subagent Orchestration** - Agents spawn other agents for verification
- **Cost Tracking** - Monitor usage with `/costs` command
- **Context Persistence** - Decisions and patterns persist across sessions
- **Memory Management** - `/memory` command for lessons and decisions
- **Circuit Breaker** - Safety limits prevent runaway `/ralph` loops
- **Pattern Discovery** - `/discover` finds new Claude Code patterns

---

## Features

- **Agentic Workflow** - `/ship` command runs full pipeline automatically
- **RALPH Integration** - Fully autonomous loop until PR created (fire and forget)
- **Browser Verification** - Visual testing with Claude Chrome extension (fix-verify loop)
- **Specialized Agents** - Code review, refactoring, security audit, git automation, research
- **Smart Commands** - Plan, implement, verify, review, commit, PR
- **Project Conventions** - CLAUDE.md enforces your patterns
- **Hooks System** - Context detection, session summaries, cost tracking, memory updates
- **Checkpoint Recovery** - Resume failed `/ship` runs from last successful phase

---

## Quick Start

### One-liner Install (Recommended)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install-adx.sh)
```

This will:
1. Add the ADX marketplace to Claude Code
2. Install the ADX plugin with all commands namespaced as `/adx:*`

### Manual Install (via Claude Code CLI)

```bash
# Add the marketplace
claude plugin marketplace add adxable/adx-toolkit

# Install the plugin
claude plugin install adx@adx-marketplace
```

### Interactive Install (via Claude Code)

1. Run `/plugin` in Claude Code
2. Go to **Marketplaces** tab → Add `adxable/adx-toolkit`
3. Go to **Browse** tab → Install `adx`

### Project Setup (Optional)

After installing the plugin, run the setup wizard to configure your project:

```bash
# Clone and run setup for hooks, memory, and CLAUDE.md
git clone https://github.com/adxable/adx-toolkit.git /tmp/adx-toolkit
/tmp/adx-toolkit/setup.sh
```

### Development (Symlink)

```bash
ln -s /path/to/adx-toolkit ~/.claude/plugins/adx-toolkit
```

---

## Commands

### Full Workflow (Autonomous)

```bash
# Single-pass autonomous (you may need to intervene on errors)
/adx:ship "add user authentication with JWT"

# With browser verification (recommended for UI features)
/adx:ship "add login form" --browser

# Fully autonomous loop until PR (fire and forget)
/adx:ralph "add dashboard with charts" --browser --monitor
```

**Modes:**
- `/adx:ship` - Single pass through pipeline, stops on completion or error
- `/adx:ralph` - Continuous loop until PR created, handles failures automatically

### Individual Commands

| Command | Description | Agent Used |
|---------|-------------|------------|
| `/adx:plan <description>` | Research and create implementation plan | `explorer` |
| `/adx:implement <plan-path>` | Execute plan step by step | `web-researcher` (if stuck) |
| `/adx:refactor [files]` | Clean up code, remove technical debt | `refactorer` |
| `/adx:verify [flags]` | Type check + lint + build + tests | `verifier` |
| `/adx:review [files]` | Code review + security audit | `code-reviewer`, `security-auditor` |
| `/adx:review --browser` | Code review + visual verification | Above + `browser-tester` |
| `/adx:commit [type]` | Create git commit | `git-automator` |
| `/adx:pr [base]` | Create pull request | `git-automator` |
| `/adx:ralph <description>` | Fully autonomous loop until PR | All agents (via RALPH) |

### New v3.0 Commands

| Command | Description |
|---------|-------------|
| `/adx:costs [period]` | View usage metrics (today, week, month) |
| `/adx:memory [action]` | Manage decisions and lessons |
| `/adx:discover [focus]` | Research new Claude Code patterns |

### Ship Recovery (v3.0)

```bash
# Resume from last checkpoint
/adx:ship --continue

# Start from specific phase
/adx:ship --from verify

# Rollback to checkpoint
/adx:ship --rollback implement

# View checkpoint status
/adx:ship --status
```

### Verify Flags (v3.0)

```bash
# Full verification (static + tests + browser)
/adx:verify

# Skip tests
/adx:verify --skip-tests

# Tests only
/adx:verify --tests-only

# Include E2E tests
/adx:verify --e2e

# Auto-fix issues
/adx:verify --fix

# Skip browser verification
/adx:verify --skip-browser
```

### Workflow Diagram

```
/adx:plan "feature description"
    │
    ↓ creates .claude/plans/plan-{name}.md
    │ CHECKPOINT saved
    ↓
/adx:implement .claude/plans/plan-{name}.md
    │
    ↓ creates/modifies files
    │ CHECKPOINT saved
    ↓
/adx:refactor
    │
    ↓ cleans up code (refactorer agent with explorer spawning)
    │ CHECKPOINT saved
    ↓
/adx:verify
    │
    ↓ type check + lint + build + tests (if detected)
    │ CHECKPOINT saved
    ↓
/adx:review --browser
    │
    ├── Phase 1: Code Review (parallel)
    │   ├── code-reviewer (spawns explorer for verification)
    │   ├── security-auditor
    │   ├── performance-auditor
    │   └── accessibility-tester
    │
    └── Phase 2: Browser Verification (fix-verify loop)
        └── browser-tester
    │
    ↓ generates .claude/reviews/review-{date}.md
    │ CHECKPOINT saved
    ↓
/adx:commit
    │
    ↓ creates commit with Co-Authored-By
    │ CHECKPOINT saved
    ↓
/adx:pr
    │
    ↓ creates PR with description
    │ CHECKPOINT cleared

✓ DONE
```

---

## Agents

### Core Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `explorer` | haiku | Fast codebase search and pattern discovery |
| `web-researcher` | sonnet | Internet research for debugging and solutions |
| `code-reviewer` | opus | Code review with markdown report output (spawns explorer) |
| `refactorer` | opus | Code cleanup, remove `any` types (spawns explorer) |
| `verifier` | sonnet | Type check, lint, build, tests with auto-fix |
| `security-auditor` | sonnet | Scan for secrets, vulnerabilities, dangerous patterns |
| `git-automator` | sonnet | Smart commits, branches, and PRs |
| `performance-auditor` | opus | Bundle size, React re-renders, memoization |
| `browser-tester` | opus | Visual UI testing, interaction testing, fix-verify loop |
| `pattern-researcher` | sonnet | Research Claude Code ecosystem for improvements |

### Optional Agents

| Agent | Purpose |
|-------|---------|
| `accessibility-tester` | WCAG compliance, a11y audits |
| `docs-generator` | README, JSDoc, API documentation |

### Subagent Orchestration (v3.0)

Agents can spawn other agents for verification:

```
[code-reviewer] Reviewing: src/features/orders/OrderCard.tsx
[code-reviewer] → Uncertain: Component uses 'handleClick' naming
[code-reviewer] → Spawning explorer to verify convention...

[explorer] Searching for event handler naming patterns...
[explorer] Found: 85% use 'handleX' pattern, 15% use 'onX'

[code-reviewer] ✓ Naming follows project convention
```

### Agent Terminal Output

When agents are invoked, they display status in terminal:

```
┌─────────────────────────────────────────────────┐
│  🔍 AGENT: security-auditor                     │
│  📋 Task: Scan for vulnerabilities              │
│  ⚡ Model: sonnet                               │
└─────────────────────────────────────────────────┘

[security-auditor] Scanning for hardcoded secrets...
[security-auditor] Scanning for dangerous patterns...
[security-auditor] Running npm audit...
[security-auditor] ✓ Complete (Critical: 0, High: 1, Medium: 2)
```

---

## Browser Verification

Visual and functional testing using Claude Chrome extension.

### Prerequisites

- Dev server running (`pnpm dev`)
- Claude Chrome extension installed and connected

### How It Works

Claude Chrome extension allows Claude to see and interact with your browser:

```
┌──────────────────────────────────────────────────────────┐
│                    FIX-VERIFY LOOP                        │
│                                                          │
│    ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│    │  View   │ ──▶ │ Analyze │ ──▶ │  Fix    │          │
│    │ Browser │     │         │     │  Code   │          │
│    └─────────┘     └─────────┘     └────┬────┘          │
│         ▲                               │                │
│         │         (if still broken)     │                │
│         └───────────────────────────────┘                │
│                                                          │
│    Max iterations: 5                                     │
└──────────────────────────────────────────────────────────┘
```

Claude can:
- **See** the browser viewport in real-time
- **Click** buttons, links, interactive elements
- **Type** into inputs and forms
- **Navigate** between pages

### What It Tests

- **Visual verification** - Components render correctly
- **Interaction testing** - Buttons, forms, modals work
- **Responsive design** - Mobile, tablet, desktop
- **State handling** - Loading, error, empty states

### Usage

```bash
# Code review + browser verification
/adx:review --browser

# Browser verification only (skip code review)
/adx:review --browser-only

# Full ship workflow with browser
/adx:ship "add user dashboard" --browser
```

---

## RALPH Integration (Fully Autonomous)

RALPH enables continuous, self-improving development loops until project completion.

### What is RALPH?

RALPH (from [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)) wraps Claude Code in an autonomous loop with intelligent safeguards:

- **Continuous execution** until PR created
- **Automatic failure handling** and retries
- **Circuit breaker** stops infinite loops (v3.0)
- **Rate limiting** prevents API overuse
- **Session continuity** across iterations

### Circuit Breaker (v3.0)

Prevents runaway execution:

```
┌─────────────────────────────────────────────────────────────┐
│  🛑 CIRCUIT BREAKER TRIGGERED                               │
├─────────────────────────────────────────────────────────────┤
│  Reason: Stagnation (3 loops with no file changes)          │
│                                                             │
│  Options:                                                   │
│  • /ralph --status   View detailed status                   │
│  • /ralph --reset    Reset and retry                        │
│  • Fix issues manually, then /ralph --reset                 │
└─────────────────────────────────────────────────────────────┘
```

Limits:
- Max 50 iterations
- Max 100 API calls/hour
- Stagnation detection (3 loops with no changes)
- Repeated error detection (5 same errors)

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                      RALPH + /ship                           │
│                                                             │
│   RALPH Loop:                                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Read PROMPT.md → Execute /ship → Track Progress    │   │
│   │       ↓                                             │   │
│   │  Success? → PR created → EXIT_SIGNAL → Done         │   │
│   │       ↓                                             │   │
│   │  Failure? → Analyze → Fix → Loop again              │   │
│   │       ↓                                             │   │
│   │  Circuit Breaker? → Stop → Report                   │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   Safeguards: Circuit breaker, rate limiting, timeout       │
└─────────────────────────────────────────────────────────────┘
```

### Installation

```bash
# Install RALPH globally (one-time)
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code
./install.sh
```

### Usage

```bash
# Initialize RALPH project with adx-toolkit templates
./scripts/ralph-init.sh "add user authentication" --browser

# Start autonomous development
cd .ralph-projects/add-user-authentication
ralph --monitor --timeout 60
```

Or use the `/adx:ralph` command:

```bash
/adx:ralph "add shopping cart" --browser --monitor
```

### /adx:ship vs /adx:ralph

| Aspect | /adx:ship | /adx:ralph |
|--------|-----------|------------|
| Execution | Single pass | Loop until done |
| Failures | Stop and report | Retry automatically |
| Duration | Minutes | Minutes to hours |
| Human involvement | May need intervention | Fire and forget |
| Best for | Known scope | Complex/exploratory |
| Recovery | `--continue` flag | Circuit breaker reset |

---

## Memory & Context System (v3.0)

### Session Context

Context persists across sessions in `.claude/context/session_context.json`:

```json
{
  "previousPlans": [...],
  "decisions": [...],
  "patterns": {
    "dataFetching": "TanStack Query with queryOptions",
    "stateManagement": "Zustand with useShallow"
  },
  "blockedPatterns": [...],
  "recentLessons": [...]
}
```

### Memory Commands

```bash
# Add a decision
/adx:memory decision "Use TanStack Query queryOptions factory"

# Add a lesson
/adx:memory lesson "Zustand without useShallow causes infinite loops"

# View all memory
/adx:memory show
```

### Output

```
┌─────────────────────────────────────────────────────────────┐
│  📚 PROJECT MEMORY                                          │
├─────────────────────────────────────────────────────────────┤
│  DECISIONS (5 total)                                        │
│  • 2026-01-20: Use TanStack Query queryOptions factory      │
│  • 2026-01-18: Feature-based folder structure               │
│                                                             │
│  LESSONS (3 total)                                          │
│  • 2026-01-20: Zustand + useShallow for object selectors    │
│                                                             │
│  ESTABLISHED PATTERNS                                       │
│  • dataFetching: TanStack Query with queryOptions           │
│  • stateManagement: Zustand with useShallow                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Cost Tracking (v3.0)

Monitor your usage with the `/costs` command:

```bash
# Today's usage
/adx:costs today

# This week
/adx:costs week

# This month
/adx:costs month
```

Output:

```
┌─────────────────────────────────────────────────────────────┐
│  📊 USAGE REPORT                                            │
├─────────────────────────────────────────────────────────────┤
│  Period: January 2026                                       │
│  Sessions: 45                                               │
│  Days Active: 15                                            │
│                                                             │
│  Top Commands:                                              │
│  • /ship: 12                                                │
│  • /plan: 18                                                │
│  • /review: 15                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Pattern Discovery (v3.0)

Research the Claude Code ecosystem for improvements:

```bash
# Research all patterns
/adx:discover all

# Focus on specific area
/adx:discover hooks
/adx:discover agents
/adx:discover workflows
/adx:discover security
```

Generates report at `.claude/discovery/report-{date}.md` with:
- New patterns found
- Comparison with current toolkit
- Prioritized recommendations

---

## Security Auditing (v3.0)

The `security-auditor` agent scans for:

### Hardcoded Secrets
- API keys and tokens
- Passwords
- AWS credentials
- Private keys

### Dangerous Patterns
- XSS vulnerabilities (innerHTML, dangerouslySetInnerHTML)
- Code injection (eval, new Function)
- SQL injection patterns

### Configuration Issues
- `.env` files in git
- Debug mode in production
- CORS set to `*`

### Output

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
└─────────────────────────────────────────────────────────────┘
```

---

## Skills

### Installed Skills (`.claude/skills/`)

| Skill | Source | Purpose |
|-------|--------|---------|
| `frontend-design` | Anthropic | Bold UI design, avoid generic aesthetics |
| `webapp-testing` | Anthropic | Playwright testing patterns |
| `tdd` | obra/superpowers | Test-driven development workflow |

### Plugin Skills (`skills/`)

| Skill | Purpose |
|-------|---------|
| `browser-testing` | Visual testing patterns, fix-verify loop workflows |

---

## Project Conventions (CLAUDE.md)

The plugin includes a `CLAUDE.md` template with your project conventions:

```markdown
## Tech Stack
- Router: TanStack Router / React Router v7
- State: Zustand (UI state only)
- Server State: TanStack Query with useSuspenseQuery
- Forms: React Hook Form + Zod
- Styling: Tailwind + shadcn/ui

## Enforced Patterns
- useShallow for Zustand object selectors
- Query Options Factory pattern
- cn() for conditional Tailwind classes
- Named exports, not default

## Anti-patterns - NEVER
- Zustand selector without useShallow
- any in TypeScript
- Index as key in lists
- Inline functions for memoized children
```

---

## Directory Structure

```
adx-toolkit/
├── CLAUDE.md                    # Project conventions template
├── .claude/
│   ├── skills/
│   │   ├── frontend-design/     # Anthropic official
│   │   ├── webapp-testing/      # Anthropic official
│   │   └── tdd/                 # obra/superpowers
│   ├── plans/                   # /plan outputs
│   ├── reviews/                 # /review outputs
│   ├── context/                 # Session context (v3.0)
│   │   └── session_context.json
│   ├── memory/                  # Decisions & lessons (v3.0)
│   │   ├── decisions.md
│   │   └── lessons.md
│   ├── metrics/                 # Usage tracking (v3.0)
│   │   └── daily/
│   ├── checkpoints/             # Ship recovery (v3.0)
│   └── discovery/               # Pattern research (v3.0)
├── skills/
│   └── browser-testing/         # Plugin-provided skill
│       └── SKILL.md
├── agents/
│   ├── explorer.md
│   ├── web-researcher.md
│   ├── code-reviewer.md         # With subagent orchestration
│   ├── refactorer.md            # With subagent orchestration
│   ├── verifier.md              # NEW in v3.0
│   ├── security-auditor.md      # NEW in v3.0
│   ├── pattern-researcher.md    # NEW in v3.0
│   ├── git-automator.md
│   ├── performance-auditor.md
│   ├── browser-tester.md
│   └── optional/
│       ├── accessibility-tester.md
│       └── docs-generator.md
├── commands/
│   ├── ship.md                  # With checkpoint system
│   ├── ralph.md                 # With circuit breaker
│   ├── plan.md
│   ├── implement.md
│   ├── refactor.md
│   ├── verify.md                # With test support
│   ├── review.md
│   ├── commit.md
│   ├── pr.md
│   ├── costs.md                 # NEW in v3.0
│   ├── memory.md                # NEW in v3.0
│   └── discover.md              # NEW in v3.0
├── hooks/
│   ├── checkpoint.py            # NEW in v3.0
│   ├── circuit_breaker.py       # NEW in v3.0
│   ├── context_loader.py        # NEW in v3.0
│   ├── context_updater.py       # NEW in v3.0
│   ├── cost_tracker.py          # NEW in v3.0
│   ├── memory_updater.py        # NEW in v3.0
│   ├── smart_context_loader.py
│   ├── stop.py
│   └── ...
├── scripts/
│   └── ralph-init.sh
├── templates/
│   └── ralph/
├── mcp.json
└── settings.json
```

---

## Hooks System

Python-based hooks for enhanced functionality.

### Core Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `smart_context_loader.py` | UserPromptSubmit | Auto-detects context, suggests skills |
| `context_loader.py` | UserPromptSubmit | Injects session context (v3.0) |
| `circuit_breaker.py` | UserPromptSubmit | Safety limits for /ralph (v3.0) |
| `stop.py` | Stop | Generates session summary |
| `context_updater.py` | Stop | Updates session context (v3.0) |
| `cost_tracker.py` | Stop | Logs usage metrics (v3.0) |
| `memory_updater.py` | Stop | Prompts for lessons (v3.0) |
| `checkpoint.py` | - | Manages /ship checkpoints (v3.0) |

### Smart Context Loader

Detects keywords in your prompt and suggests relevant context:

```
──────────────────────────────────────────────────
📋 SMART CONTEXT DETECTED
──────────────────────────────────────────────────

💡 Suggested Skills:
   → react-forms
   → zod-validation

📝 Context Notes:
   ❗ [FORMS] Consider validation, error states, accessibility

──────────────────────────────────────────────────
```

---

## MCP Integrations

Pre-configured MCP servers in `mcp.json`:

| Server | Purpose |
|--------|---------|
| `sequential-thinking` | Enhanced reasoning |
| `playwright` | Browser automation |
| `filesystem` | File operations |
| `memory` | Persistent storage |
| `fetch` | HTTP requests |
| `git` | Git operations |

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_HOOKS_LOG_DIR` | Log directory (default: `logs`) |
| `CLAUDE_PROJECT_DIR` | Project directory |

### settings.json

```json
{
  "permissions": {
    "allow": ["Edit:*", "Write:*", "Bash:*"]
  },
  "hooks": {
    "UserPromptSubmit": [
      "uv run hooks/dev_standards_loader.py",
      "uv run hooks/context_loader.py",
      "uv run hooks/circuit_breaker.py"
    ],
    "Stop": [
      "uv run hooks/context_updater.py",
      "uv run hooks/cost_tracker.py",
      "uv run hooks/memory_updater.py",
      "uv run hooks/stop.py"
    ]
  }
}
```

---

## Changelog

### v3.0 (2026-01-20)

**New Features:**
- Testing integration in `/verify` with auto-detection
- Security auditor agent for vulnerability scanning
- Checkpoint system for `/ship` recovery
- Subagent orchestration (agents spawning agents)
- Cost tracking with `/costs` command
- Context persistence across sessions
- Memory management with `/memory` command
- Circuit breaker for `/ralph` safety
- Pattern discovery with `/discover` command

**New Agents:**
- `verifier` - Type check, lint, build, test with auto-fix
- `security-auditor` - Scan for secrets and vulnerabilities
- `pattern-researcher` - Research Claude Code ecosystem

**New Commands:**
- `/adx:costs` - View usage metrics
- `/adx:memory` - Manage decisions and lessons
- `/adx:discover` - Research new patterns

**New Hooks:**
- `checkpoint.py` - Ship recovery checkpoints
- `circuit_breaker.py` - Ralph safety limits
- `context_loader.py` - Session context injection
- `context_updater.py` - Session context updates
- `cost_tracker.py` - Usage tracking
- `memory_updater.py` - Memory update prompts

**Improvements:**
- Code reviewer spawns explorer for pattern verification
- Refactorer spawns explorer before major changes
- `/verify` supports `--skip-tests`, `--tests-only`, `--e2e`, `--fix` flags
- `/ship` supports `--continue`, `--from`, `--rollback`, `--status` flags

---

## License

MIT

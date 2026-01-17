# ADX Toolkit

A Claude Code plugin for React/TypeScript frontend development with autonomous agentic workflows.

> **Plugin ID:** `adx-toolkit`
> **Commands:** `adx:plan`, `adx:ship`, `adx:review`, `adx:ralph`, etc.

## Features

- **Agentic Workflow** - `/ship` command runs full pipeline automatically
- **RALPH Integration** - Fully autonomous loop until PR created (fire and forget)
- **Browser Verification** - Visual testing with Claude Chrome extension (fix-verify loop)
- **Specialized Agents** - Code review, refactoring, git automation, research, browser testing
- **Smart Commands** - Plan, implement, verify, review, commit, PR
- **Project Conventions** - CLAUDE.md enforces your patterns
- **Hooks System** - Context detection, session summaries, logging

---

## Quick Start

### One-liner Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install.sh | bash
```

This will:
1. Clone the plugin to `~/.claude/plugins/adx-toolkit`
2. Launch interactive setup wizard
3. Configure your project with your tech stack preferences

### Manual Install

```bash
# Clone to your plugins directory
git clone https://github.com/adxable/adx-toolkit.git ~/.claude/plugins/adx-toolkit

# Run interactive setup
~/.claude/plugins/adx-toolkit/setup.sh
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
/ship "add user authentication with JWT"

# With browser verification (recommended for UI features)
/ship "add login form" --browser

# Fully autonomous loop until PR (fire and forget)
/ralph "add dashboard with charts" --browser --monitor
```

**Modes:**
- `/ship` - Single pass through pipeline, stops on completion or error
- `/ralph` - Continuous loop until PR created, handles failures automatically

### Individual Commands

| Command | Description | Agent Used |
|---------|-------------|------------|
| `/plan <description>` | Research and create implementation plan | `explorer` |
| `/implement <plan-path>` | Execute plan step by step | `web-researcher` (if stuck) |
| `/refactor [files]` | Clean up code, remove technical debt | `refactorer` |
| `/verify [url]` | Type check + lint + build loop | - |
| `/review [files]` | Code review, generate report | `code-reviewer`, `performance-auditor`, `accessibility-tester` |
| `/review --browser` | Code review + visual verification | Above + `browser-tester` |
| `/review --browser-only` | Visual verification only | `browser-tester` |
| `/commit [type]` | Create git commit | `git-automator` |
| `/pr [base]` | Create pull request | `git-automator` |
| `/ralph <description>` | Fully autonomous loop until PR | All agents (via RALPH) |

### Workflow Diagram

```
/plan "feature description"
    │
    ↓ creates .claude/plans/plan-{name}.md

/implement .claude/plans/plan-{name}.md
    │
    ↓ creates/modifies files

/refactor
    │
    ↓ cleans up code (refactorer agent)

/verify
    │
    ↓ type check + lint + build

/review --browser
    │
    ├── Phase 1: Code Review (3 agents parallel)
    │   ├── code-reviewer
    │   ├── performance-auditor
    │   └── accessibility-tester
    │
    └── Phase 2: Browser Verification (fix-verify loop)
        └── browser-tester
    │
    ↓ generates .claude/reviews/review-{date}.md

/commit
    │
    ↓ creates commit with Co-Authored-By

/pr
    │
    ↓ creates PR with description

✓ DONE
```

---

## Agents

### Core Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `explorer` | haiku | Fast codebase search and pattern discovery |
| `web-researcher` | sonnet | Internet research for debugging and solutions |
| `code-reviewer` | opus | Code review with markdown report output |
| `git-automator` | sonnet | Smart commits, branches, and PRs |
| `refactorer` | opus | Code cleanup, remove `any` types, dead code |
| `performance-auditor` | opus | Bundle size, React re-renders, memoization |
| `browser-tester` | opus | Visual UI testing, interaction testing, fix-verify loop |

### Optional Agents

| Agent | Purpose |
|-------|---------|
| `accessibility-tester` | WCAG compliance, a11y audits |
| `docs-generator` | README, JSDoc, API documentation |

Agents are invoked automatically by Claude when needed, or explicitly through commands.

### Agent Terminal Output

When agents are invoked, they display status in terminal:

```
┌─────────────────────────────────────────────────┐
│  🌐 AGENT: browser-tester                       │
│  📋 Task: Verify login form renders correctly   │
│  ⚡ Model: opus                                 │
└─────────────────────────────────────────────────┘

[browser-tester] Starting dev server...
[browser-tester] Screenshot: Login page
[browser-tester] Issue found: Button misaligned
[browser-tester] Fixing: LoginForm.tsx:45
[browser-tester] Re-verifying...
[browser-tester] ✓ Complete (Tests: 5, Issues Fixed: 1, Iterations: 2)
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
/review --browser

# Browser verification only (skip code review)
/review --browser-only

# Full ship workflow with browser
/ship "add user dashboard" --browser
```

---

## RALPH Integration (Fully Autonomous)

RALPH enables continuous, self-improving development loops until project completion.

### What is RALPH?

RALPH (from [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)) wraps Claude Code in an autonomous loop with intelligent safeguards:

- **Continuous execution** until PR created
- **Automatic failure handling** and retries
- **Circuit breaker** stops infinite loops
- **Rate limiting** prevents API overuse
- **Session continuity** across iterations

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

Or use the `/ralph` command:

```bash
/ralph "add shopping cart" --browser --monitor
```

### /ship vs /ralph

| Aspect | /ship | /ralph |
|--------|-------|--------|
| Execution | Single pass | Loop until done |
| Failures | Stop and report | Retry automatically |
| Duration | Minutes | Minutes to hours |
| Human involvement | May need intervention | Fire and forget |
| Best for | Known scope | Complex/exploratory |

### When to Use /ralph

- **Overnight development** - Start before bed, wake up to PR
- **Complex features** - Multiple unknowns, likely failures
- **Hands-off mode** - Don't want to monitor progress

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
│   └── reviews/                 # /review outputs
├── skills/
│   └── browser-testing/         # Plugin-provided skill
│       └── SKILL.md
├── agents/
│   ├── explorer.md
│   ├── web-researcher.md
│   ├── code-reviewer.md
│   ├── git-automator.md
│   ├── refactorer.md
│   ├── performance-auditor.md
│   ├── browser-tester.md        # Browser verification agent
│   └── optional/
│       ├── accessibility-tester.md
│       └── docs-generator.md
├── commands/
│   ├── ship.md                  # Single-pass autonomous workflow
│   ├── ralph.md                 # RALPH loop integration
│   ├── plan.md
│   ├── implement.md
│   ├── refactor.md
│   ├── verify.md
│   ├── review.md                # Supports --browser flag
│   ├── commit.md
│   └── pr.md
├── scripts/
│   └── ralph-init.sh            # Initialize RALPH project
├── templates/
│   └── ralph/                   # RALPH project templates
│       ├── PROMPT.md
│       └── @fix_plan.md
├── hooks/                       # Python hooks
│   ├── smart_context_loader.py
│   ├── stop.py
│   └── ...
├── memory/                      # Memory system templates
│   ├── CLAUDE.md
│   ├── decisions.md
│   ├── conventions.md
│   └── lessons.md
├── mcp.json                     # MCP server config
└── settings.json                # Claude Code settings
```

---

## Hooks System

Python-based hooks for enhanced functionality.

| Hook | Event | Description |
|------|-------|-------------|
| `smart_context_loader.py` | UserPromptSubmit | Auto-detects context, suggests skills |
| `stop.py` | Stop | Generates session summary |
| `user_prompt_submit.py` | UserPromptSubmit | Logs prompts |
| `pre_tool_use.py` | PreToolUse | Logs tool usage |
| `post_tool_use.py` | PostToolUse | Logs tool results |

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

## Memory System

Persistent context across sessions.

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project overview, conventions (auto-loaded) |
| `decisions.md` | Architecture Decision Records |
| `conventions.md` | Discovered code patterns |
| `lessons.md` | What worked, what didn't |

---

## Installation

### Recommended: Interactive Setup

```bash
# Install and configure in one command
curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install.sh | bash
```

The setup wizard will ask you about:
- **Project directory** - Where to configure ADX
- **Tech stack** - Router (TanStack/React Router/Next.js), State manager (Zustand/Jotai/Redux)
- **Features** - Hooks, MCP servers, memory system
- **Agents** - Which specialized agents to enable

### Manual Installation

```bash
# 1. Clone the plugin
git clone https://github.com/adxable/adx-toolkit.git ~/.claude/plugins/adx-toolkit

# 2. Run setup for your project
cd /your-project
~/.claude/plugins/adx-toolkit/setup.sh

# Or copy files manually:
cp ~/.claude/plugins/adx-toolkit/CLAUDE.md /your-project/CLAUDE.md
cp -r ~/.claude/plugins/adx-toolkit/hooks /your-project/.claude/hooks
cp ~/.claude/plugins/adx-toolkit/settings.json /your-project/.claude/settings.json
```

### Reconfigure Existing Project

```bash
~/.claude/plugins/adx-toolkit/setup.sh
```

---

## Usage Examples

### Ship a feature (fully autonomous)

```bash
/ship add user profile page with avatar upload
```

### Ship with browser verification (recommended for UI)

```bash
/ship add dashboard with charts --browser
```

### Plan first, then implement (controlled)

```bash
/plan add shopping cart functionality
# Review the plan at .claude/plans/plan-shopping-cart.md
# Make adjustments if needed

/implement .claude/plans/plan-shopping-cart.md
/refactor
/verify
/review --browser  # With visual verification
/commit
/pr
```

### Quick refactor

```bash
/refactor src/features/users/
```

### Code review only

```bash
/review
# Check report at .claude/reviews/review-{date}.md
```

### Browser verification only

```bash
/review --browser-only
# Claude uses Chrome extension to view UI, verifies it, fixes issues if found
```

### RALPH: Fire and forget (overnight development)

```bash
# Initialize RALPH project
./scripts/ralph-init.sh "add user authentication with JWT" --browser

# Start autonomous loop (go to sleep)
cd .ralph-projects/add-user-authentication
ralph --monitor --timeout 120

# Wake up to completed PR
```

### RALPH: Using the command

```bash
# Start RALPH with monitoring dashboard
/ralph "implement payment integration" --browser --monitor

# RALPH will loop until PR is created or circuit breaker trips
```

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
    "UserPromptSubmit": ["python hooks/smart_context_loader.py"],
    "Stop": ["python hooks/stop.py"]
  }
}
```

---

## License

MIT

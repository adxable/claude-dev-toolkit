# ADX Toolkit

Autonomous frontend development workflow for Claude Code. Plan → Implement → Verify → Ship.

## How It Works

```
/adx:ship "add user authentication"
```

Runs a 6-phase pipeline automatically:

```
PLAN → IMPLEMENT → VERIFY → REVIEW → COMMIT → PR

Alternative (browser-first):
INVESTIGATE → IMPLEMENT → VERIFY → REVIEW → COMMIT → PR
```

Each phase has checkpoints. If something fails, resume with `--continue`.

---

## Install

**One-liner:**
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install-adx.sh)
```

**Project setup** (optional - adds hooks, memory, conventions):
```bash
git clone https://github.com/adxable/adx-toolkit.git /tmp/adx-toolkit
/tmp/adx-toolkit/setup.sh
```

**Update:**
```bash
claude plugin update adx
```

---

## Commands

### Autonomous Workflow

| Command | Description |
|---------|-------------|
| `/adx:ship "task"` | Full pipeline, stops on error |
| `/adx:ship "task" --browser` | With visual verification |

### Individual Steps

| Command | Description |
|---------|-------------|
| `/adx:investigate "/url issue"` | Browser investigation + planning |
| `/adx:plan "task"` | Create implementation plan |
| `/adx:implement` | Execute the plan |
| `/adx:verify` | Type check, lint, build, test |
| `/adx:review` | Code review + security scan |
| `/adx:commit` | Create git commit |
| `/adx:pr` | Create pull request |

### Optional Commands (`.claude/dev/`)

| Command | Description |
|---------|-------------|
| `/refactor` | Clean up code (requires `.claude/dev/`) |

### When to Use What

| Scenario | Command |
|----------|---------|
| Know what to build, need a plan | `/adx:plan "add user auth"` |
| See a bug, need to investigate first | `/adx:investigate /dashboard "chart not loading"` |
| Validate implementation works | `/adx:verify /dashboard` |

### State Tracking

| Command | Description |
|---------|-------------|
| `/adx:init-state` | Set up project tracking |
| `/adx:progress` | Where am I? What's next? |
| `/adx:pause` | Save session for later |
| `/adx:resume` | Continue from last session |

### Utilities

| Command | Description |
|---------|-------------|
| `/adx:costs` | View usage metrics |
| `/adx:memory` | Manage semantic knowledge store |
| `/adx:discover` | Research new patterns |

---

## Recovery

```bash
/adx:ship --continue      # Resume from last checkpoint
/adx:ship --from verify   # Start from specific phase
/adx:ship --rollback impl # Revert to checkpoint
/adx:ship --status        # View checkpoint status
```

---

## Agents

### Core Agents (Used by /ship)

| Agent | Purpose | When Used |
|-------|---------|-----------|
| `explorer` | Fast codebase search | /plan, /implement |
| `verifier` | Type check, lint, build, test | /verify |
| `code-reviewer` | Code review with reports | /review |
| `security-auditor` | Scan for vulnerabilities | /review |
| `performance-auditor` | Bundle and runtime analysis | /review |
| `browser-tester` | Visual UI testing | /verify --browser, /review --browser |
| `git-automator` | Commits and PRs | /commit, /pr |
| `web-researcher` | Debug with internet research | /implement (when stuck) |

### Standalone Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `planner` | Create detailed implementation plans | Complex features needing research |
| `implementer` | Execute plans step-by-step | After planner creates a plan |
| `refactorer` | Code cleanup, remove `any` types | Technical debt cleanup |
| `pattern-researcher` | Research new patterns online | /discover command |

### Optional Agents

| Agent | Purpose | Install |
|-------|---------|---------|
| `accessibility-tester` | WCAG compliance | `agents/optional/` |
| `docs-generator` | Generate README, JSDoc | `agents/optional/` |

---

## Browser Verification

Requires [Claude Chrome extension](https://chromewebstore.google.com/detail/claude-for-chrome/). Claude sees your app and fixes issues in a loop.

```bash
/adx:review --browser       # Code review + visual testing
/adx:ship "task" --browser  # Full workflow with browser
```

---

## Project Structure

```
.claude/
├── plans/          # Implementation plans
├── reviews/        # Code review reports
├── state/          # Progress tracking (optional)
├── context/        # Session persistence
├── checkpoints/    # Ship recovery points
└── settings.json   # Hooks and permissions

hooks/
├── *.py            # Hook scripts (UserPromptSubmit, Stop, etc.)
└── utils/          # Shared utilities
    ├── knowledge_store.py     # Fragment storage + TF-IDF index
    └── knowledge_retriever.py # Context-aware retrieval

memory/
├── decisions.md    # Architectural decisions (ADRs)
├── lessons.md      # Problems solved, patterns learned
├── conventions.md  # Code patterns and standards
├── knowledge/      # Semantic knowledge store (shared)
│   ├── index.json  # TF-IDF search index
│   └── fragments/  # Knowledge fragment files
└── local/          # Personal knowledge (gitignored)
    └── fragments/  # Session-specific context
```

---

## Setup & Configuration

### Prerequisites

ADX Toolkit hooks are written in Python and use `uv` for fast dependency management.

**macOS:**
```bash
# Install Python 3.11+
brew install python@3.12

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Linux:**
```bash
# Install Python 3.11+
sudo apt install python3.12 python3.12-venv  # Debian/Ubuntu
# or
sudo dnf install python3.12                   # Fedora

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (WSL recommended):**
```bash
# In WSL, follow Linux instructions above
# Or use winget:
winget install astral-sh.uv
```

**Verify installation:**
```bash
python3 --version  # Should be 3.11+
uv --version       # Should be 0.4+
```

### Setup Script

Run `setup.sh` to configure:

| Feature | Description |
|---------|-------------|
| Hooks | Context detection, knowledge retrieval, state persistence |
| Memory | Semantic knowledge store with TF-IDF search |
| State | Phase-based progress tracking |
| MCP | Context7 for library documentation |

### MCP Servers

ADX Toolkit uses minimal MCP configuration. Most functionality uses Claude Code's built-in tools.

**Available MCP (in `mcp.json`):**

| Server | Purpose | Enabled by Default |
|--------|---------|-------------------|
| `context7` | Up-to-date library documentation | ✅ Yes |
| `sequential-thinking` | Enhanced reasoning for complex problems | ✅ Yes |

**External MCP (user-installed):**

| Server | Purpose | Used By |
|--------|---------|---------|
| `claude-in-chrome` | Browser automation and visual testing | browser-tester, verify, investigate |

> **Note:** Browser testing uses `claude-in-chrome` (Chrome extension), not Playwright MCP.

### Configuration Files

| File | Purpose |
|------|---------|
| `mcp.json` | MCP server definitions (copy to `.claude/mcp.json`) |
| `settings.json` | Hooks, permissions, enabled MCP servers |

### Enabling MCP Servers

In `settings.json`:
```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["context7", "sequential-thinking"]
}
```

Only servers listed in `enabledMcpjsonServers` are loaded at startup. MCP servers cannot be loaded dynamically during a session.

### Browser Testing Setup

For visual UI testing with `/adx:verify --browser` or `/adx:review --browser`:

1. Install [Claude Chrome extension](https://chromewebstore.google.com/detail/claude-for-chrome/)
2. The extension provides `claude-in-chrome` MCP tools globally
3. No additional configuration needed in `mcp.json`

---

## Memory System

Semantic knowledge store with automatic learning and retrieval.

### How It Works

1. **Auto-retrieve** - On each prompt, relevant knowledge fragments are injected as context
2. **Auto-learn** - At session end, decisions/patterns/fixes are extracted and stored
3. **Manual add** - Use `/adx:memory` to add decisions and lessons

### Commands

```bash
/adx:memory decision "Use queryOptions factory for TanStack Query"
/adx:memory lesson "Zustand without useShallow causes infinite loops"
/adx:memory search "authentication patterns"
/adx:memory show                    # View all memory + stats
/adx:memory promote <id>            # Move personal → shared
```

### Storage Tiers

| Tier | Files | Loaded |
|------|-------|--------|
| L1 (always) | `decisions.md`, `lessons.md`, `conventions.md` | Every prompt |
| L2 (semantic) | `knowledge/fragments/*.json` | Top 5 by relevance |
| L3 (personal) | `local/fragments/*.json` | Session context |

### Fragment Format

```json
{
  "id": "abc123",
  "content": "Use JWT with short-lived tokens for API auth",
  "tags": ["authentication", "api", "security"],
  "source": "session:xyz",
  "scope": "shared"
}
```

---

## Context & Session Continuity

Claude Code has a limited context window. When conversations get long, earlier context gets compacted. When you start a new session, Claude doesn't remember the previous one. The context system persists important information to files that get re-injected into every prompt.

### State Tracking (Solo Development)

For multi-day projects, use state tracking to maintain continuity:

```bash
# Day 1: Start project
/adx:init-state "Building a recipe app with Next.js and Supabase"
# Creates PROJECT.md, STATE.md, ROADMAP.md with your phases

# Work on features...

# End of day - save your position
/adx:pause
# Saves: "Phase 1, implementing auth, OAuth done, email auth incomplete"

# Day 2 - restore context
/adx:resume
# Shows where you left off, blockers, decisions made
```

**State files** (`.claude/state/`):
| File | Purpose |
|------|---------|
| `PROJECT.md` | Project vision and tech stack |
| `STATE.md` | Current position, decisions, blockers |
| `ROADMAP.md` | Phases and progress |

### Team Use

**What to share (commit to git):**
```
memory/
├── decisions.md    # Team ADRs - "We chose X because Y"
├── lessons.md      # Shared learnings - "X failed because Y"
├── conventions.md  # Coding standards
└── knowledge/      # Shared knowledge fragments
```

**What stays personal (gitignored):**
```
.claude/state/      # Your position tracking
.claude/context/    # Your session context
memory/local/       # Your personal knowledge
```

### Recommended .gitignore

```gitignore
# Personal (don't share)
.claude/context/
.claude/state/
.claude/ship/
memory/local/

# Shared (commit these)
# memory/decisions.md
# memory/lessons.md
# memory/conventions.md
# memory/knowledge/
```

### When to Use What

| Scenario | State Tracking | Knowledge Store |
|----------|---------------|-----------------|
| Solo dev, multi-day project | Yes | Yes |
| Team, shared codebase | No (personal only) | Yes (shared `memory/`) |
| Quick one-off task | No | No |
| Complex feature, multiple sessions | Yes | Yes |

---

## Tech Stack Conventions

The `CLAUDE.md` template enforces:

- **Router:** TanStack Router / React Router v7
- **State:** Zustand with `useShallow`
- **Server State:** TanStack Query with `useSuspenseQuery`
- **Forms:** React Hook Form + Zod
- **Styling:** Tailwind + shadcn/ui

---

## Skills

Auto-loaded contextual guidelines for React/TypeScript development.

| Skill | Description |
|-------|-------------|
| `react-best-practices` | 57 Vercel performance rules (waterfalls, bundle size, SSR, re-renders) |
| `composition-patterns` | Component architecture: compound components, boolean prop avoidance |
| `code-quality-rules` | Design principles linters can't catch (SOLID, abstraction quality) |
| `project-structure` | Module boundaries, framework detection, folder organization |
| `browser-testing` | Visual testing patterns for Claude Chrome extension |
| `performance-profiling` | Runtime profiling with Chrome DevTools and React DevTools |

### Rule Priorities (react-best-practices)

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Eliminating Waterfalls | CRITICAL |
| 2 | Bundle Size Optimization | CRITICAL |
| 3 | Server-Side Performance | HIGH |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH |
| 5 | Re-render Optimization | MEDIUM |

---

## License

MIT

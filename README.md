# ADX Toolkit

Autonomous frontend development workflow for Claude Code. Plan → Implement → Verify → Ship.

## How It Works

```
/adx:ship "add user authentication"
```

Runs a 7-phase pipeline automatically:

```
PLAN → IMPLEMENT → REFACTOR → VERIFY → REVIEW → COMMIT → PR

Alternative (browser-first):
INVESTIGATE → IMPLEMENT → REFACTOR → VERIFY → REVIEW → COMMIT → PR
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
| `/adx:refactor` | Clean up code |
| `/adx:verify` | Type check, lint, build, test |
| `/adx:review` | Code review + security scan |
| `/adx:commit` | Create git commit |
| `/adx:pr` | Create pull request |

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
| `/adx:memory` | Manage decisions/lessons |
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

| Agent | Purpose |
|-------|---------|
| `explorer` | Fast codebase search |
| `web-researcher` | Debug with internet research |
| `code-reviewer` | Code review with reports |
| `security-auditor` | Scan for vulnerabilities |
| `refactorer` | Code cleanup |
| `verifier` | Type check, lint, build, test |
| `git-automator` | Commits and PRs |
| `browser-tester` | Visual UI testing |
| `performance-auditor` | Bundle and runtime analysis |

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
├── memory/         # Decisions and lessons
├── context/        # Session persistence
├── checkpoints/    # Ship recovery points
└── settings.json   # Hooks and permissions
```

---

## Setup Options

Run `setup.sh` to configure:

| Feature | Description |
|---------|-------------|
| Hooks | Context detection, session summaries |
| Memory | Persistent decisions and lessons |
| State | Phase-based progress tracking |
| MCP | Sequential thinking, Playwright |

---

## Tech Stack Conventions

The `CLAUDE.md` template enforces:

- **Router:** TanStack Router / React Router v7
- **State:** Zustand with `useShallow`
- **Server State:** TanStack Query with `useSuspenseQuery`
- **Forms:** React Hook Form + Zod
- **Styling:** Tailwind + shadcn/ui

---

## License

MIT

# Ralph

Start autonomous development loop using RALPH (Recursive Autonomous Loop for Project Handling).

## Arguments

- `$ARGUMENTS` - Feature description or path to existing PROMPT.md

## Flags

- `--browser` - Enable browser verification in /ship steps
- `--timeout <mins>` - Max execution time (default: 60, max: 120)
- `--monitor` - Open tmux monitoring dashboard

## Prerequisites

RALPH must be installed system-wide:

```bash
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code
./install.sh
```

## Instructions

### 1. Check RALPH Installation

```bash
which ralph || echo "RALPH not installed - see prerequisites"
```

### 2. Initialize or Resume

**If feature description provided:**
Create new RALPH project with adx-toolkit workflow.

**If PROMPT.md path provided:**
Resume existing RALPH project.

### 3. Project Setup (New Projects)

Create RALPH project structure:

```bash
mkdir -p .ralph-projects/{project-name}
cd .ralph-projects/{project-name}
```

Generate `PROMPT.md` with adx-toolkit integration:

```markdown
# {Feature Description}

## Overview
{User's feature description}

## Workflow
Use the adx-toolkit /ship command for implementation:

1. Run `/ship "{feature}" --browser` to execute full pipeline
2. If any step fails, analyze the error and fix it
3. Repeat until PR is created successfully

## Commands Available
- `/plan` - Research and create implementation plan
- `/implement` - Execute plan step by step
- `/refactor` - Clean up code, remove technical debt
- `/verify` - Type check + lint + build loop
- `/review --browser` - Code review + visual verification
- `/commit` - Create git commit
- `/pr` - Create pull request

## Success Criteria
- [ ] Feature implemented and working
- [ ] All types correct (no `any`)
- [ ] Tests passing (if applicable)
- [ ] Browser verification passing (if --browser)
- [ ] PR created with description

## EXIT_SIGNAL Conditions
Set EXIT_SIGNAL: true ONLY when:
- PR has been successfully created
- All success criteria met
- No blocking errors remain

## Current Status
Starting fresh - no work completed yet.
```

Generate `@fix_plan.md`:

```markdown
# Development Plan

## Priority 1 - Core Implementation
- [ ] Research codebase for similar patterns
- [ ] Create implementation plan
- [ ] Implement core feature
- [ ] Add error handling

## Priority 2 - Quality
- [ ] Run type check and fix errors
- [ ] Run linter and fix issues
- [ ] Refactor if needed

## Priority 3 - Verification
- [ ] Build successfully
- [ ] Browser verification (if enabled)
- [ ] Code review passing

## Priority 4 - Ship
- [ ] Create commit
- [ ] Create PR

## Completed
(Items move here when done)
```

### 4. Start RALPH Loop

```bash
cd .ralph-projects/{project-name}
ralph --monitor --timeout {timeout}
```

### 5. Monitor Progress

RALPH will:
1. Read PROMPT.md instructions
2. Execute /ship or individual commands
3. Track progress in @fix_plan.md
4. Handle failures and retry
5. Exit when PR created (EXIT_SIGNAL: true)

```
┌─────────────────────────────────────────────────────────────┐
│                      RALPH + /ship                           │
│                                                             │
│   RALPH Loop:                                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Read PROMPT.md                                     │   │
│   │       ↓                                             │   │
│   │  Execute: /ship "feature" --browser                 │   │
│   │       ↓                                             │   │
│   │  /ship Pipeline:                                    │   │
│   │    plan → implement → refactor → verify → review    │   │
│   │       ↓                                             │   │
│   │  Success? → commit → pr → EXIT_SIGNAL: true         │   │
│   │       ↓                                             │   │
│   │  Failure? → Analyze → Fix → Loop again              │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   Safeguards:                                               │
│   • Circuit breaker (3 loops no progress)                   │
│   • Rate limiting (100 calls/hour)                          │
│   • Timeout (configurable)                                  │
│   • 5-hour API limit handling                               │
└─────────────────────────────────────────────────────────────┘
```

## Output

On completion, display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RALPH Session Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {description}
Mode: Autonomous (RALPH)

Stats:
  Loops:      {N}
  Duration:   {time}
  API Calls:  {N}

Result:
  Status: {SUCCESS | CIRCUIT_BREAKER | TIMEOUT | RATE_LIMITED}
  PR:     {url or N/A}

Artifacts:
  RALPH Project: .ralph-projects/{name}/
  Plan:          .claude/plans/plan-{name}.md
  Review:        .claude/reviews/review-{date}.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Usage Examples

```bash
# Start autonomous development of a feature
/ralph "add user authentication with JWT"

# With browser verification
/ralph "add dashboard with charts" --browser

# Extended timeout for complex features
/ralph "implement shopping cart" --timeout 120 --browser

# With monitoring dashboard
/ralph "add search functionality" --monitor
```

## Comparison: /ship vs /ralph

| Aspect | /ship | /ralph |
|--------|-------|--------|
| Execution | Single pass | Loop until done |
| Failure handling | Stop and report | Retry automatically |
| Human involvement | Review output | Fire and forget |
| Duration | Minutes | Minutes to hours |
| Best for | Known scope | Exploratory/complex |
| API usage | Predictable | Variable (with limits) |

## When to Use /ralph

- **Overnight development** - Start before bed, wake up to PR
- **Complex features** - Multiple unknowns, likely failures
- **Hands-off mode** - Don't want to monitor progress
- **Learning projects** - Let Claude explore and iterate

## When to Use /ship

- **Quick features** - Clear scope, likely to succeed first try
- **Supervised work** - Want to review at each step
- **Cost control** - Predictable API usage
- **Time-sensitive** - Need result in specific timeframe

## Workflow Position

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT MODES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SUPERVISED (you're watching):                              │
│  /plan → /implement → /refactor → /verify → /review →       │
│  /commit → /pr                                              │
│                                                             │
│  SEMI-AUTONOMOUS (single pass):                             │
│  /ship "feature" --browser                                  │
│                                                             │
│  FULLY AUTONOMOUS (loop until done):                        │
│  /ralph "feature" --browser --monitor                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

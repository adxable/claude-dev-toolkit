# Ship

Fully autonomous workflow: plan → implement → refactor → verify → review → commit → pr.

## Arguments

- `$ARGUMENTS` - Description of what to build/fix

## Flags

- `--browser` - Enable browser verification during review step (fix-verify loop)

## Instructions

Execute the complete development workflow automatically.

### Step 1: Plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1/7: PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use `explorer` agent to research codebase, then create plan:
- Find similar implementations
- Identify relevant files
- Create `.claude/plans/plan-{name}.md`

### Step 2: Implement

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 2/7: IMPLEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Execute the plan step by step:
- Create/modify files as specified
- Use `web-researcher` agent if stuck
- Quick type check after changes

### Step 3: Refactor

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 3/7: REFACTOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use `refactorer` agent on changed files:
- Remove `any` types
- Clean dead code
- Simplify over-abstractions

### Step 4: Verify

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 4/7: VERIFY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Run verification loop:
```bash
npx tsc --noEmit    # Type check
npx eslint src/     # Lint
npm run build       # Build
```

Fix issues and repeat until all pass.

### Step 5: Review (Parallel Agents + Browser)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 5/7: REVIEW (3 agents in parallel + browser)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Phase 1: Code Review (Parallel)**

Run 3 agents **simultaneously**:

```
┌────────────────────┬────────────────────┬────────────────────┐
│   code-reviewer    │ performance-auditor│ accessibility-tester│
├────────────────────┼────────────────────┼────────────────────┤
│ • Types            │ • Re-renders       │ • WCAG compliance  │
│ • Patterns         │ • Memoization      │ • Keyboard nav     │
│ • Error handling   │ • Bundle size      │ • ARIA attributes  │
│ • Conventions      │ • useShallow       │ • Color contrast   │
└────────────────────┴────────────────────┴────────────────────┘
                              │
                              ▼
                    Code Review Report
```

**Phase 2: Browser Verification (if --browser flag)**

```
┌─────────────────────────────────────────────────────────────┐
│                    browser-tester                           │
├─────────────────────────────────────────────────────────────┤
│  ┌──────┐   ┌───────┐   ┌─────┐   ┌──────┐                 │
│  │Screen│ → │Analyze│ → │ Fix │ → │Verify│ ──► (loop)      │
│  │ shot │   │       │   │     │   │      │                 │
│  └──────┘   └───────┘   └─────┘   └──────┘                 │
│                                                             │
│  • Visual verification    • Interaction testing             │
│  • Responsive design      • Fix-verify loop (max 5)         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Combined Report
                    .claude/reviews/review-{date}.md
```

**If critical issues found:** Go back to Step 3 (Refactor) to fix.

### Step 6: Commit

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 6/7: COMMIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use `git-automator` agent:
- Stage all changes
- Generate commit message
- Create commit with Co-Authored-By

### Step 7: PR

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 7/7: PR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use `git-automator` agent:
- Push to remote
- Generate PR description
- Create PR with `gh pr create`

### Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ SHIPPED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {description}

Artifacts:
  Plan:   .claude/plans/plan-{name}.md
  Review: .claude/reviews/review-{date}.md

Stats:
  Files created:  {N}
  Files modified: {N}

Browser verification: {enabled/disabled}
  Issues fixed: {N}
  Iterations:   {N}

Git:
  Commit: {hash} {message}
  PR:     #{number} {url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Pipeline Diagram

```
/ship "add user authentication" --browser
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 1: PLAN                                    │
│   └─► explorer agent                            │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 2: IMPLEMENT                               │
│   └─► web-researcher agent (if stuck)           │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 3: REFACTOR                                │
│   └─► refactorer agent                          │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 4: VERIFY                                  │
│   └─► tsc + eslint + build (loop until pass)    │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 5: REVIEW                                  │
│                                                 │
│   Phase 1: Code Review (parallel)               │
│   ├─► code-reviewer agent      ─┐               │
│   ├─► performance-auditor agent ├─► Report      │
│   └─► accessibility-tester agent┘               │
│                                                 │
│   Phase 2: Browser Verification (if --browser)  │
│   └─► browser-tester agent                      │
│       └─► Screenshot → Analyze → Fix → Verify   │
│           └─► (loop until pass, max 5)          │
│                                                 │
│   Critical issues? ──► Loop back to Step 3      │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 6: COMMIT                                  │
│   └─► git-automator agent                       │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 7: PR                                      │
│   └─► git-automator agent                       │
└─────────────────────────────────────────────────┘
    │
    ▼
  ✓ SHIPPED
```

## Agents Used

| Step | Agent(s) | Parallel | Notes |
|------|----------|----------|-------|
| Plan | `explorer` | - | |
| Implement | `web-researcher` (if stuck) | - | |
| Refactor | `refactorer` | - | |
| Verify | - | - | |
| Review | `code-reviewer`, `performance-auditor`, `accessibility-tester` | ✓ Yes | Phase 1 |
| Review | `browser-tester` | - | Phase 2 (if --browser) |
| Commit | `git-automator` | - | |
| PR | `git-automator` | - | |

**Total: 7 agents (6 core + browser-tester), 3 running in parallel during review**

## Error Handling

| Error | Action |
|-------|--------|
| Verification fails 5+ times | Stop, ask user |
| Critical review issues | Loop back to refactor |
| Browser issues after 5 iterations | Report unresolved, continue |
| Git push fails | Stop, ask user |
| PR creation fails | Show manual command |

## Usage Examples

```bash
# Standard shipping (code review only)
/ship add user authentication with JWT

# With browser verification
/ship add user authentication with JWT --browser

# UI feature (browser recommended)
/ship create dashboard component --browser
```

## Example with Browser

```
User: /ship add login form --browser

Claude:
  Step 1/7: PLAN
  → Researching codebase...
  → Plan created: .claude/plans/plan-login-form.md

  Step 2/7: IMPLEMENT
  → Creating src/features/auth/LoginForm.tsx...
  → ✓ 3 files created

  Step 3/7: REFACTOR
  → Cleaning up code...
  → ✓ Removed 1 any type

  Step 4/7: VERIFY
  → Type check: ✓
  → Lint: ✓
  → Build: ✓

  Step 5/7: REVIEW
  Phase 1: Code Review (3 agents in parallel)
  → code-reviewer: ✓
  → performance-auditor: ✓
  → accessibility-tester: ✓

  Phase 2: Browser Verification (Chrome extension)
  → Opening Chrome, navigating to localhost:5173
  → Viewing: Login form page
  → Issue found: Submit button not aligned
  → Fixing: LoginForm.tsx:45
  → Waiting for hot reload...
  → Viewing again... ✓ Fixed
  → All visual tests passing

  → Report: .claude/reviews/review-2024-01-16.md

  Step 6/7: COMMIT
  → feat: add login form with validation

  Step 7/7: PR
  → PR #42: https://github.com/user/repo/pull/42

  ✓ SHIPPED (browser verified)
```

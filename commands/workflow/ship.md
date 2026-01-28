# Ship

Fully autonomous workflow: plan → implement → verify → review → commit → pr.

**CRITICAL: ALL 6 STEPS ARE MANDATORY. NEVER SKIP ANY STEP.**

## Arguments

- `$ARGUMENTS` - Description of what to build/fix

## Flags

- `--skip-browser` - Skip browser verification (NOT recommended for UI changes)
- `--skip-tests` - Skip test execution in verify step
- `--continue` - Resume from last checkpoint
- `--from <phase>` - Start from specific phase
- `--status` - Show checkpoint status

## State Tracking Commands

**IMPORTANT: Use these commands to track progress. State survives context compaction.**

```bash
# Start ship (REQUIRED at beginning)
uv run hooks/ship_state.py start "feature description"

# Mark phase as complete (REQUIRED after each phase)
uv run hooks/ship_state.py phase_done <phase>

# Check current status
uv run hooks/ship_state.py status

# Mark ship as fully complete
uv run hooks/ship_state.py complete

# Abort if needed
uv run hooks/ship_state.py abort
```

## MANDATORY EXECUTION RULES

**YOU MUST FOLLOW THESE RULES:**

1. **ALWAYS start with ship_state** - Run `ship_state.py start` before anything else
2. **NEVER skip any step** - All 6 steps must execute in order
3. **ALWAYS mark phases done** - Run `ship_state.py phase_done <phase>` after each phase
4. **ALWAYS output step banner** - Print the step number/name before starting each step
5. **ALWAYS run browser verification** - Unless `--skip-browser` is explicitly passed
6. **STOP on critical failures** - Don't continue if a step fails critically

## Instructions

### Pre-flight Check

Before starting, initialize state tracking:
```bash
# Check git status
git status

# Ensure clean working directory or stash
git stash --include-untracked || true

# CRITICAL: Initialize ship state tracking
uv run hooks/ship_state.py start "$ARGUMENTS"
```

The ship_state command will output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 SHIP STARTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID: {timestamp}
Feature: {description}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Starting with Phase 1: PLAN
```

---

### Step 1: PLAN (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1/6: PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions:**
1. Use `explorer` agent to research codebase
2. Find similar implementations
3. Identify ALL relevant files that need changes
4. Create detailed plan at `.claude/plans/plan-{name}.md`

**Plan MUST include:**
- Files to create/modify (with paths)
- Step-by-step implementation
- Testing requirements
- UI elements to verify in browser

**Completion check:**
- [ ] Plan file created
- [ ] All files identified
- [ ] Implementation steps defined

**CHECKPOINT: Mark phase complete**
```bash
uv run hooks/ship_state.py phase_done plan
```

---

### Step 2: IMPLEMENT (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 2/6: IMPLEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions:**
1. Execute plan step by step
2. Create/modify files as specified
3. Use `web-researcher` agent if stuck on implementation details
4. Quick type check after major changes

**For each file:**
```
[implement] Creating: {file_path}
[implement] Modifying: {file_path}
```

**Completion check:**
- [ ] All planned files created/modified
- [ ] No TODO comments left
- [ ] Basic functionality in place

**CHECKPOINT: Mark phase complete**
```bash
uv run hooks/ship_state.py phase_done implement
```

---

### Step 3: VERIFY (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 3/6: VERIFY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions (ALL REQUIRED):**

1. **Type check:**
```bash
npx tsc --noEmit
```

2. **Lint:**
```bash
npm run lint || npx eslint src/
```

3. **Build:**
```bash
npm run build
```

4. **Tests (if detected):**
```bash
# Check if tests exist
grep -E '"test":|"vitest"|"jest"' package.json

# Run tests if found
npm test
```

**Fix-loop:**
- If any check fails, fix the issue
- Re-run the failing check
- Maximum 5 iterations per check type
- After 5 failures, STOP and report

**Output for each check:**
```
[verify] Type check: ✓ Pass / ✗ N errors
[verify] Lint:       ✓ Pass / ✗ N errors
[verify] Build:      ✓ Pass / ✗ Failed
[verify] Tests:      ✓ Pass (N/N) / ✗ N failed / ○ Skipped
```

**Completion check:**
- [ ] Type check passes
- [ ] Lint passes
- [ ] Build succeeds
- [ ] Tests pass (if present)

**CHECKPOINT: Mark phase complete**
```bash
uv run hooks/ship_state.py phase_done verify
```

---

### Step 4: REVIEW (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 4/6: REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Phase 1: Code Review (MANDATORY - Parallel Agents)**

Run ALL 4 agents **simultaneously**:

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│  code-reviewer   │ security-auditor │ performance-     │ accessibility-   │
│                  │                  │ auditor          │ tester           │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ • Types          │ • Hardcoded      │ • Re-renders     │ • WCAG           │
│ • Patterns       │   secrets        │ • Memoization    │ • Keyboard nav   │
│ • Error handling │ • XSS/injection  │ • Bundle size    │ • ARIA           │
│ • Conventions    │ • Dependencies   │ • useShallow     │ • Contrast       │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

**Phase 2: Browser Verification (DEFAULT ENABLED)**

**ALWAYS RUN unless `--skip-browser` is explicitly passed.**

```
┌─────────────────────────────────────────────────────────────┐
│                    browser-tester agent                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FOR EACH UI ELEMENT/FEATURE IMPLEMENTED:                   │
│                                                             │
│  1. Navigate to relevant page                               │
│  2. Take screenshot                                         │
│  3. Verify element renders correctly                        │
│  4. Test interactions (click, type, submit)                 │
│  5. Check responsive (if applicable)                        │
│  6. If issue found:                                         │
│     → Fix the code                                          │
│     → Wait for hot reload                                   │
│     → Re-verify                                             │
│     → Repeat until fixed (max 5 iterations)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Browser verification checklist (MUST verify ALL):**
- [ ] Page loads without errors
- [ ] All new components render correctly
- [ ] Interactions work (buttons, forms, links)
- [ ] No console errors
- [ ] No visual glitches
- [ ] Loading states display correctly
- [ ] Error states handled
- [ ] Empty states handled (if applicable)

**Critical issues handling:**
- If CRITICAL issues found in code review → Fix and re-verify
- If browser issues persist after 5 iterations → Stop and report

**Generate report:**
Save to `.claude/reviews/review-{date}.md`

**CHECKPOINT: Mark phase complete**
```bash
uv run hooks/ship_state.py phase_done review
```

---

### Step 5: COMMIT (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 5/6: COMMIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions:**
1. Use `git-automator` agent
2. Stage all changes: `git add .`
3. Generate descriptive commit message
4. Include Co-Authored-By trailer

**Commit message format:**
```
{type}: {short description}

{detailed description}

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Output:**
```
[commit] Staged: N files
[commit] Message: {type}: {description}
[commit] ✓ Committed: {hash}
```

**CHECKPOINT: Mark phase complete**
```bash
uv run hooks/ship_state.py phase_done commit
```

---

### Step 6: PR (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 6/6: PR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions:**
1. Use `git-automator` agent
2. Push to remote: `git push -u origin HEAD`
3. Generate PR description with:
   - Summary of changes
   - Files modified
   - Test plan
   - Browser verification status
4. Create PR: `gh pr create`

**Output:**
```
[pr] Pushed to: origin/{branch}
[pr] Creating PR...
[pr] ✓ PR created: #{number} {url}
```

**CHECKPOINT: Mark phase and ship complete**
```bash
uv run hooks/ship_state.py phase_done pr
uv run hooks/ship_state.py complete
```

---

### Summary (MANDATORY OUTPUT)

**YOU MUST OUTPUT THIS SUMMARY. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ SHIPPED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {description}

Steps Completed:
  ✓ 1. Plan     - .claude/plans/plan-{name}.md
  ✓ 2. Implement - {N} files created, {N} modified
  ✓ 3. Verify    - Types ✓ Lint ✓ Build ✓ Tests ✓
  ✓ 4. Review    - Code ✓ Security ✓ Browser ✓
  ✓ 5. Commit    - {hash}
  ✓ 6. PR        - #{number}

Artifacts:
  Plan:   .claude/plans/plan-{name}.md
  Review: .claude/reviews/review-{date}.md

Browser Verification:
  Status: {verified/skipped}
  Pages tested: {list}
  Issues fixed: {N}
  Iterations: {N}

Git:
  Commit: {hash} {message}
  PR:     #{number} {url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## State Tracking System

State is persisted in `.claude/ship/current.json` and survives:
- Context compaction
- Session restarts
- Interruptions

```
/ship "add feature"
    │
    ├─ ship_state.py start "add feature"
    │
    ├─ Phase 1: PLAN
    │   └─ ship_state.py phase_done plan
    │
    ├─ Phase 2: IMPLEMENT
    │   └─ ship_state.py phase_done implement
    │
    ├─ Phase 3: VERIFY
    │   └─ ship_state.py phase_done verify
    │
    ├─ Phase 4: REVIEW
    │   └─ ship_state.py phase_done review
    │
    ├─ Phase 5: COMMIT
    │   └─ ship_state.py phase_done commit
    │
    ├─ Phase 6: PR
    │   └─ ship_state.py phase_done pr
    │
    └─ ship_state.py complete

```

### Recovery

```bash
# Check current status
uv run hooks/ship_state.py status

# Resume: The ship_loader hook automatically injects state.
# Just run /ship --continue and follow the <ship-state> context.
/ship --continue
```

### On Failure

When a phase fails, the state file preserves your progress:

```
┌─────────────────────────────────────────────────────────────┐
│  ❌ SHIP FAILED at {phase}                                   │
├─────────────────────────────────────────────────────────────┤
│  State preserved in: .claude/ship/current.json             │
│                                                             │
│  Progress:                                                  │
│  ✓ plan      (done)                                        │
│  ✓ implement (done)                                        │
│  → verify    (in_progress)                                 │
│                                                             │
│  Options:                                                   │
│  • /ship --continue     Resume from current phase          │
│  • Fix issues manually, then continue                       │
│  • ship_state.py abort  Cancel and start fresh             │
└─────────────────────────────────────────────────────────────┘
```

---

## Agents Used (ALL MANDATORY)

| Step | Agent(s) | Parallel | MANDATORY |
|------|----------|----------|-----------|
| Plan | `explorer` | - | ✓ YES |
| Implement | `web-researcher` (if stuck) | - | ✓ YES |
| Verify | `verifier` | - | ✓ YES |
| Review | `code-reviewer`, `security-auditor`, `performance-auditor`, `accessibility-tester` | ✓ Yes | ✓ YES |
| Review | `browser-tester` | - | ✓ YES (default) |
| Commit | `git-automator` | - | ✓ YES |
| PR | `git-automator` | - | ✓ YES |

**Total: 8 agents, 4 running in parallel during review**

---

## Error Handling

| Error | Action |
|-------|--------|
| Verification fails 5+ times | STOP, save checkpoint, ask user |
| Critical review issues | Fix and re-verify |
| Security CRITICAL found | STOP immediately, report |
| Browser issues after 5 iterations | STOP, save checkpoint, report |
| Git push fails | STOP, save checkpoint, ask user |
| PR creation fails | Show manual command |

---

## Usage Examples

```bash
# Standard shipping (with browser verification - DEFAULT)
/ship add user authentication with JWT

# Explicitly skip browser (NOT recommended for UI)
/ship add utility function --skip-browser

# Resume failed ship
/ship --continue

# Retry from specific step
/ship --from verify
```

---

## FINAL REMINDER

**BEFORE COMPLETING /ship, VERIFY:**

1. ✓ Did I execute Step 1 (Plan)?
2. ✓ Did I execute Step 2 (Implement)?
3. ✓ Did I execute Step 3 (Verify)?
4. ✓ Did I execute Step 4 (Review)?
5. ✓ Did I verify in browser (unless --skip-browser)?
6. ✓ Did I execute Step 5 (Commit)?
7. ✓ Did I execute Step 6 (PR)?
8. ✓ Did I output the summary?

**IF ANY ANSWER IS "NO", GO BACK AND COMPLETE THAT STEP.**
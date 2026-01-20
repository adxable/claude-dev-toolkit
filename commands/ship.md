# Ship

Fully autonomous workflow: plan → implement → refactor → verify → review → commit → pr.

**CRITICAL: ALL 7 STEPS ARE MANDATORY. NEVER SKIP ANY STEP.**

## Arguments

- `$ARGUMENTS` - Description of what to build/fix

## Flags

- `--skip-browser` - Skip browser verification (NOT recommended for UI changes)
- `--skip-tests` - Skip test execution in verify step
- `--continue` - Resume from last checkpoint
- `--from <phase>` - Start from specific phase
- `--rollback <phase>` - Rollback to checkpoint state
- `--status` - Show checkpoint status

## MANDATORY EXECUTION RULES

**YOU MUST FOLLOW THESE RULES:**

1. **NEVER skip any step** - All 7 steps must execute in order
2. **ALWAYS output step banner** - Print the step number/name before starting each step
3. **ALWAYS verify completion** - Confirm each step succeeded before moving to next
4. **ALWAYS run browser verification** - Unless `--skip-browser` is explicitly passed
5. **ALWAYS save checkpoints** - After each successful step
6. **STOP on critical failures** - Don't continue if a step fails critically

## Instructions

### Pre-flight Check

Before starting, verify:
```bash
# Check git status
git status

# Ensure clean working directory or stash
git stash --include-untracked || true
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 SHIP STARTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Feature: {description}
Browser verification: {enabled/disabled}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 1: PLAN (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1/7: PLAN
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

**CHECKPOINT: Save after plan completion**

```
[checkpoint] ✓ Saved after plan
```

---

### Step 2: IMPLEMENT (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 2/7: IMPLEMENT
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

**CHECKPOINT: Save after implementation**

```
[checkpoint] ✓ Saved after implement
```

---

### Step 3: REFACTOR (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 3/7: REFACTOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions:**
1. Use `refactorer` agent on ALL changed files
2. Agent will spawn `explorer` to verify patterns
3. Fix any issues found

**Refactorer checks:**
- Remove `any` types → proper TypeScript types
- Remove dead code
- Simplify over-abstractions
- Verify naming conventions
- Check for duplicate utilities

**Output:**
```
[refactorer] Analyzing: {file}
[refactorer] Fixed: {issue}
[refactorer] ✓ Complete (Files: N, Issues: N)
```

**Completion check:**
- [ ] No `any` types in changed files
- [ ] No dead code
- [ ] Consistent naming

**CHECKPOINT: Save after refactor**

```
[checkpoint] ✓ Saved after refactor
```

---

### Step 4: VERIFY (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 4/7: VERIFY
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

**CHECKPOINT: Save after verify**

```
[checkpoint] ✓ Saved after verify
```

---

### Step 5: REVIEW (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 5/7: REVIEW
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
- If CRITICAL issues found in code review → Loop back to Step 3
- If browser issues persist after 5 iterations → Stop and report

**Generate report:**
Save to `.claude/reviews/review-{date}.md`

**CHECKPOINT: Save after review**

```
[checkpoint] ✓ Saved after review
```

---

### Step 6: COMMIT (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 6/7: COMMIT
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

**CHECKPOINT: Save after commit**

```
[checkpoint] ✓ Saved after commit
```

---

### Step 7: PR (MANDATORY)

**YOU MUST EXECUTE THIS STEP. DO NOT SKIP.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 7/7: PR
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

**CHECKPOINT: Clear checkpoints on success**

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
  ✓ 3. Refactor  - {N} issues fixed
  ✓ 4. Verify    - Types ✓ Lint ✓ Build ✓ Tests ✓
  ✓ 5. Review    - Code ✓ Security ✓ Browser ✓
  ✓ 6. Commit    - {hash}
  ✓ 7. PR        - #{number}

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

## Checkpoint System

Each step saves a checkpoint for recovery:

```
/ship "add feature"
    ├─ CHECKPOINT: after plan
    ├─ CHECKPOINT: after implement
    ├─ CHECKPOINT: after refactor
    ├─ CHECKPOINT: after verify
    ├─ CHECKPOINT: after review
    ├─ CHECKPOINT: after commit
    └─ Complete: checkpoints cleared
```

### Recovery Flags

```bash
# Resume from last successful checkpoint
/ship --continue

# Start from specific phase
/ship --from verify

# Rollback to checkpoint state
/ship --rollback implement

# View checkpoint status
/ship --status
```

### On Failure

```
┌─────────────────────────────────────────────────────────────┐
│  ❌ SHIP FAILED at {phase}                                   │
├─────────────────────────────────────────────────────────────┤
│  Error: {description}                                        │
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
│  • /ship --rollback refactor  Undo and retry                │
│  • Fix manually, then /ship --from verify                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Agents Used (ALL MANDATORY)

| Step | Agent(s) | Parallel | MANDATORY |
|------|----------|----------|-----------|
| Plan | `explorer` | - | ✓ YES |
| Implement | `web-researcher` (if stuck) | - | ✓ YES |
| Refactor | `refactorer` (spawns `explorer`) | - | ✓ YES |
| Verify | `verifier` | - | ✓ YES |
| Review | `code-reviewer`, `security-auditor`, `performance-auditor`, `accessibility-tester` | ✓ Yes | ✓ YES |
| Review | `browser-tester` | - | ✓ YES (default) |
| Commit | `git-automator` | - | ✓ YES |
| PR | `git-automator` | - | ✓ YES |

**Total: 9 agents, 4 running in parallel during review**

---

## Error Handling

| Error | Action |
|-------|--------|
| Verification fails 5+ times | STOP, save checkpoint, ask user |
| Critical review issues | Loop back to refactor |
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
3. ✓ Did I execute Step 3 (Refactor)?
4. ✓ Did I execute Step 4 (Verify)?
5. ✓ Did I execute Step 5 (Review)?
6. ✓ Did I verify in browser (unless --skip-browser)?
7. ✓ Did I execute Step 6 (Commit)?
8. ✓ Did I execute Step 7 (PR)?
9. ✓ Did I output the summary?

**IF ANY ANSWER IS "NO", GO BACK AND COMPLETE THAT STEP.**

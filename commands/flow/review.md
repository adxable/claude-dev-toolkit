# Review

Comprehensive code review using multiple agents in parallel, with optional browser verification.

## Arguments

- `$ARGUMENTS` - Optional: file paths, `--browser` flag, or empty for all changed files

## Flags

- `--browser` - Enable browser verification with fix-verify loop
- `--browser-only` - Skip code review, only run browser verification

## Instructions

### 1. Parse Arguments

```
--browser       → Run code review + browser verification
--browser-only  → Skip code review, only browser verification
(no flag)       → Code review only (default)
```

### 2. Identify Changes

**If file paths provided:**
Review specified files.

**If no arguments:**
```bash
git diff main...HEAD --name-only | grep -E '\.(tsx?|jsx?)$'
```

### 3. Code Review Phase (Parallel)

Skip if `--browser-only` flag is set.

Run these agents **simultaneously**:

| Agent | Focus Area |
|-------|------------|
| `code-reviewer` | Types, patterns, error handling, conventions |
| `performance-auditor` | Re-renders, memoization, bundle size |
| `accessibility-tester` | WCAG compliance, keyboard nav, ARIA (optional) |

```
┌─────────────────────────────────────────────────────────┐
│                    PHASE 1: Code Review                  │
├─────────────────────────────────────────────────────────┤
│                         │                               │
│    ┌────────────────────┼────────────────────┐          │
│    │                    │                    │          │
│    ▼                    ▼                    ▼          │
│ [code-reviewer]  [performance-auditor]  [a11y-tester]   │
│    │                    │                    │          │
│    └────────────────────┼────────────────────┘          │
│                         │                               │
│                         ▼                               │
│               Code Review Report                        │
└─────────────────────────────────────────────────────────┘
```

### 4. Browser Verification Phase (Sequential)

Run if `--browser` or `--browser-only` flag is set.

```
┌─────────────────────────────────────────────────────────┐
│              PHASE 2: Browser Verification               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │              [browser-tester]                   │    │
│  │                                                 │    │
│  │   ┌──────┐   ┌───────┐   ┌─────┐   ┌──────┐    │    │
│  │   │Screen│ → │Analyze│ → │ Fix │ → │Verify│    │    │
│  │   │ shot │   │       │   │     │   │      │    │    │
│  │   └──────┘   └───────┘   └─────┘   └──────┘    │    │
│  │       ▲                               │        │    │
│  │       └───────── (loop) ──────────────┘        │    │
│  │                                                 │    │
│  │   Max iterations: 5                            │    │
│  └─────────────────────────────────────────────────┘    │
│                         │                               │
│                         ▼                               │
│               Browser Test Report                       │
└─────────────────────────────────────────────────────────┘
```

#### Browser Verification Steps

1. **Ensure dev server running**
   ```bash
   # Check if running
   lsof -i :5173 || pnpm dev &
   ```

2. **Navigate to application**
   - Claude opens Chrome via extension
   - Navigates to localhost URL
   - Waits for page load

3. **Visual verification**
   - Claude views the browser
   - Verifies components render correctly
   - Checks layout, colors, text

4. **Interaction testing**
   - Test buttons, links, forms
   - Verify responses

5. **If issues found → Fix-Verify Loop**
   ```
   For each issue:
   1. Document what Claude sees in browser
   2. Identify root cause in code
   3. Fix the code
   4. Wait for hot reload (~2s)
   5. Claude views browser again
   6. Verify fix
   7. If still broken, iterate (max 5)
   ```

6. **Report results**

### 5. Agent Tasks

**code-reviewer agent:**
- TypeScript types (no `any`)
- React patterns (hooks, memoization)
- Error handling
- CLAUDE.md convention compliance
- Dead code, unused imports

**performance-auditor agent:**
- Missing React.memo on list items
- Inline functions passed to memoized children
- Missing useCallback/useMemo
- Zustand selectors without useShallow
- Large components that should be split

**accessibility-tester agent (if available):**
- Semantic HTML
- Keyboard navigation
- ARIA attributes
- Color contrast
- Form labels

**browser-tester agent:**
- Visual verification (UI renders correctly)
- Interaction testing (buttons, forms work)
- Responsive design (mobile, tablet, desktop)
- State handling (loading, error, empty states)
- Fix-verify loop for issues

### 6. Generate Combined Report

Create report at `.claude/reviews/review-{date}.md`:

```markdown
# Code Review Report

**Branch:** {branch}
**Date:** {date}
**Files Reviewed:** {count}
**Agents Used:** code-reviewer, performance-auditor, accessibility-tester, browser-tester
**Browser Verification:** {enabled/disabled}

## Summary

{2-3 sentence overview combining all agent findings}

---

## Code Quality (code-reviewer)

### Critical
| File | Line | Issue | Suggestion |
|------|------|-------|------------|

### Important
| File | Line | Issue | Suggestion |
|------|------|-------|------------|

### Minor
- {file}:{line} - {suggestion}

---

## Performance (performance-auditor)

### Critical
| File | Line | Issue | Impact |
|------|------|-------|--------|

### Warnings
- {file}:{line} - {issue}

### Opportunities
- {optimization opportunity}

---

## Accessibility (accessibility-tester)

### WCAG Violations
| File | Line | Level | Issue |
|------|------|-------|-------|

### Improvements
- {suggestion}

---

## Browser Verification (browser-tester)

### Issues Found & Fixed
| # | Issue | File | Fix | Verified |
|---|-------|------|-----|----------|
| 1 | {issue} | {file}:{line} | {fix} | ✓ |

### Visual Tests
| Test | Status |
|------|--------|
| Page loads | ✓ Pass |
| Components render | ✓ Pass |
| Interactions work | ✓ Pass |
| Responsive design | ✓ Pass |

### Loop Summary
- Iterations: {N}
- Issues found: {N}
- Issues fixed: {N}
- Unresolved: {N}

---

## Combined Checklist

- [ ] No `any` types
- [ ] Proper error handling
- [ ] Memoization where needed
- [ ] useShallow for Zustand
- [ ] Keyboard navigation works
- [ ] Color contrast meets 4.5:1
- [ ] UI renders correctly (browser verified)
- [ ] Interactions work (browser verified)

---

## Metrics

| Category | Critical | Important | Minor |
|----------|----------|-----------|-------|
| Code Quality | {n} | {n} | {n} |
| Performance | {n} | {n} | {n} |
| Accessibility | {n} | {n} | {n} |
| Browser | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** |
```

### 7. Summary

```
Review complete.

Report: .claude/reviews/review-{date}.md

Agents used:
  ✓ code-reviewer
  ✓ performance-auditor
  ✓ accessibility-tester (optional)
  ✓ browser-tester (if --browser flag)

Issues found:
  Critical:  {N}
  Important: {N}
  Minor:     {N}

Browser verification:
  Issues fixed: {N}
  Iterations:   {N}
  Status:       All passing / {N} unresolved

Next step:
  /commit
```

## Usage Examples

```bash
# Code review only (default)
/review

# Code review + browser verification
/review --browser

# Browser verification only (skip code review)
/review --browser-only

# Review specific files with browser
/review src/components/Button.tsx --browser
```

## Workflow Position

```
/plan → /implement → /verify → /review → /commit → /pr
                                  ↑
                              YOU ARE HERE
```

## Parallel Execution Note

Code review agents (code-reviewer, performance-auditor, accessibility-tester) run simultaneously.

Browser verification (browser-tester) runs sequentially after code review to allow fixes during the loop.

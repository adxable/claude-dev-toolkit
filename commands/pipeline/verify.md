# Verify

Type check, lint, build, and optionally run tests.

## Arguments

- `$ARGUMENTS` - Optional: "--skip-tests" or "--tests-only" or "--skip-browser" or URL path
- `--skip-tests` - Skip test execution even if detected
- `--tests-only` - Run only tests, skip type/lint/build
- `--e2e` - Include E2E tests (Playwright/Cypress)
- `--fix` - Auto-fix all fixable issues
- `--skip-browser` - Skip browser verification (static checks only)

## Prerequisites

- Claude Chrome extension installed and connected (for browser verification)
- Dev server running (or will be started automatically)

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

### 2. Run Static Checks (Parallel)

**Skip if `--tests-only` flag is provided.**

Run type check and lint in parallel:

```bash
# Check 1: TypeScript
npx tsc --noEmit

# Check 2: ESLint
npx eslint src/
```

### 3. Evaluate Static Check Results

```
[Type Check] ✓ Passed | ✗ {N} errors
[Lint]       ✓ Passed | ✗ {N} errors
```

### 4. Handle Static Failures

For each failure type:

**Type errors:**
- List errors with file:line
- Attempt auto-fix (max 3 iterations)

**Lint errors:**
- Run `npm run lint:fix` if available and `--fix` flag provided
- Manual fix remaining

### 5. Build

**Skip if `--tests-only` flag is provided.**

After static checks pass:

```bash
npm run build
```

**Build errors:**
- Analyze error output
- Suggest fixes

### 6. Run Tests (If Detected)

**Only if HAS_TESTS=true AND --skip-tests not passed:**

```bash
# Unit tests
npm test

# If playwright detected and --e2e flag
npx playwright test
```

**Test failures:**
- Show failed test names
- Ask: "Fix failing tests? [Y/n]"
- If yes, analyze and fix (max 3 iterations)

### 7. Browser Verification (Chrome Extension)

**IMPORTANT: Always use Claude Chrome extension tools (`mcp__claude-in-chrome__*`). Never use Playwright MCP.**

Skip this phase if `--skip-browser` flag is provided or `--tests-only` flag is provided.

#### 7.1 Ensure Dev Server Running

```bash
# Check if dev server is running on common ports
lsof -i :5173 || lsof -i :3000 || pnpm dev &
```

#### 7.2 Get Browser Context

Use `mcp__claude-in-chrome__tabs_context_mcp` to get available tabs:
- If no tab group exists, create one with `createIfEmpty: true`
- Create a new tab with `mcp__claude-in-chrome__tabs_create_mcp`

#### 7.3 Navigate to Application

Use `mcp__claude-in-chrome__navigate` to navigate to:
- `http://localhost:5173{url}` (Vite default)
- Or `http://localhost:3000{url}` (CRA/Next default)

#### 7.4 Visual Verification

Use `mcp__claude-in-chrome__computer` with `action: screenshot` to view the page.

**Verification Checklist:**
```
□ Page loads without errors
□ Layout renders correctly
□ All components visible
□ No visual glitches/overlaps
□ Text is readable
□ Images load correctly
```

#### 7.5 Check Console Errors

Use `mcp__claude-in-chrome__read_console_messages` with `onlyErrors: true` to check for:
- JavaScript errors
- React errors
- Network failures

#### 7.6 Interaction Testing (Quick)

Use Chrome extension tools to verify basic interactions:
- `mcp__claude-in-chrome__find` - Find interactive elements
- `mcp__claude-in-chrome__computer` with clicks - Test buttons work
- `mcp__claude-in-chrome__read_page` - Verify DOM structure

#### 7.7 Fix-Verify Loop

If issues found:

```
┌──────────────────────────────────────────────────────────┐
│                    FIX-VERIFY LOOP                        │
│                                                          │
│    ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│    │Screenshot│ ──▶ │ Analyze │ ──▶ │  Fix    │          │
│    │         │     │ Issue   │     │  Code   │          │
│    └─────────┘     └────┬────┘     └────┬────┘          │
│         ▲               │               │                │
│         │               │ No Issue      │                │
│         │               ▼               │                │
│         │          ┌─────────┐          │                │
│         └──────────│Re-verify│◀─────────┘                │
│                    └─────────┘                           │
│                         │                                │
│                         │ All Pass                       │
│                         ▼                                │
│                    ┌─────────┐                           │
│                    │  Done   │                           │
│                    └─────────┘                           │
│                                                          │
│  Max iterations: 5                                       │
└──────────────────────────────────────────────────────────┘
```

1. Take screenshot with `mcp__claude-in-chrome__computer`
2. Analyze what Claude sees in the browser
3. If issue found, fix the code using Edit tool
4. Wait for hot reload (~2 seconds)
5. Take new screenshot and verify fix
6. Repeat until all issues resolved (max 5 iterations)

### 8. Output Summary

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ VERIFICATION COMPLETE                                    │
├─────────────────────────────────────────────────────────────┤
│  Type Check:  ✓ Pass (0 errors)                             │
│  Lint:        ✓ Pass (2 warnings)                           │
│  Build:       ✓ Pass                                        │
│  Tests:       ✓ Pass (45/45) [optional - if detected]       │
│               ○ Skipped (no tests detected)                 │
│  Browser:     ✓ Verified (Chrome Extension)                 │
├─────────────────────────────────────────────────────────────┤
│  Static Check Iterations: {N}                               │
│  Test Iterations: {N}                                       │
│  Browser Iterations: {N}                                    │
│  Issues fixed: {N}                                          │
└─────────────────────────────────────────────────────────────┘

Next step:
  /review
```

## Chrome Extension Tools Reference

| Tool | Purpose |
|------|---------|
| `tabs_context_mcp` | Get/create tab context |
| `tabs_create_mcp` | Create new tab |
| `navigate` | Go to URL |
| `computer` (screenshot) | View page state |
| `computer` (left_click) | Click elements |
| `read_page` | Get DOM accessibility tree |
| `find` | Find elements by description |
| `read_console_messages` | Check for errors |
| `form_input` | Fill form fields |

## Usage Examples

```bash
# Full verification (static + tests + browser at root)
/verify

# Verify specific page
/verify /dashboard

# Static checks only (no browser, no tests)
/verify --skip-browser --skip-tests

# Tests only
/verify --tests-only

# Include E2E tests
/verify --e2e

# Auto-fix all issues
/verify --fix

# Verify login page
/verify /login
```

## Workflow Position

```
/plan → /implement → /refactor → /verify → /review → /commit → /pr
                                    ↑
                        Now includes testing!
```

# Verification Loop

Run a complete verification cycle including type checking, linting, and build. Automatically fixes issues and re-runs until all checks pass.

## Arguments

- `$ARGUMENTS` - Optional: URL path for browser testing (e.g., `/dashboard`)

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json` for:
- Package manager
- Validation commands
- Project paths

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    VERIFICATION LOOP                        │
├─────────────────────────────────────────────────────────────┤
│  1. PARALLEL STATIC CHECKS (run simultaneously)             │
│     ├── Type Check (tsc --noEmit)                           │
│     └── Lint Check (eslint)                                 │
│                                                             │
│  2. BUILD CHECK (sequential, depends on #1)                 │
│     └── Build command (vite build / next build / etc.)      │
│                                                             │
│  3. BROWSER VERIFICATION (optional)                         │
│     └── Navigate to URL and check for errors                │
│                                                             │
│  4. ISSUE RESOLUTION                                        │
│     └── If issues found → Fix → Return to step 1            │
│                                                             │
│  5. SUCCESS                                                 │
│     └── All checks pass → Report summary                    │
└─────────────────────────────────────────────────────────────┘
```

## Instructions

### Phase 1: Parallel Static Analysis

Launch TWO checks IN PARALLEL:

**Check 1 - Type Check:**
```bash
{config.commands.typeCheck || "npx tsc --noEmit"}
```

**Check 2 - Lint Check:**
```bash
{config.commands.lint || "npx eslint src/"}
```

Display:
```
═══════════════════════════════════════════════════
           VERIFICATION ITERATION {N}
═══════════════════════════════════════════════════

Running parallel static checks...

[Type Check] ⏳ Running...
[Lint Check] ⏳ Running...
```

### Phase 2: Evaluate Static Results

After both complete:

```
[Type Check] {✅ Passed | ❌ {N} errors}
[Lint Check] {✅ Passed | ❌ {N} errors}
```

- If BOTH passed → proceed to Phase 3
- If ANY failed → proceed to Phase 4 (Fix Issues)

### Phase 3: Build Verification

Only run if static checks passed:

```bash
{config.commands.build || "npm run build"}
```

Display:
```
[Build] ⏳ Running...
[Build] {✅ Passed | ❌ Failed}
```

- If build passes → proceed to Browser Verification (if URL provided)
- If build fails → proceed to Phase 4 (Fix Issues)

### Phase 4: Browser Verification (Optional)

If `$ARGUMENTS` contains a URL:

1. Parse URL (prepend `http://localhost:3000` if relative path)
2. Navigate using Playwright MCP
3. Wait for page load
4. Check for console errors
5. Take screenshot

```
Browser Verification:
  URL: {full_url}
  [Page Load] ✅ Loaded in {time}ms
  [Console] {✅ No errors | ❌ {N} errors}
  [Screenshot] Saved to .claude/screenshots/verify-{timestamp}.jpeg
```

### Phase 5: Issue Resolution Loop

When issues are found:

1. **Display issues:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Issues Found:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TypeScript Errors:
  • src/components/Button.tsx:15 - Type 'string' not assignable to 'number'
  • src/hooks/useData.ts:23 - Property 'name' does not exist

ESLint Errors:
  • src/utils/helpers.ts:10 - 'unused' is defined but never used
```

2. **Fix issues:**
   - TypeScript errors → Fix type annotations
   - ESLint errors → Fix or add disable comment with explanation
   - Build errors → Fix compilation issues

3. **Re-run verification:**
   - Return to Phase 1
   - Track iteration count

4. **Maximum iterations: 5**
   - If still failing after 5 attempts, report and ask user

### Phase 6: Success Report

When all checks pass:

```
═══════════════════════════════════════════════════
           ✅ VERIFICATION COMPLETE
═══════════════════════════════════════════════════

Static Analysis:
  ✅ TypeScript: No errors
  ✅ ESLint: No violations

Build:
  ✅ Build successful

{Browser Testing (if URL provided):
  ✅ Page loads correctly
  ✅ No console errors}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
  Iterations: {N}
  Issues Fixed: {total}
  Time: {duration}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. CODE REVIEW:
   /review

2. CREATE COMMIT:
   /utils:commit

3. CREATE PR:
   /utils:pr

═══════════════════════════════════════════════════
```

## Important Rules

1. **Always run type-check and lint in PARALLEL**
2. **Never skip the loop** - If issues found, fix and verify again
3. **Track all iterations** - Report progress after each cycle
4. **Be specific about errors** - Include file paths and line numbers
5. **Maximum 5 iterations** - Ask user if still failing

## Report

Return a summary of:
- All checks passed/failed
- Issues fixed
- Number of iterations

# Verify

Run type checking, linting, and build. Fix issues automatically.

## Arguments

- `$ARGUMENTS` - Optional: URL path for browser testing (e.g., `/dashboard`)

## Instructions

### 1. Run Checks (Parallel)

Run type check and lint in parallel:

```bash
# Check 1: TypeScript
npx tsc --noEmit

# Check 2: ESLint
npx eslint src/
```

### 2. Evaluate Results

```
[Type Check] ✓ Passed | ✗ {N} errors
[Lint]       ✓ Passed | ✗ {N} errors
```

### 3. Fix Issues

If errors found:
1. Fix TypeScript errors (type annotations, null checks)
2. Fix ESLint errors (or disable with explanation)
3. Re-run checks
4. Repeat until all pass (max 5 iterations)

### 4. Build

After static checks pass:

```bash
npm run build
```

### 5. Browser Test (Optional)

If URL provided in arguments:
1. Navigate to `http://localhost:3000{url}`
2. Check for console errors
3. Take screenshot

### 6. Summary

```
Verification complete.

✓ Type Check: Passed
✓ Lint: Passed
✓ Build: Passed
{✓ Browser: No errors (if URL provided)}

Iterations: {N}
Issues fixed: {N}

Next step:
  /review
```

## Workflow Position

```
/plan → /implement → /refactor → /verify → /review → /commit → /pr
                                    ↑
                                YOU ARE HERE
```

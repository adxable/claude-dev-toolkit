# Refactor

Clean up code using the refactorer agent.

## Arguments

- `$ARGUMENTS` - Optional: specific file paths, or empty for all changed files on branch

## Instructions

### 1. Identify Target Files

**If file paths provided:**
```
Refactoring: {provided paths}
```

**If no arguments:**
```bash
git diff main...HEAD --name-only | grep -E '\.(tsx?|jsx?)$'
```

### 2. Invoke Refactorer Agent

Use the `refactorer` agent to:
- Eliminate `any` types
- Remove dead code and unused imports
- Inline single-use abstractions
- Split oversized functions/components
- Fix silent error handling

### 3. Verify After Changes

Run verification after refactoring:
```bash
npx tsc --noEmit
npx eslint src/
```

If verification fails, revert breaking changes and continue.

### 4. Summary

```
Refactoring complete.

Changes:
  - {file}: Removed 3 any types
  - {file}: Inlined single-use helper
  - {file}: Removed unused imports

Lines removed: {N}

Next step:
  /verify
```

## Workflow Position

```
/plan → /implement → /refactor → /verify → /review → /commit → /pr
                        ↑
                    YOU ARE HERE
```

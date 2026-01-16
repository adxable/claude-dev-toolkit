# Lint Check

Run ESLint and optionally fix errors.

## Arguments

- `$ARGUMENTS` - Optional: `--fix` to automatically fix lint errors

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Instructions

### Step 1: Run Lint Check

```bash
{config.commands.lint || "npx eslint src/"}

# If --fix argument provided:
{config.commands.lint || "npx eslint src/"} --fix
```

### Step 2: Parse Results

```
═══════════════════════════════════════════════════
           LINT CHECK RESULTS
═══════════════════════════════════════════════════

{✅ No lint errors | ❌ {N} errors, {M} warnings}

{If errors:}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Errors by file:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 src/utils/helpers.ts
   Line 10: 'unused' is defined but never used (@typescript-eslint/no-unused-vars)
   Line 15: Unexpected console statement (no-console)

📄 src/components/Modal.tsx
   Line 5: Missing return type on function (@typescript-eslint/explicit-function-return-type)
```

### Step 3: Report

```
═══════════════════════════════════════════════════

{Summary of auto-fixed issues if --fix was used}

{If remaining errors:}
Manual fixes needed for:
  • {rule-name}: {count} occurrences

═══════════════════════════════════════════════════
```

# Type Check

Run TypeScript type checking and optionally fix errors.

## Arguments

- `$ARGUMENTS` - Optional: `--fix` to automatically fix type errors

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Instructions

### Step 1: Run Type Check

```bash
{config.commands.typeCheck || "npx tsc --noEmit"}
```

### Step 2: Parse Results

If errors found, parse and categorize:

```
═══════════════════════════════════════════════════
           TYPE CHECK RESULTS
═══════════════════════════════════════════════════

{✅ No type errors found | ❌ {N} type errors found}

{If errors:}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Errors by file:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 src/components/Button.tsx
   Line 15: Type 'string' is not assignable to type 'number'
   Line 23: Property 'onClick' is missing in type

📄 src/hooks/useData.ts
   Line 10: Cannot find name 'fetchData'
```

### Step 3: Fix Errors (if --fix)

If `$ARGUMENTS` contains `--fix`:

1. Read each file with errors
2. Load `typescript-standards` skill
3. Fix type issues:
   - Add missing type annotations
   - Fix type mismatches
   - Add missing properties
   - Import missing types
4. Re-run type check
5. Repeat until no errors or max 3 iterations

### Step 4: Report

```
═══════════════════════════════════════════════════

{If fixed:}
✅ Fixed {N} type errors

{If still errors:}
❌ {N} errors remaining - manual fix required

═══════════════════════════════════════════════════
```

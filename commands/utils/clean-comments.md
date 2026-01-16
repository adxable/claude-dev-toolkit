# Clean Comments

Remove all [CR] code review comments from the codebase after issues have been addressed.

## Arguments

None

## Instructions

### Step 1: Find All [CR] Comments

Search for files containing `// [CR]` comments:

```bash
grep -r "\[CR\]" src/ --include="*.tsx" --include="*.ts" -l
```

### Step 2: Display Found Comments

```
═══════════════════════════════════════════════════
        CLEANING CODE REVIEW COMMENTS
═══════════════════════════════════════════════════

Found [CR] comments in:
  • src/components/Button.tsx (3 comments)
  • src/hooks/useData.ts (2 comments)

Total: 5 comments to remove
```

### Step 3: Remove Comments

For each file:
1. Read the file
2. Remove lines containing `// [CR]`
3. Save the file

### Step 4: Report

```
═══════════════════════════════════════════════════
           CLEANUP COMPLETE
═══════════════════════════════════════════════════

Removed 5 [CR] comments from 2 files.

Files cleaned:
  • src/components/Button.tsx
  • src/hooks/useData.ts

═══════════════════════════════════════════════════
```

## Report

Return count of comments removed and files modified.

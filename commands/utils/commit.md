# Generate Git Commit

Analyze changes and create a well-formatted git commit.

## Arguments

- `$ARGUMENTS` - Optional: commit type override (feat, fix, chore, refactor, docs, test)

## Instructions

### Step 1: Analyze Changes

```bash
# Check current status
git status

# See staged changes
git diff --cached

# See unstaged changes
git diff

# See recent commits for style reference
git log --oneline -5
```

### Step 2: Determine Commit Type

Based on the changes, determine the commit type:

- `feat` - New feature or functionality
- `fix` - Bug fix
- `chore` - Maintenance, dependencies, config
- `refactor` - Code restructuring without behavior change
- `docs` - Documentation only
- `test` - Adding or updating tests
- `style` - Formatting, whitespace (no code change)
- `perf` - Performance improvement

If `$ARGUMENTS` provided, use that as override.

### Step 3: Generate Commit Message

Format: `{type}: {description}`

Rules:
- Present tense ("add", not "added")
- Lowercase first letter after type
- 50 characters or less
- No period at the end
- Descriptive of actual changes

### Step 4: Stage and Commit

```bash
# Stage all changes
git add -A

# Create commit
git commit -m "{generated_message}"
```

### Step 5: Display Result

```
═══════════════════════════════════════════════════
           COMMIT CREATED
═══════════════════════════════════════════════════

{commit_hash} {commit_message}

Files changed: {count}
Insertions: +{count}
Deletions: -{count}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. PUSH TO REMOTE:
   git push

2. CREATE PR:
   /utils:pr

═══════════════════════════════════════════════════
```

## Report

Return the commit message that was used.

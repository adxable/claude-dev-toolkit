# Commit

Create a git commit using the git-automator agent.

## Arguments

- `$ARGUMENTS` - Optional: commit type override (feat, fix, chore, refactor, docs, test)

## Instructions

### 1. Invoke Git-Automator Agent

Use the `git-automator` agent to:
- Analyze staged and unstaged changes
- Determine commit type from changes
- Generate commit message

### 2. Analyze Changes

```bash
git status
git diff --staged
git diff
git log --oneline -5  # For style reference
```

### 3. Generate Commit

Format:
```
{type}: {description}

{Optional body explaining what and why}

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring
- `chore` - Maintenance
- `docs` - Documentation
- `test` - Tests

### 4. Create Commit

```bash
git add -A
git commit -m "{message}"
```

### 5. Summary

```
Commit created.

{hash} {type}: {description}

Files: {N} changed
+{insertions} -{deletions}

Next step:
  /pr
```

## Workflow Position

```
/plan → /implement → /verify → /review → /commit → /pr
                                            ↑
                                        YOU ARE HERE
```

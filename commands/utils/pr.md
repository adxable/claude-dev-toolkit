# Create Pull Request

Generate a well-formatted pull request description and create the PR.

## Arguments

- `$ARGUMENTS` - Optional: base branch (default: main)

## Instructions

### Step 1: Gather Information

```bash
# Get current branch
git branch --show-current

# Get commits since branching from base
git log {base}...HEAD --oneline

# Get full diff
git diff {base}...HEAD --stat

# Check if pushed to remote
git status
```

### Step 2: Analyze Changes

Review all commits and changes to understand:
- What feature/fix/chore was implemented
- What files were changed
- What the impact is

### Step 3: Generate PR Description

```markdown
## Summary

{2-3 bullet points describing the changes}

## Changes

{List of main changes by category}

### Added
- {new features/files}

### Changed
- {modifications}

### Fixed
- {bug fixes}

## Test Plan

- [ ] {How to test change 1}
- [ ] {How to test change 2}

## Screenshots

{If UI changes, note that screenshots should be added}
```

### Step 4: Push and Create PR

```bash
# Push to remote if needed
git push -u origin {branch_name}

# Create PR using GitHub CLI
gh pr create --title "{title}" --body "{description}" --base {base_branch}
```

### Step 5: Display Result

```
═══════════════════════════════════════════════════
           PULL REQUEST CREATED
═══════════════════════════════════════════════════

PR #{number}: {title}
URL: {pr_url}

Base: {base_branch} ← {current_branch}
Commits: {count}
Files changed: {count}

═══════════════════════════════════════════════════
```

## Report

Return the PR URL.

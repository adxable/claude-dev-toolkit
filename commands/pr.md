# PR

Create a pull request using the git-automator agent.

## Arguments

- `$ARGUMENTS` - Optional: base branch (default: main)

## Instructions

### 1. Invoke Git-Automator Agent

Use the `git-automator` agent to:
- Analyze all commits on branch
- Generate PR description
- Create the PR

### 2. Gather Information

```bash
git branch --show-current
git log main...HEAD --oneline
git diff main...HEAD --stat
```

### 3. Generate PR Description

```markdown
## Summary

- {Bullet point 1}
- {Bullet point 2}

## Changes

### Added
- {New features/files}

### Changed
- {Modifications}

### Fixed
- {Bug fixes}

## Test Plan

- [ ] {How to verify change 1}
- [ ] {How to verify change 2}
```

### 4. Push and Create PR

```bash
git push -u origin HEAD

gh pr create \
  --title "{type}: {description}" \
  --body "{generated description}" \
  --base {base_branch}
```

### 5. Summary

```
PR created.

#{number}: {title}
URL: {pr_url}

Base: {base} ← {branch}
Commits: {N}
Files changed: {N}
```

## Workflow Position

```
/plan → /implement → /refactor → /verify → /review → /commit → /pr
                                                                 ↑
                                                             YOU ARE HERE
                                                                 ✓ DONE
```

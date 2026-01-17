# Implement

Execute a plan file step by step.

## Arguments

- `$ARGUMENTS` - Path to plan file (e.g., `.claude/plans/plan-user-auth.md`)

## Instructions

### 1. Load Plan

Read the plan file and extract:
- Implementation steps
- Files to create/modify
- Verification criteria

### 2. Execute Steps

For each step in the plan:

1. Announce: `Step {N}/{Total}: {description}`
2. Implement the changes
3. Quick type check if TypeScript files changed
4. Mark complete: `✓ Step {N} complete`

Use agents when needed:
- Stuck on issue → `web-researcher` agent
- Need to find patterns → `explorer` agent

### 3. Summary

```
Implementation complete.

Files created:
  - path/to/new/file.tsx

Files modified:
  - path/to/existing/file.tsx

Next step:
  /refactor
```

## Workflow Position

```
/plan → /implement → /refactor → /verify → /review → /commit → /pr
           ↑
       YOU ARE HERE
```

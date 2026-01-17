# {{FEATURE_NAME}}

## Overview

{{FEATURE_DESCRIPTION}}

## Development Approach

You are using the **adx-toolkit** plugin with structured commands.
Follow this workflow to implement the feature:

### Primary Command

```bash
/ship "{{FEATURE_NAME}}" {{BROWSER_FLAG}}
```

This runs the full pipeline: plan → implement → refactor → verify → review → commit → pr

### If /ship Fails

Break down into individual commands:

1. `/plan "{{FEATURE_NAME}}"` - Research and create plan
2. `/implement` - Execute the plan
3. `/refactor` - Clean up code
4. `/verify` - Type check + lint + build
5. `/review {{BROWSER_FLAG}}` - Code review + visual verification
6. `/commit` - Create commit
7. `/pr` - Create pull request

### On Errors

- **Type errors**: Fix types, run `/verify` again
- **Lint errors**: Fix issues, run `/verify` again
- **Build errors**: Analyze error, fix code, run `/verify` again
- **Review issues**: Run `/refactor` then `/review` again
- **Browser issues**: Fix UI, wait for hot reload, verify again

## Tech Stack (from CLAUDE.md)

- **Router**: TanStack Router / React Router v7
- **State**: Zustand (UI state only, use `useShallow` for objects)
- **Server State**: TanStack Query with `useSuspenseQuery`
- **Forms**: React Hook Form + Zod
- **Styling**: Tailwind + shadcn/ui (use `cn()` for conditionals)

## Patterns to Follow

- Named exports, not default exports
- Query Options Factory pattern for TanStack Query
- Feature-based folder structure: `src/features/{feature}/`
- Collocate components, hooks, types within features

## Anti-patterns to Avoid

- No `any` types
- No Zustand selectors without `useShallow`
- No index as key in lists
- No inline functions for memoized children

## Success Criteria

- [ ] Feature implemented and functional
- [ ] TypeScript types correct (no `any`)
- [ ] Follows CLAUDE.md conventions
- [ ] Build passes (`npm run build`)
- [ ] Lint passes (`npx eslint src/`)
{{BROWSER_CRITERIA}}
- [ ] PR created with description

## Status Reporting

After each action, report:

```
STATUS: IN_PROGRESS | COMPLETE | BLOCKED
TASKS_DONE: X/Y
FILES_MODIFIED: [list]
CURRENT_STEP: plan | implement | refactor | verify | review | commit | pr
ERRORS: [any blocking errors]
EXIT_SIGNAL: false | true
```

## EXIT_SIGNAL Conditions

Set `EXIT_SIGNAL: true` ONLY when ALL of these are met:

1. PR has been successfully created (you have the PR URL)
2. All success criteria checked off
3. No blocking errors remain
4. Build and lint passing

**Important**: Do NOT set EXIT_SIGNAL: true if:
- PR creation failed
- There are unresolved errors
- Any success criteria unchecked
- You're still working on implementation

## Current Status

Starting fresh - no work completed yet.

---

*This project uses adx-toolkit for structured development workflows.*

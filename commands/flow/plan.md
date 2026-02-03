# Plan

Research and plan a feature, bug fix, or task before implementation.

## Arguments

- `$ARGUMENTS` - Description of what to build/fix

## Instructions

### 1. Research Phase

Use the `explorer` agent to understand the codebase:
- Find similar implementations
- Identify relevant files and patterns
- Understand existing architecture

### 2. Create Plan

Create a plan file at `.claude/plans/plan-{descriptive-name}.md`:

```markdown
# Plan: {Title}

**Type:** Feature / Bug Fix / Refactor
**Created:** {date}

## Goal

{What we're trying to achieve}

## Research Findings

{What explorer agent found - similar patterns, relevant files}

## Approach

{High-level approach}

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| path/to/file | Create/Modify | Why |

## Implementation Steps

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Verification

- [ ] Type check passes
- [ ] Lint passes
- [ ] Build passes
- [ ] {Feature-specific verification}
```

### 3. Output

```
Plan created: .claude/plans/plan-{name}.md

Next step:
  /implement .claude/plans/plan-{name}.md
```

## Workflow Position

```
/plan → /implement → /verify → /review → /commit → /pr
  ↑
  YOU ARE HERE
```

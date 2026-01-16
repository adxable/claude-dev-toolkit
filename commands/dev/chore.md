# Chore Planning

Create a plan for maintenance, refactoring, or technical debt work. This command creates a plan document only - it does NOT implement any changes.

## Arguments

- `$ARGUMENTS` - Description of the maintenance task

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Critical Rules

**This command creates a PLAN only. You MUST NOT implement any changes.**

## Instructions

### Step 1: Load Configuration

```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Chore Planning
   └─ Type: Maintenance/Refactoring
═══════════════════════════════════════════════════
```

### Step 2: Analyze the Chore

Based on `$ARGUMENTS`, determine the type:

- **Refactoring:** Code restructuring without behavior change
- **Dependency Update:** Updating packages
- **Technical Debt:** Addressing known issues
- **Configuration:** Build/tooling changes
- **Documentation:** Updating docs
- **Cleanup:** Removing dead code

### Step 3: Research Impact

1. Identify affected files
2. Check for dependencies on affected code
3. Assess risk level
4. Identify testing requirements

### Step 4: Create Chore Plan

Create the plan file at `{specsPath}/chore-{descriptive-name}.md`:

```markdown
# Chore: {Chore Title}

## Metadata

- **Type:** Chore
- **Category:** {Refactoring/Dependency/TechDebt/Config/Docs/Cleanup}
- **Created:** {YYYY-MM-DD}
- **Status:** Planning
- **Risk Level:** {Low/Medium/High}

## Description

{What needs to be done and why}

## Motivation

{Why is this chore necessary?}

- {Reason 1}
- {Reason 2}

## Scope

### In Scope
- {What will be changed}

### Out of Scope
- {What will NOT be changed}

## Affected Files

- `{path/to/file1}` - {what will change}
- `{path/to/file2}` - {what will change}

## Implementation Plan

### Step 1: {Task}
- {Specific action}

### Step 2: {Task}
- {Specific action}

## Risk Assessment

### Potential Issues
- {Risk 1} - Mitigation: {how to handle}

### Rollback Plan
{How to revert if something goes wrong}

## Testing Strategy

- {How to verify the chore is complete}
- {How to ensure no regression}

## Validation Commands

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] No regression in existing functionality

## Notes

{Additional context}
```

### Step 5: Display Success Message

```
═══════════════════════════════════════════════════
           CHORE PLAN CREATED
═══════════════════════════════════════════════════

Plan saved to: {plan_file_path}

Category: {category}
Risk Level: {risk}
Files Affected: {count}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this chore, run:

  /dev:implement {plan_file_path}

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the plan file created.

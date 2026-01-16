# Bug Fix Planning

Create a plan to investigate and fix a bug. This command creates a plan document only - it does NOT implement any fixes.

## Arguments

- `$ARGUMENTS` - Bug description or error message

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Critical Rules

**This command creates a PLAN only. You MUST NOT implement any fixes.**

## Instructions

### Step 1: Load Configuration and Skills

```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Bug Fix Planning
   └─ Tech Stack: {from config}
═══════════════════════════════════════════════════
```

### Step 2: Investigate the Bug

Based on the bug description in `$ARGUMENTS`:

1. **Search for related code:**
   - Use grep to find relevant files
   - Look for error messages, component names, function names

2. **Identify the affected area:**
   - Which component(s)?
   - Which feature?
   - Which API endpoint?

3. **Understand the current behavior:**
   - Read the relevant code
   - Trace the data flow
   - Identify the root cause

4. **Determine the expected behavior:**
   - What should happen instead?
   - Are there similar working implementations?

### Step 3: Create Bug Fix Plan

Create the plan file at `{specsPath}/bug-{descriptive-name}.md`:

```markdown
# Bug Fix: {Bug Title}

## Metadata

- **Type:** Bug
- **Created:** {YYYY-MM-DD}
- **Status:** Planning
- **Severity:** {Critical/High/Medium/Low}

## Bug Description

{What is happening? Include error messages if applicable}

## Steps to Reproduce

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Expected Behavior

{What should happen instead}

## Current Behavior

{What is currently happening}

## Root Cause Analysis

### Investigation Findings

{What did you discover while investigating?}

### Root Cause

{What is causing the bug?}

### Affected Files

- `{path/to/file1}` - {how it's affected}
- `{path/to/file2}` - {how it's affected}

## Solution Approach

### Option 1 (Recommended): {Approach name}

{Description of the fix}

**Pros:**
- {Pro 1}
- {Pro 2}

**Cons:**
- {Con 1}

### Option 2: {Alternative approach}

{Description of alternative}

## Implementation Plan

### Step 1: {Fix description}
- {Specific change}
- {File to modify}

### Step 2: {Verification}
- {How to verify the fix}

## Testing Strategy

### Regression Testing
- Ensure existing functionality still works

### Bug Verification
- Confirm the bug is fixed

### Edge Cases
- {Edge case to test}

## Validation Commands

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Acceptance Criteria

- [ ] Bug no longer occurs
- [ ] No regression in related functionality
- [ ] All tests pass

## Notes

{Any additional context or related issues}
```

### Step 4: Display Success Message

```
═══════════════════════════════════════════════════
           BUG FIX PLAN CREATED
═══════════════════════════════════════════════════

Plan saved to: {plan_file_path}

Root Cause: {brief description}
Recommended Fix: {approach summary}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this bug fix, run:

  /dev:implement {plan_file_path}

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the plan file created.

# Implement Plan

Execute a plan document step-by-step. This command reads a plan file and implements each task in order.

## Arguments

- `$ARGUMENTS` - Path to the plan file (e.g., `.claude/specs/feature-user-auth.md`)

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Instructions

### Step 1: Load and Validate Plan

Read the plan file from `$ARGUMENTS`:

```
═══════════════════════════════════════════════════
🚀 Invoking [react-developer] agent...
   └─ Task: Plan Implementation
   └─ Plan: {plan_file_path}
═══════════════════════════════════════════════════
```

Parse the plan to extract:
- Feature/Bug/Chore name
- Step by step tasks
- Relevant files
- Validation commands
- Acceptance criteria

### Step 2: Display Implementation Overview

```
═══════════════════════════════════════════════════
           IMPLEMENTATION OVERVIEW
═══════════════════════════════════════════════════

Plan: {plan name}
Type: {Feature/Bug/Chore}
Tasks: {number of tasks}

Steps to implement:
1. {Task 1 summary}
2. {Task 2 summary}
3. {Task 3 summary}
...

═══════════════════════════════════════════════════
```

### Step 3: Execute Tasks Sequentially

For each task in the "Step by Step Tasks" section:

1. **Announce the task:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Task {N}/{Total}: {Task Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

2. **Read relevant files** mentioned in the task

3. **Implement the changes** following:
   - Project patterns from loaded skills
   - Tech stack from configuration
   - Existing code conventions

4. **Verify after each task:**
   - Run type check if TypeScript files changed
   - Ensure no obvious errors

5. **Mark task complete:**
```
✅ Task {N} complete: {brief summary of changes}
```

### Step 4: Load Skills Based on Context

As you implement, load relevant skills:

- Creating components → `react-guidelines`
- Adding types → `typescript-standards`
- Styling → `tailwind-patterns`
- Data fetching → `tanstack-query` (if configured)
- Form validation → `zod-validation` (if configured)
- State management → `zustand-state` (if configured)

Print when loading:
```
📚 Loading skill: {skill-name}
```

### Step 5: Run Validation Commands

After all tasks complete, run validation from the plan:

```
═══════════════════════════════════════════════════
           RUNNING VALIDATION
═══════════════════════════════════════════════════
```

Execute each validation command:
- Type checking
- Linting
- Build

If validation fails:
1. Identify the error
2. Fix the issue
3. Re-run validation
4. Continue until all pass

### Step 6: Verify Acceptance Criteria

Check each acceptance criterion from the plan:

```
═══════════════════════════════════════════════════
         ACCEPTANCE CRITERIA CHECK
═══════════════════════════════════════════════════

✅ {Criterion 1} - Verified
✅ {Criterion 2} - Verified
⚠️ {Criterion 3} - Needs manual verification
```

### Step 7: Display Completion Summary

```
═══════════════════════════════════════════════════
         IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════

Plan: {plan name}

Files Created:
  • {path/to/file1.tsx}
  • {path/to/file2.ts}

Files Modified:
  • {path/to/existing1.tsx}
  • {path/to/existing2.ts}

Validation Results:
  ✅ Type Check: Passed
  ✅ Lint: Passed
  ✅ Build: Passed

Acceptance Criteria: {X}/{Y} verified

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. VERIFY (recommended):
   /verify

2. CODE REVIEW:
   /review

3. CREATE COMMIT:
   /utils:commit

4. CREATE PR:
   /utils:pr

═══════════════════════════════════════════════════
```

## Implementation Guidelines

### Follow Existing Patterns

- Check similar components in the codebase
- Match naming conventions
- Use existing utilities and helpers
- Follow the project's code style

### Quality Standards

- No `any` types in TypeScript
- Proper error handling
- Accessibility considerations
- Performance optimization (memoization where needed)

### Code Organization

- One component per file
- Hooks in dedicated files
- Types in dedicated files
- Keep files focused and small

## Error Handling

If implementation encounters errors:

1. **Type errors:** Fix immediately, don't proceed with broken types
2. **Lint errors:** Fix or disable with explanation
3. **Build errors:** Must resolve before completing
4. **Missing dependencies:** Install and document

## Report

Return a summary of:
- Tasks completed
- Files created/modified
- Validation results
- Any manual steps needed

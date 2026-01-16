# Code Review

Review code changes on the current branch for adherence to React best practices, performance optimization, and project guidelines.

## Arguments

- `$ARGUMENTS` - Optional: path to specification file to compare against

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Instructions

### Step 1: Load Skills Based on Config

```
═══════════════════════════════════════════════════
🚀 Invoking [code-reviewer] agent...
   └─ Task: Code Review
   └─ Branch: {current-branch}
═══════════════════════════════════════════════════

📚 Loading skills based on project config:
   └─ react-guidelines (core)
   └─ typescript-standards (core)
   └─ tailwind-patterns (core)
   └─ {additional based on config.techStack}
```

### Step 2: Identify Changes

```bash
# Check for uncommitted changes first
git diff HEAD --name-only

# If no uncommitted changes, check branch changes against main
git diff main...HEAD --name-only
```

Focus on `.tsx`, `.ts`, `.jsx`, `.js` files in the `src/` directory.

### Step 3: Review Each Changed File

For each modified/new file, check against loaded skills:

#### Components (.tsx, .jsx)

- [ ] Uses proper component patterns
- [ ] Lazy loaded if heavy component
- [ ] Uses data fetching patterns from config (TanStack Query, SWR, etc.)
- [ ] No early returns for loading states (if using Suspense)
- [ ] Handles all state scenarios (empty, loading, error)
- [ ] Uses `useCallback` for handlers passed to children
- [ ] Uses `useMemo` for expensive computations
- [ ] Uses import aliases (@/)
- [ ] Styled with Tailwind CSS
- [ ] Proper TypeScript types (no `any`)

#### Data Fetching (based on config.techStack.dataFetching)

If TanStack Query:
- [ ] Uses `useSuspenseQuery` or `useQuery` appropriately
- [ ] Proper query keys
- [ ] Uses mutations for write operations

If SWR:
- [ ] Proper key patterns
- [ ] Handles revalidation

#### Validation (based on config.techStack.validation)

If Zod:
- [ ] Schemas defined for data types
- [ ] Proper validation at boundaries

#### State Management (based on config.techStack.stateManagement)

If Zustand:
- [ ] Uses `useShallow` for object selectors
- [ ] Proper store organization

### Step 4: Add [CR] Comments

For each issue found, add inline comments directly in the code:

**Format:** `// [CR] {severity} {comment}`

Severity levels:
- `🔴 CRITICAL` - Breaks patterns, causes bugs, security/performance issues
- `🟡 IMPORTANT` - Violates guidelines, maintainability concerns
- `🔵 SUGGESTION` - Style, optimization opportunities

**Example:**
```typescript
// [CR] 🔴 CRITICAL: Use useSuspenseQuery for Suspense pattern (see react-guidelines)
const { data, isLoading } = useQuery({...});

// [CR] 🟡 IMPORTANT: Wrap in useCallback - passed to memoized child
const handleClick = () => {...};

// [CR] 🔵 SUGGESTION: Consider extracting to custom hook for reusability
```

### Step 5: Generate Review Summary

Create: `.claude/reviews/code-review-{branch}-{date}.md`

```markdown
# Code Review - {Branch Name}

Date: {YYYY-MM-DD}
Reviewer: frontend-dev-toolkit (code-reviewer)

## Executive Summary

{Brief overview of changes and overall code quality assessment}

## Tech Stack Compliance

| Technology | Expected | Compliance | Notes |
|------------|----------|------------|-------|
| React | ✓ | ✅/❌ | {notes} |
| TypeScript | ✓ | ✅/❌ | {notes} |
| {from config} | ✓ | ✅/❌ | {notes} |

## Issues by Severity

### 🔴 Critical (Must Fix)

- **{file}:{line}**: {description}

### 🟡 Important (Should Fix)

- **{file}:{line}**: {description}

### 🔵 Suggestions (Nice to Have)

- **{file}:{line}**: {description}

## State Handling Review

- Empty states: ✅/❌
- Loading states: ✅/❌
- Error states: ✅/❌

## Positive Observations

{What was done well}

## Next Steps

1. Review all [CR] comments in the code files
2. Address critical issues before merging
3. Consider important improvements
```

### Step 6: Run Validation

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

### Step 7: Display Results

```
═══════════════════════════════════════════════════
           CODE REVIEW COMPLETE
═══════════════════════════════════════════════════

Review summary: {review_file_path}

Issue Summary:
- 🔴 Critical Issues: {count}
- 🟡 Important Improvements: {count}
- 🔵 Minor Suggestions: {count}

[CR] Comments added to:
- {file1} ({count} comments)
- {file2} ({count} comments)

Validation Results:
- TypeScript: {✅/❌}
- ESLint: {✅/❌}
- Build: {✅/❌}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. REVIEW COMMENTS:
   Check [CR] comments in the code files

2. FIX ISSUES (if critical):
   /dev:implement {review_file_path}

3. CLEAN UP COMMENTS (after fixing):
   /utils:clean-comments

4. CREATE PR (if no critical issues):
   /utils:pr

═══════════════════════════════════════════════════
```

## Report

Return:
- Review summary file path
- Issue counts by severity
- Validation results

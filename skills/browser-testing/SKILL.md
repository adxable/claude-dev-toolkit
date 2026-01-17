---
name: browser-testing
description: Visual UI testing using Claude Chrome extension. Provides patterns for visual verification, interaction testing, responsive checks, and automated fix-verify loops.
---

# Browser Testing Skill

Patterns for visual and functional testing using Claude Chrome extension.

## When to Use

- Verifying UI changes render correctly
- Testing interactive components work
- Checking responsive design
- Validating error/loading/empty states
- Creating fix-verify feedback loops

## Prerequisites

1. **Claude Chrome extension** installed and connected
2. **Dev server running:**
   ```bash
   pnpm dev
   # or
   npm run dev
   ```
3. **App accessible** at localhost URL (e.g., http://localhost:5173)

## How Claude Chrome Extension Works

Claude can:
- **See** the browser viewport in real-time
- **Click** buttons, links, and interactive elements
- **Type** text into inputs and forms
- **Scroll** to view different parts of the page
- **Navigate** between pages and routes
- **Observe** changes after interactions

## Core Patterns

### Pattern 1: Visual Verification Loop

```
1. Ask Claude to open browser and navigate to URL
2. Claude views the page
3. Claude analyzes for visual issues
4. If issue found:
   a. Document issue
   b. Fix code
   c. Wait for hot reload (~2s)
   d. Claude views page again
   e. Verify fix
   f. Repeat if more issues
5. Report results
```

### Pattern 2: Component Testing

```
For each component to test:
1. Navigate to component URL or render location
2. Claude verifies initial render state
3. Test each interaction:
   - Claude clicks buttons → verify response
   - Claude fills forms → verify validation
   - Claude triggers modals → verify display
4. Test each state:
   - Loading → spinner/skeleton shows
   - Error → error message displays
   - Empty → empty state renders
   - Success → data displays correctly
```

### Pattern 3: Responsive Testing

```
For each breakpoint:
1. Resize browser window (or use DevTools)
2. Claude views the layout
3. Verify:
   - No horizontal overflow
   - Text readable
   - Touch targets adequate (mobile)
   - Navigation accessible
   - Layout appropriate for size

BREAKPOINTS:
- Mobile: 375px
- Tablet: 768px
- Desktop: 1280px
- Wide: 1920px
```

## Verification Checklists

### Initial Page Load

```markdown
- [ ] No console errors
- [ ] No network failures (4xx/5xx)
- [ ] All images load
- [ ] Fonts render correctly
- [ ] No layout shift after load
```

### Component Render

```markdown
- [ ] Component visible
- [ ] Correct position/size
- [ ] Correct colors/styling
- [ ] Text content correct
- [ ] Icons display
- [ ] No z-index issues
```

### Interaction

```markdown
- [ ] Hover states work
- [ ] Click triggers action
- [ ] Focus states visible
- [ ] Form inputs accept text
- [ ] Validation messages appear
- [ ] Submit works correctly
```

### State Handling

```markdown
- [ ] Loading: spinner/skeleton
- [ ] Error: message + retry option
- [ ] Empty: helpful message
- [ ] Success: data displayed
```

## Issue Documentation

When Claude finds an issue:

```markdown
## Issue: {Brief Title}

**What Claude Sees:** {description of visual problem}
**Location:** {file}:{line}
**Severity:** Critical | Important | Minor

**Expected:** {what should appear}
**Actual:** {what is appearing}

**Root Cause:** {analysis}
**Fix:** {what to change}
```

## Fix-Verify Workflow

```
┌──────────────────────────────────────────────────┐
│              FIX-VERIFY LOOP                      │
│                                                  │
│  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐   │
│  │ View │ -> │Analyze│ -> │ Fix  │ -> │Verify│   │
│  │      │    │      │    │      │    │      │   │
│  └──────┘    └──────┘    └──────┘    └──────┘   │
│      ▲                                    │      │
│      │         (if still broken)          │      │
│      └────────────────────────────────────┘      │
│                                                  │
│  Max iterations: 5                               │
│  Bailout: Report unresolved issues               │
└──────────────────────────────────────────────────┘
```

### Implementation

```
iteration = 0
max_iterations = 5

while iteration < max_iterations:
    claude_views_browser()
    issues = claude_analyzes_what_it_sees()

    if no issues:
        break

    for issue in issues:
        fix_code(issue)
        wait_for_hot_reload()  # ~2 seconds

    iteration++

if iteration == max_iterations:
    report_unresolved_issues()
```

## Common Issues & Fixes

### Layout Issues

| Issue | Common Fix |
|-------|------------|
| Overflow | Add `overflow-hidden` or `overflow-auto` |
| Overlap | Check z-index, position |
| Not visible | Check display, opacity, visibility |
| Wrong size | Check width, height, flex/grid |

### Interaction Issues

| Issue | Common Fix |
|-------|------------|
| Click not working | Check event handler, z-index, pointer-events |
| Form not submitting | Check onSubmit, prevent default |
| Input not updating | Check value + onChange binding |

### State Issues

| Issue | Common Fix |
|-------|------------|
| No loading state | Add isLoading check |
| No error state | Add error boundary or error check |
| Stale data | Check query invalidation |

## Integration with Commands

### With /review --browser

```
/review --browser
  └── Phase 1: Code Review (parallel)
      ├── code-reviewer
      ├── performance-auditor
      └── accessibility-tester
  └── Phase 2: Browser Verification (sequential)
      └── browser-tester
           └── Fix-verify loop if issues found
```

### With /ship --browser

```
/ship "feature" --browser
  └── ... other steps ...
  └── Review step includes browser verification
```

## Best Practices

1. **One fix at a time** - Fix one issue, verify, then move to next
2. **Document what Claude sees** - Describe visual state clearly
3. **Wait for hot reload** - Give HMR time to update (~2s)
4. **Set iteration limit** - Prevent infinite loops (max 5)
5. **Report unresolved** - Document issues that can't be auto-fixed
6. **Test all states** - Don't just test happy path
7. **Check DevTools console** - Look for JS errors, failed requests

## Example Session

```
User: /review --browser

Claude:
  Phase 1: Code Review
  → Running code-reviewer, performance-auditor, accessibility-tester...
  → Code review complete

  Phase 2: Browser Verification
  → Opening Chrome and navigating to http://localhost:5173
  → Viewing login page...
  → Issue found: Submit button overlaps input on mobile
  → Fixing: LoginForm.tsx:45 - adding mt-4 spacing
  → Waiting for hot reload...
  → Viewing again... Fixed!
  → All visual tests passing

  Report: .claude/reviews/review-2024-01-16.md
```

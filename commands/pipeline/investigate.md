# Investigate

Investigate an issue or feature in the browser, then create an implementation/fix plan based on findings.

## Arguments

- `$ARGUMENTS` - URL path and description (e.g., `/dashboard fix chart not loading`)

## Prerequisites

- Claude Chrome extension installed and connected
- Dev server running (or will be started automatically)

## Instructions

This command combines browser investigation with planning. It does NOT implement - only investigates and plans.

### 1. Parse Arguments

Extract from `$ARGUMENTS`:
- **URL path**: The route to investigate (e.g., `/dashboard`, `/users/list`)
- **Description**: What to investigate/fix (everything after the URL)

If no URL provided, ask user for the URL.

### 2. Show Start Banner

```
═══════════════════════════════════════════════════
🔍 Starting Investigation
   └─ URL: http://localhost:5173{url}
   └─ Goal: {description}
═══════════════════════════════════════════════════
```

### 3. Phase 1: Browser Investigation

**IMPORTANT: Use Claude Chrome extension tools (`mcp__claude-in-chrome__*`). Never use Playwright MCP.**

#### 3.1 Ensure Dev Server Running

```bash
# Check if dev server is running on common ports
lsof -i :5173 || lsof -i :3000 || npm run dev &
```

#### 3.2 Get Browser Context

Use `mcp__claude-in-chrome__tabs_context_mcp` to get available tabs:
- If no tab group exists, create one with `createIfEmpty: true`
- Create a new tab with `mcp__claude-in-chrome__tabs_create_mcp`

#### 3.3 Navigate to Application

Use `mcp__claude-in-chrome__navigate` to navigate to the URL.

#### 3.4 Investigation Mode (Read-Only)

**DO NOT FIX anything during investigation. Only observe and document.**

Use Chrome extension tools to observe:

```
OBSERVE:
□ Current visual state (take screenshot)
□ Console errors/warnings (read_console_messages)
□ Network requests (read_network_requests)
□ Component behavior
□ Interaction issues
□ Performance problems (slow renders, duplicate API calls)

DOCUMENT:
□ What works correctly
□ What is broken/missing
□ Steps to reproduce issues
□ Related components/files (if identifiable)
```

#### 3.5 Capture Evidence

Take screenshots and document:
- Initial page load state
- After key interactions
- Console errors
- Network activity

#### 3.6 Create Findings Report

```markdown
## Investigation Findings

**URL:** {url}
**Date:** {date}
**Goal:** {description}

### Current State

{Description of what Claude observes in the browser}

### Screenshots

- Initial load: [screenshot taken]
- After interaction: [screenshot taken]

### Issues Found

| # | Issue | Severity | Observation |
|---|-------|----------|-------------|
| 1 | {issue} | Critical/High/Medium/Low | {what Claude sees} |

### Console Output

- Errors: {list any errors}
- Warnings: {list any warnings}

### Network Activity

- API calls observed: {list}
- Duplicates: {yes/no, details}
- Failures: {any 4xx/5xx}

### Reproduction Steps

1. Navigate to {url}
2. {action}
3. Observe: {result}

### Related Files (if identifiable)

- {file path} - {why it's relevant}
```

### 4. Phase 2: Create Plan

After browser investigation, use the `planner` agent approach:

```
═══════════════════════════════════════════════════
📋 Phase 2: Create Implementation Plan
   └─ Input: Investigation findings
═══════════════════════════════════════════════════
```

#### 4.1 Research Codebase

Using the investigation findings, research the codebase:
- Find files related to the observed issues
- Identify components shown in screenshots
- Locate API calls and data fetching logic
- Find similar patterns for reference

#### 4.2 Create Plan File

Create a plan file at `.claude/plans/plan-{type}-{descriptive-name}.md`:

```markdown
# Plan: {Title based on investigation}

**Type:** Bug / Feature / Patch
**Created:** {date}
**Status:** Draft
**Source:** Browser Investigation

## Goal

{What we're trying to achieve - specific and measurable}

## Investigation Summary

### Observed Issues

{Summary from browser investigation}

### Screenshots

{Reference screenshots taken}

### Console/Network Findings

{Any errors or API issues observed}

## Root Cause Analysis

**Cause:** {technical explanation based on codebase research}
**Location:** `{file:line}` (if identifiable)

## Research Findings

{From codebase exploration:}
- Similar patterns found at: {locations}
- Architecture observations
- Relevant files identified

## Approach

{High-level approach to fixing the observed issues}

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| path/to/file | Create/Modify | Why |

## Implementation Steps

### Step 1: {Action}

- {Detail}
- {Detail}

### Step 2: {Action}

- {Detail}
- {Detail}

### Final Step: Verification

- Run `/verify {url}` to confirm fix
- Verify issue no longer reproducible

## Acceptance Criteria

- [ ] Issue #{N} resolved: {description}
- [ ] No console errors
- [ ] No network failures
- [ ] Type check passes
- [ ] Lint passes
- [ ] Build passes
```

### 5. Show Completion Banner

```
═══════════════════════════════════════════════════
        ✅ INVESTIGATION COMPLETE
═══════════════════════════════════════════════════

## Phase 1: Browser Investigation
✓ URL visited: {url}
✓ Screenshots taken: {N}
✓ Issues documented: {N}

## Phase 2: Plan Created
📄 Plan saved to: .claude/plans/{plan_file}
📋 Type: {Bug|Feature|Patch}
📊 Steps: {N}
📁 Files: {N}

═══════════════════════════════════════════════════
              INVESTIGATION SUMMARY
═══════════════════════════════════════════════════

Issues Found:
{list of issues from findings}

Root Cause:
{from plan analysis}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. Review the plan:
   cat .claude/plans/{plan_file}

2. When ready, implement:
   /implement .claude/plans/{plan_file}

═══════════════════════════════════════════════════
```

## Chrome Extension Tools Reference

| Tool | Purpose |
|------|---------|
| `tabs_context_mcp` | Get/create tab context |
| `tabs_create_mcp` | Create new tab |
| `navigate` | Go to URL |
| `computer` (screenshot) | View page state |
| `read_page` | Get DOM accessibility tree |
| `find` | Find elements by description |
| `read_console_messages` | Check for errors |
| `read_network_requests` | Monitor API calls |

## Usage Examples

```bash
# Investigate a specific bug
/investigate /dashboard fix chart not loading

# Investigate UI behavior
/investigate /users/list modal not closing after save

# Investigate performance issue
/investigate /products slow loading and double API calls

# Investigate missing feature
/investigate /orders add bulk delete functionality

# Investigate visual issue
/investigate /settings layout broken on mobile
```

## Comparison with Other Commands

| Command | When to Use | Browser? | Fixes Code? | Creates Plan? |
|---------|-------------|----------|-------------|---------------|
| `/investigate` | Discover issues visually before coding | Yes (observe only) | No | Yes |
| `/plan` | Plan from description alone | No | No | Yes |
| `/verify` | Validate after implementation | Yes (fix loop) | Yes | No |

## Workflow Position

```
/investigate → /implement → /refactor → /verify → /review → /commit → /pr
       ↑
   YOU ARE HERE
   (combines browser discovery + planning)

Alternative flow (no browser):
/plan → /implement → /refactor → /verify → /review → /commit → /pr
```

## Rules

- **Investigation is read-only** - DO NOT fix code during Phase 1
- **Document everything** - Screenshots, console, network
- **Be thorough** - Check all related functionality
- **Plan follows findings** - The plan should directly address observed issues
- **Max 10 screenshots** - Keep evidence focused
- **Ask if unclear** - If you can't reproduce or understand the issue, ask the user

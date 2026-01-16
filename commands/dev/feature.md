# Feature Planning

Create a comprehensive plan for implementing a new feature. This command creates a plan document only - it does NOT implement any code.

## Arguments

- `$ARGUMENTS` - Feature description (text) or path to prompt file

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json` to determine:
- Tech stack (which skills to load)
- Project paths
- Package manager
- Validation commands

## Critical Rules

**This command creates a PLAN only. You MUST NOT implement any changes.**

### Forbidden Actions
- DO NOT edit any source files (only create the plan file)
- DO NOT implement the feature
- DO NOT modify any code
- DO NOT run implementation commands

### Required Actions
- Research and analyze the feature requirements
- Design the architecture and component structure
- Create the plan file in the specs directory
- Display the "PLAN CREATED SUCCESSFULLY" message
- Suggest running `/dev:implement {plan_path}` for implementation

## Instructions

### Step 1: Load Configuration

Read `.claude/frontend-dev-toolkit.json` to get project settings:

```javascript
const config = JSON.parse(fs.readFileSync('.claude/frontend-dev-toolkit.json'));
const specsPath = config.paths.specs || '.claude/specs';
const srcPath = config.paths.src || 'src';
```

### Step 2: Load Relevant Skills

Based on `config.techStack`, load the appropriate skills:

**Always load:**
- `react-guidelines`
- `typescript-standards`
- `tailwind-patterns`

**Conditionally load:**
- `tanstack-query` if dataFetching === 'tanstack-query'
- `zod-validation` if validation === 'zod'
- `zustand-state` if stateManagement === 'zustand'
- `react-router` if routing === 'react-router'

Print:
```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Feature Planning
   └─ Tech Stack: {list from config}
═══════════════════════════════════════════════════

📚 Loading skills:
   └─ react-guidelines (core)
   └─ typescript-standards (core)
   └─ {additional skills based on config}
```

### Step 3: Parse Input

**If $ARGUMENTS is a file path (ends with .md or starts with ./):**
- Read the file and extract feature information
- Look for XML tags: `<objective>`, `<user_story>`, `<requirements>`

**If $ARGUMENTS is text:**
- Use it directly as the feature description

### Step 4: Research Codebase

Before planning, explore the codebase:

1. Read project README if exists
2. Check existing patterns in `{srcPath}/features/` or `{srcPath}/components/`
3. Identify similar implementations for reference
4. Note any relevant utilities or hooks

### Step 5: Create Plan Document

Create the plan file at `{specsPath}/feature-{descriptive-name}.md`:

```markdown
# Feature: {Feature Name}

## Metadata

- **Type:** Feature
- **Created:** {YYYY-MM-DD}
- **Status:** Planning
- **Tech Stack:** {from config}

## Feature Description

{Detailed description of the feature, its purpose, and value to users}

## User Story

As a {type of user}
I want to {action/goal}
So that {benefit/value}

## Problem Statement

{What problem does this feature solve?}

## Solution Statement

{How will this feature solve the problem?}

## Architecture Design

### Component Hierarchy

```
{FeatureName}/
├── {FeatureName}View.tsx          # Main view component
├── components/
│   ├── {FeatureName}Header.tsx    # Header with actions
│   ├── {FeatureName}Content.tsx   # Main content area
│   └── {FeatureName}Modals.tsx    # Modal components
├── hooks/
│   └── use{FeatureName}.ts        # Feature-specific hooks
├── api/
│   ├── schema.ts                  # Zod schemas (if using)
│   ├── queries.ts                 # Query definitions (if using TanStack Query)
│   └── mutations.ts               # Mutation definitions
└── types/
    └── index.ts                   # TypeScript types
```

### State Management

| State | Location | Subscribers | Re-render Scope |
|-------|----------|-------------|-----------------|
| {state name} | {location} | {components} | {scope} |

### Data Flow

{Describe how data flows through the feature}

## Relevant Files

### Existing Files to Reference
- {path/to/file} - {why it's relevant}

### New Files to Create
- {path/to/new/file} - {purpose}

## Implementation Plan

### Phase 1: Foundation
{Setup and foundational work}

### Phase 2: Core Implementation
{Main feature implementation}

### Phase 3: Integration
{Connecting with existing code}

## Step by Step Tasks

### 1. Setup Feature Structure
- Create feature directory at `{srcPath}/features/{feature-name}/`
- Create subdirectories: `api/`, `components/`, `hooks/`, `types/`

### 2. Define Types and Schemas
- Create TypeScript interfaces in `types/index.ts`
- Create Zod schemas in `api/schema.ts` (if using Zod)

### 3. Implement API Layer
- Create query definitions in `api/queries.ts`
- Create mutation definitions in `api/mutations.ts`

### 4. Build Components
- Create main view component
- Create child components with proper memoization
- Add loading and error states

### 5. Add Routing (if applicable)
- Add route in router configuration
- Create lazy-loaded route component

### 6. Validate Implementation
- Run type checking
- Run linting
- Run build
- Manual testing

## Testing Strategy

### Unit Tests
- {Component/hook} should {behavior}

### Integration Tests
- {Feature} should {end-to-end behavior}

### Edge Cases
- {Edge case description}

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Validation Commands

Execute these commands to validate the implementation:

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Notes

{Additional considerations, future improvements, technical debt}
```

### Step 6: Display Success Message

```
═══════════════════════════════════════════════════
            PLAN CREATED SUCCESSFULLY
═══════════════════════════════════════════════════

Plan saved to: {plan_file_path}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this feature plan, run:

  /dev:implement {plan_file_path}

This will execute the step-by-step tasks from your plan.

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the plan file created.

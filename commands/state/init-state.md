# /adx:init-state

Initialize state tracking for a project interactively.

## Trigger

User runs `/adx:init-state` to set up project tracking.

## Behavior

### Step 1: Project Vision

Ask the user:
```
Let's set up project tracking.

**What is this project?**
Describe in 1-2 sentences what you're building and why.
```

Update `PROJECT.md` with their response.

### Step 2: Tech Stack

Ask or detect:
```
**What's your tech stack?**
(I can detect from package.json if available)

- Frontend: [detected or ask]
- Backend: [detected or ask]
- Database: [ask]
```

### Step 3: Define Phases

Ask:
```
**What are the main phases of work?**
List 3-6 phases to complete this project.

Example:
1. Project setup and auth
2. Core data models
3. Main features
4. Polish and testing
```

Create `ROADMAP.md` with their phases.

### Step 4: Scope v1 Requirements

Ask:
```
**What must be in v1 (MVP)?**
List the core features needed for initial release.
```

Update `REQUIREMENTS.md` with v1 scope.

### Step 5: Set Current Position

Ask:
```
**Where are you now?**
- Which phase are you starting/continuing?
- Any work already done?
```

Initialize `STATE.md` with current position.

### Step 6: Confirm

```
State tracking initialized!

Created:
- .claude/state/PROJECT.md
- .claude/state/STATE.md
- .claude/state/ROADMAP.md
- .claude/state/REQUIREMENTS.md

**Current Position:** Phase 1 - [Name]

Commands available:
- `/adx:progress` - Check current status
- `/adx:pause` - Save before ending session
- `/adx:resume` - Continue from last session

Ready to start working?
```

## Quick Mode

If user provides context upfront:
```
/adx:init-state "Building a task manager app with React and Supabase"
```

Use the description to:
1. Auto-fill PROJECT.md vision
2. Detect/suggest tech stack
3. Propose reasonable phases
4. Ask only for confirmation

## For Existing Projects

If state files already exist:
```
State tracking already initialized.

Current position: Phase 2 - User Authentication

Options:
1. View current state (`/adx:progress`)
2. Reset and reinitialize (will overwrite existing state)
3. Cancel
```

## Example Interaction

```
User: /adx:init-state

Claude: Let's set up project tracking.

**What is this project?**
Describe in 1-2 sentences what you're building and why.

User: A recipe sharing app where users can save, organize, and share their favorite recipes

Claude: Got it! I'll set that as your project vision.

**What's your tech stack?**
I detected from package.json:
- Frontend: Next.js 14 with App Router
- Styling: Tailwind + shadcn/ui

What about:
- Database: [Supabase / PostgreSQL / MongoDB / Other]
- Auth: [Supabase Auth / NextAuth / Clerk / Other]

User: Supabase for both

Claude: Perfect. Now let's define your phases.

**What are the main phases of work?**
Based on your project, I suggest:

1. Setup & Auth - Project config, Supabase setup, user auth
2. Recipe CRUD - Create, read, update, delete recipes
3. Organization - Collections, tags, search
4. Social - Sharing, comments, likes
5. Polish - Performance, mobile, testing

Does this look right, or would you like to adjust?

User: Looks good, let's go with that

Claude: **What must be in v1 (MVP)?**

User: Basic auth, recipe CRUD, and simple search

Claude: **Where are you starting?**

User: Phase 1, haven't started yet

Claude: State tracking initialized!

Created:
- .claude/state/PROJECT.md
- .claude/state/STATE.md
- .claude/state/ROADMAP.md
- .claude/state/REQUIREMENTS.md

**Current Position:** Phase 1 - Setup & Auth

Ready to start working on Phase 1?
```

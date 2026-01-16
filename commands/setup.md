# Project Setup

Interactive setup command that configures the frontend-dev-toolkit for your project. This command detects your tech stack and creates a configuration file.

## Purpose

Set up the frontend-dev-toolkit for a new project by:
1. Detecting existing technologies from package.json
2. Asking about your tech stack preferences
3. Configuring project paths
4. Creating the configuration file

## Instructions

### Step 1: Detect Project Structure

First, analyze the project to detect existing technologies:

```bash
# Check if package.json exists
cat package.json 2>/dev/null || echo "No package.json found"

# Check for common config files
ls -la tsconfig.json tailwind.config.* vite.config.* next.config.* 2>/dev/null || true
```

Parse package.json to detect:
- **React**: `react` in dependencies
- **TypeScript**: `typescript` in devDependencies
- **Tailwind CSS**: `tailwindcss` in devDependencies
- **TanStack Query**: `@tanstack/react-query` in dependencies
- **React Router**: `react-router` or `react-router-dom` in dependencies
- **TanStack Router**: `@tanstack/react-router` in dependencies
- **Zod**: `zod` in dependencies
- **Zustand**: `zustand` in dependencies
- **AG Grid**: `ag-grid-react` in dependencies
- **shadcn/ui**: Check for `components.json` file

Detect package manager:
- Check for `pnpm-lock.yaml` → pnpm
- Check for `yarn.lock` → yarn
- Check for `bun.lockb` → bun
- Default to npm

### Step 2: Display Detection Results

Show the user what was detected:

```
═══════════════════════════════════════════════════
       FRONTEND DEV TOOLKIT - PROJECT SETUP
═══════════════════════════════════════════════════

Analyzing your project...

📦 Package Manager: {detected or "npm (default)"}

✅ Detected Technologies:
   • React {version}
   • TypeScript {version}
   • Tailwind CSS {version}
   • TanStack Query {version}
   • (list all detected)

❓ Not Detected (may need to configure):
   • Zod
   • Zustand
   • (list not found)

═══════════════════════════════════════════════════
```

### Step 3: Ask Configuration Questions

Use the AskUserQuestion tool to confirm and expand configuration:

**Question 1: Core Technologies**
```
Which core technologies does your project use?
(Pre-select based on detection)

☑️ React (Recommended - detected)
☑️ TypeScript (Recommended - detected)
☑️ Tailwind CSS (Recommended - detected)
```

**Question 2: Data Fetching**
```
How do you handle data fetching?

○ TanStack Query (React Query) - Recommended
○ SWR
○ RTK Query
○ Custom/fetch
```

**Question 3: Routing**
```
Which routing solution do you use?

○ React Router v7 (Recommended)
○ TanStack Router
○ Next.js App Router
○ Other/None
```

**Question 4: Validation**
```
Do you use schema validation?

○ Zod (Recommended)
○ Yup
○ Joi
○ None
```

**Question 5: State Management**
```
How do you manage global client state?

○ Zustand (Recommended)
○ Redux/RTK
○ Jotai
○ Context only
○ None
```

**Question 6: UI Components**
```
Which UI component library do you use?

○ shadcn/ui (Recommended)
○ MUI
○ Chakra UI
○ Ant Design
○ Custom/None
```

**Question 7: Project Paths**
```
Confirm your project paths:

Source directory: src (default)
Components: src/components
Features: src/features
Specs output: .claude/specs
```

### Step 4: Create Configuration File

Based on answers, create `.claude/frontend-dev-toolkit.json`:

```json
{
  "version": "1.0.0",
  "techStack": {
    "core": ["react", "typescript", "tailwind"],
    "dataFetching": "tanstack-query",
    "routing": "react-router",
    "validation": "zod",
    "stateManagement": "zustand",
    "uiLibrary": "shadcn"
  },
  "paths": {
    "src": "src",
    "components": "src/components",
    "features": "src/features",
    "specs": ".claude/specs",
    "reviews": ".claude/reviews"
  },
  "packageManager": "pnpm",
  "commands": {
    "typeCheck": "pnpm tsc --noEmit",
    "lint": "pnpm eslint src/",
    "build": "pnpm build",
    "test": "pnpm test"
  }
}
```

### Step 5: Create Required Directories

```bash
mkdir -p .claude/specs
mkdir -p .claude/reviews
```

### Step 6: Display Summary

```
═══════════════════════════════════════════════════
           SETUP COMPLETE!
═══════════════════════════════════════════════════

Configuration saved to: .claude/frontend-dev-toolkit.json

Your Tech Stack:
├── Core: React, TypeScript, Tailwind CSS
├── Data Fetching: TanStack Query
├── Routing: React Router
├── Validation: Zod
├── State: Zustand
└── UI: shadcn/ui

Package Manager: pnpm

Loaded Skills:
├── react-guidelines (core)
├── typescript-standards (core)
├── tailwind-patterns (core)
├── tanstack-query (optional)
├── zod-validation (optional)
└── zustand-state (optional)

═══════════════════════════════════════════════════
                GETTING STARTED
═══════════════════════════════════════════════════

Available commands:

  PLANNING:
    /dev:feature <description>  - Plan a new feature
    /dev:bug <description>      - Plan a bug fix
    /dev:chore <description>    - Plan maintenance work

  IMPLEMENTATION:
    /dev:implement <plan-path>  - Execute a plan

  VERIFICATION:
    /verify                     - Full verification loop
    /verify:types               - Type checking only
    /verify:lint                - Linting only

  CODE REVIEW:
    /review                     - Review branch changes
    /review:performance         - Performance review

  UTILITIES:
    /utils:commit               - Generate git commit
    /utils:pr                   - Create pull request

═══════════════════════════════════════════════════

Try running: /dev:feature Add user authentication
```

## Configuration Options Reference

### techStack.core
Always-enabled technologies:
- `react` - React library
- `typescript` - TypeScript language
- `tailwind` - Tailwind CSS

### techStack.dataFetching
- `tanstack-query` - TanStack Query (React Query)
- `swr` - SWR
- `rtk-query` - Redux Toolkit Query
- `custom` - Custom solution

### techStack.routing
- `react-router` - React Router v7
- `tanstack-router` - TanStack Router
- `next-router` - Next.js routing
- `none` - No routing

### techStack.validation
- `zod` - Zod schema validation
- `yup` - Yup validation
- `joi` - Joi validation
- `none` - No validation library

### techStack.stateManagement
- `zustand` - Zustand
- `redux` - Redux/RTK
- `jotai` - Jotai
- `context` - React Context only
- `none` - No global state

### techStack.uiLibrary
- `shadcn` - shadcn/ui
- `mui` - Material UI
- `chakra` - Chakra UI
- `antd` - Ant Design
- `custom` - Custom components

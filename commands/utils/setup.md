# Setup

Configure development standards for your project. Detects your stack and creates configuration files.

## Arguments

- `$ARGUMENTS` - Optional: "quick" for defaults, or specific skill name

## Instructions

### 1. Detect Existing Stack

First, read `package.json` and detect the installed stack:

```bash
cat package.json
```

Identify:
- State management: zustand, redux, jotai, mobx
- Server state: @tanstack/react-query, swr
- Forms: react-hook-form, formik
- Styling: tailwindcss, styled-components, emotion
- UI library: @radix-ui/*, @mui/*, @chakra-ui/*
- Framework: next, remix, or router (tanstack-router, react-router)

Output detected stack:

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 DETECTED STACK                                          │
├─────────────────────────────────────────────────────────────┤
│  State:        zustand                                      │
│  Server State: @tanstack/react-query                        │
│  Forms:        react-hook-form + zod                        │
│  Styling:      tailwindcss + class-variance-authority       │
│  UI:           @radix-ui/* (shadcn/ui)                      │
│  Framework:    Next.js 14                                   │
└─────────────────────────────────────────────────────────────┘
```

### 2. Ask Configuration Questions

#### Question 1: Confirm Stack

```
Header: "Stack"
Question: "Is this stack detection correct?"
Options:
  - label: "Yes, continue"
    description: "Use detected stack for guidelines"
  - label: "I'm adding new libraries"
    description: "I'll tell you what I'm planning to add"
```

#### Question 2: Project Type

```
Header: "Project"
Question: "What type of project is this?"
Options:
  - label: "Product/Application"
    description: "Long-lived, maintainability matters"
  - label: "Prototype/MVP"
    description: "Speed matters, some shortcuts OK"
  - label: "Library"
    description: "API stability critical"
```

#### Question 3: Team Size

```
Header: "Team"
Question: "Team size?"
Options:
  - label: "Solo"
    description: "Less documentation needed"
  - label: "Small (2-5)"
    description: "Moderate conventions"
  - label: "Large (6+)"
    description: "Strict conventions essential"
```

#### Question 4: Strictness

```
Header: "Strictness"
Question: "How strict should enforcement be?"
Options:
  - label: "Strict (Recommended)"
    description: "Flag all deviations"
  - label: "Moderate"
    description: "Critical only, warn on others"
  - label: "Relaxed"
    description: "Suggestions only"
```

### 3. Create Configuration Files

Create `.claude/config/` directory and config files:

```bash
mkdir -p .claude/config
```

#### 3.1 Code Quality Config

Write `.claude/config/code-quality.json`:

```json
{
  "projectType": "{detected}",
  "teamSize": "{answered}",
  "strictness": "{answered}",
  "abstractionRule": "rule-of-three",
  "principles": {
    "singleResponsibility": true,
    "dependencyInversion": true,
    "noGodClasses": true
  },
  "tooling": {
    "eslint": true,
    "typescript": true
  }
}
```

#### 3.2 Project Structure Config

Write `.claude/config/project-structure.json`:

```json
{
  "detected": {
    "framework": "{from package.json}",
    "organization": "{detected from folder structure}",
    "naming": "{detected from existing files}"
  },
  "enforced": {
    "organization": "{detected or feature-based}",
    "naming": "{detected}",
    "colocation": true
  },
  "boundaries": {
    "noFeatureCrossImports": true
  }
}
```

#### 3.3 Frontend Guidelines Config

Write `.claude/config/frontend-guidelines.json`:

```json
{
  "detected": {
    "state": "{from package.json}",
    "serverState": "{from package.json}",
    "forms": "{from package.json}",
    "styling": "{from package.json}",
    "ui": "{from package.json}"
  },
  "strictness": "{answered}",
  "rules": {
    "useShallow": "{if zustand}",
    "queryOptionsFactory": "{if tanstack-query}",
    "zodResolver": "{if react-hook-form+zod}",
    "cnHelper": "{if tailwind}"
  }
}
```

### 4. Check/Suggest Tooling

Based on config, check if ESLint rules exist and suggest additions:

```
[setup] Checking tooling configuration...

[setup] ESLint: Found .eslintrc.js
[setup] Recommended rules to add:
  • max-lines: ['warn', { max: 300 }]
  • complexity: ['warn', 10]
  • @typescript-eslint/no-explicit-any: 'error'

[setup] TypeScript: Found tsconfig.json
[setup] ✓ strict: true (good)
[setup] ⚠ Consider adding: noImplicitReturns: true
```

### 5. Output Summary

```
┌─────────────────────────────────────────────────────────────┐
│  ✅ SETUP COMPLETE                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Configuration saved to .claude/config/                     │
│                                                             │
│  Active Rules (based on your stack):                        │
│  • ZUSTAND: useShallow for object selectors                 │
│  • TANSTACK QUERY: queryOptions() factory pattern           │
│  • TAILWIND: cn() helper for conditional classes            │
│  • STRUCTURE: Feature-based organization                    │
│                                                             │
│  These rules load automatically via dev_standards_loader    │
│  hook when you run implementation commands.                 │
│                                                             │
│  Commands that use these standards:                         │
│  • /adx:plan - Structure recommendations                    │
│  • /adx:implement - Applies stack patterns                  │
│  • /refactor - Enforces conventions (optional)              │
│  • /adx:review - Validates against config                   │
│                                                             │
│  To reconfigure: /adx:setup                                 │
│  To view config: cat .claude/config/*.json                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Setup Mode

If `$ARGUMENTS` is "quick", skip questions and use:
- Detected stack from package.json
- Strict enforcement
- Rule of three for abstraction
- Feature-based structure (if not detected)

```
> /adx:setup quick

[setup] Quick setup mode - using detected stack and recommended defaults
[setup] ✓ Created .claude/config/code-quality.json
[setup] ✓ Created .claude/config/project-structure.json
[setup] ✓ Created .claude/config/frontend-guidelines.json
[setup] Done! Standards will load automatically.
```

---

## Workflow Position

```
/setup → /plan → /implement → /verify → /review → /commit → /pr
   ↑
   RUN ONCE at project start (or when stack changes)
```

## How It Works

1. **Setup** creates config files in `.claude/config/`
2. **dev_standards_loader.py** hook reads configs on each prompt
3. **Stack-specific rules** are injected into context
4. **Skills** (code-quality, project-structure, frontend-guidelines) provide detailed guidance when needed

The hook only shows relevant rules for your detected stack - no assumptions about libraries you don't use.

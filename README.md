# Frontend Dev Toolkit

A comprehensive Claude Code plugin for React/TypeScript frontend development workflows.

## Features

- **Planning Commands** - Structured feature, bug, and chore planning
- **Implementation Commands** - Guided implementation from plans
- **Verification Commands** - Parallel type checking, linting, and build verification
- **Code Review Commands** - Automated code review with inline comments
- **Utility Commands** - Git commit, PR creation, and project utilities

## Installation

```bash
# In Claude Code, run:
/plugin install /path/to/frontend-dev-toolkit

# Or add to your project's .claude/settings.json:
{
  "plugins": ["/path/to/frontend-dev-toolkit"]
}
```

## Quick Start

After installation, run the setup command to configure your project:

```bash
/frontend-dev-toolkit:setup
```

This will ask about your tech stack and create a configuration file.

## Commands

### Setup & Configuration

| Command | Description |
|---------|-------------|
| `/frontend-dev-toolkit:setup` | Interactive project setup - configures tech stack and paths |
| `/frontend-dev-toolkit:config` | View/edit current configuration |

### Development Workflow

| Command | Description |
|---------|-------------|
| `/dev:feature <description>` | Create a feature implementation plan |
| `/dev:bug <description>` | Create a bug fix plan |
| `/dev:chore <description>` | Create a maintenance/refactoring plan |
| `/dev:implement <plan-path>` | Implement a plan step-by-step |
| `/dev:refactor <file-or-description>` | Guided code refactoring |

### Verification

| Command | Description |
|---------|-------------|
| `/verify` | Run full verification loop (types, lint, build) |
| `/verify:types` | Run TypeScript type checking |
| `/verify:lint` | Run ESLint |
| `/verify:build` | Run build command |

### Code Review

| Command | Description |
|---------|-------------|
| `/review` | Full code review of branch changes |
| `/review:performance` | Performance-focused review |

### Utilities

| Command | Description |
|---------|-------------|
| `/utils:commit` | Generate and create git commit |
| `/utils:pr` | Create pull request with description |
| `/utils:clean-comments` | Remove [CR] review comments |

## Tech Stack Support

### Core (Always Enabled)
- React
- TypeScript
- Tailwind CSS

### Optional (Configure During Setup)
- TanStack Query (React Query)
- React Router / TanStack Router
- Zod (validation)
- Zustand (state management)
- AG Grid
- shadcn/ui

## Skills

The plugin includes specialized skills that provide context-aware guidance:

### Core Skills
- `react-guidelines` - React best practices and patterns
- `typescript-standards` - TypeScript conventions
- `tailwind-patterns` - Tailwind CSS patterns

### Optional Skills (loaded based on config)
- `tanstack-query` - Data fetching patterns
- `zod-validation` - Schema validation patterns
- `zustand-state` - State management patterns
- `react-router` - Routing patterns

## Agents

Specialized agents for different tasks:

- `code-reviewer` - Reviews code and adds [CR] comments
- `frontend-architect` - Designs component architecture
- `react-developer` - Implements React features
- `typescript-expert` - Resolves type issues

## Configuration File

After setup, your project will have `.claude/frontend-dev-toolkit.json`:

```json
{
  "techStack": {
    "core": ["react", "typescript", "tailwind"],
    "optional": ["tanstack-query", "zod", "zustand"]
  },
  "paths": {
    "src": "src",
    "components": "src/components",
    "features": "src/features",
    "specs": ".claude/specs"
  },
  "packageManager": "pnpm"
}
```

## Directory Structure

```
frontend-dev-toolkit/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── commands/
│   ├── setup.md              # Project setup command
│   ├── dev/                  # Development commands
│   │   ├── feature.md
│   │   ├── bug.md
│   │   ├── chore.md
│   │   ├── implement.md
│   │   └── refactor.md
│   ├── verify/               # Verification commands
│   │   ├── verify.md
│   │   ├── types.md
│   │   ├── lint.md
│   │   └── build.md
│   ├── review/               # Code review commands
│   │   ├── review.md
│   │   └── performance.md
│   └── utils/                # Utility commands
│       ├── commit.md
│       ├── pr.md
│       └── clean-comments.md
├── skills/
│   ├── core/                 # Always-loaded skills
│   │   ├── react-guidelines/
│   │   ├── typescript-standards/
│   │   └── tailwind-patterns/
│   └── optional/             # Conditionally-loaded skills
│       ├── tanstack-query/
│       ├── zod-validation/
│       └── zustand-state/
├── agents/
│   ├── code-reviewer.md
│   ├── frontend-architect.md
│   └── react-developer.md
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## License

MIT

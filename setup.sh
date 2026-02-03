#!/bin/bash

# ADX Toolkit Interactive Setup
# https://github.com/adxable/adx-toolkit

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
PROJECT_DIR=""
ROUTER="tanstack"
STATE_MANAGER="zustand"
INSTALL_HOOKS="yes"
INSTALL_MCP="no"
INSTALL_MEMORY="yes"
INSTALL_STATE="no"
SELECTED_AGENTS=()

# Print banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║     █████╗ ██████╗ ██╗  ██╗    ████████╗ ██████╗  ██████╗ ║"
    echo "║    ██╔══██╗██╔══██╗╚██╗██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗║"
    echo "║    ███████║██║  ██║ ╚███╔╝        ██║   ██║   ██║██║   ██║║"
    echo "║    ██╔══██║██║  ██║ ██╔██╗        ██║   ██║   ██║██║   ██║║"
    echo "║    ██║  ██║██████╔╝██╔╝ ██╗       ██║   ╚██████╔╝╚██████╔╝║"
    echo "║    ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ║"
    echo "║                                                           ║"
    echo "║           Autonomous Frontend Development Toolkit         ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# Print section header
section() {
    echo ""
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Print success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print info message
info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Print warning message
warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Ask yes/no question
ask_yes_no() {
    local prompt="$1"
    local default="$2"
    local result

    if [ "$default" = "yes" ]; then
        prompt="$prompt [Y/n]: "
    else
        prompt="$prompt [y/N]: "
    fi

    read -p "$prompt" result
    result=${result:-$default}

    case "$result" in
        [Yy]|[Yy][Ee][Ss]) echo "yes" ;;
        *) echo "no" ;;
    esac
}

# Ask for selection from options
ask_select() {
    local prompt="$1"
    shift
    local options=("$@")
    local selection

    echo -e "${BOLD}$prompt${NC}"
    echo ""

    for i in "${!options[@]}"; do
        echo "  $((i+1))) ${options[$i]}"
    done
    echo ""

    while true; do
        read -p "Enter number (1-${#options[@]}): " selection
        if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le "${#options[@]}" ]; then
            echo "${options[$((selection-1))]}"
            return
        fi
        echo -e "${RED}Invalid selection. Please try again.${NC}"
    done
}

# Ask for multi-select from options
ask_multi_select() {
    local prompt="$1"
    shift
    local options=("$@")
    local selections

    echo -e "${BOLD}$prompt${NC}"
    echo -e "${CYAN}(Enter numbers separated by spaces, or 'all' for all options)${NC}"
    echo ""

    for i in "${!options[@]}"; do
        echo "  $((i+1))) ${options[$i]}"
    done
    echo ""

    read -p "Enter selections: " selections

    if [ "$selections" = "all" ]; then
        echo "${options[@]}"
        return
    fi

    local result=()
    for sel in $selections; do
        if [[ "$sel" =~ ^[0-9]+$ ]] && [ "$sel" -ge 1 ] && [ "$sel" -le "${#options[@]}" ]; then
            result+=("${options[$((sel-1))]}")
        fi
    done

    echo "${result[@]}"
}

# Step 1: Project Directory
ask_project_dir() {
    section "Step 1/5: Project Directory"

    echo "Where would you like to configure ADX Toolkit?"
    echo ""
    echo "  1) Current directory ($(pwd))"
    echo "  2) Specify a different directory"
    echo ""

    read -p "Enter choice (1-2): " choice

    case "$choice" in
        1) PROJECT_DIR="$(pwd)" ;;
        2)
            read -p "Enter project path: " PROJECT_DIR
            PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"
            ;;
        *) PROJECT_DIR="$(pwd)" ;;
    esac

    # Validate directory
    if [ ! -d "$PROJECT_DIR" ]; then
        warn "Directory does not exist. Create it?"
        if [ "$(ask_yes_no "" "yes")" = "yes" ]; then
            mkdir -p "$PROJECT_DIR"
            success "Created $PROJECT_DIR"
        else
            echo "Aborting."
            exit 1
        fi
    fi

    success "Project directory: $PROJECT_DIR"
}

# Step 2: Tech Stack
ask_tech_stack() {
    section "Step 2/5: Tech Stack"

    echo -e "${BOLD}Router:${NC}"
    echo "  1) TanStack Router (Recommended)"
    echo "  2) React Router v7"
    echo "  3) Next.js App Router"
    echo ""
    read -p "Enter choice (1-3) [1]: " choice
    case "${choice:-1}" in
        1) ROUTER="tanstack" ;;
        2) ROUTER="react-router" ;;
        3) ROUTER="nextjs" ;;
    esac
    success "Router: $ROUTER"
    echo ""

    echo -e "${BOLD}State Management:${NC}"
    echo "  1) Zustand (Recommended)"
    echo "  2) Jotai"
    echo "  3) Redux Toolkit"
    echo "  4) None / React Context only"
    echo ""
    read -p "Enter choice (1-4) [1]: " choice
    case "${choice:-1}" in
        1) STATE_MANAGER="zustand" ;;
        2) STATE_MANAGER="jotai" ;;
        3) STATE_MANAGER="redux" ;;
        4) STATE_MANAGER="context" ;;
    esac
    success "State manager: $STATE_MANAGER"
}

# Step 3: Features
ask_features() {
    section "Step 3/5: Features"

    echo -e "${BOLD}Which features would you like to install?${NC}"
    echo ""

    # Hooks
    echo -e "${CYAN}Hooks${NC} - Smart context detection, session summaries, logging"
    INSTALL_HOOKS=$(ask_yes_no "  Install hooks?" "yes")
    [ "$INSTALL_HOOKS" = "yes" ] && success "Hooks: enabled" || info "Hooks: disabled"
    echo ""

    # MCP Servers
    echo -e "${CYAN}MCP Servers${NC} - Sequential thinking, Playwright, filesystem, etc."
    INSTALL_MCP=$(ask_yes_no "  Install MCP configuration?" "no")
    [ "$INSTALL_MCP" = "yes" ] && success "MCP: enabled" || info "MCP: disabled"
    echo ""

    # Memory System
    echo -e "${CYAN}Memory System${NC} - Persistent context (decisions, conventions, lessons)"
    INSTALL_MEMORY=$(ask_yes_no "  Install memory system?" "yes")
    [ "$INSTALL_MEMORY" = "yes" ] && success "Memory: enabled" || info "Memory: disabled"
    echo ""

    # State Tracking
    echo -e "${CYAN}State Tracking${NC} - Progress tracking with phases, roadmap, and session handoffs"
    INSTALL_STATE=$(ask_yes_no "  Install state tracking?" "no")
    [ "$INSTALL_STATE" = "yes" ] && success "State: enabled" || info "State: disabled"
}

# Step 4: Agents
ask_agents() {
    section "Step 4/5: Agents"

    echo "Select which agents to enable:"
    echo ""
    echo -e "${CYAN}Core Agents (used by /adx:ship):${NC}"
    echo "  1) explorer          - Fast codebase search"
    echo "  2) verifier          - Type check, lint, build, test"
    echo "  3) code-reviewer     - Code review with reports"
    echo "  4) security-auditor  - Scan for vulnerabilities"
    echo "  5) performance-auditor - Bundle and runtime analysis"
    echo "  6) browser-tester    - Visual UI testing"
    echo "  7) git-automator     - Smart commits and PRs"
    echo "  8) web-researcher    - Debug with internet research"
    echo ""
    echo -e "${CYAN}Standalone Agents:${NC}"
    echo "  9) planner           - Create detailed plans"
    echo "  10) implementer      - Execute plans step-by-step"
    echo "  11) refactorer       - Code cleanup, remove any types"
    echo "  12) pattern-researcher - Research new patterns online"
    echo ""
    echo -e "${CYAN}Optional Agents:${NC}"
    echo "  13) accessibility-tester - WCAG compliance"
    echo "  14) docs-generator   - README, JSDoc generation"
    echo ""

    read -p "Enter numbers separated by spaces (or 'all') [1-8]: " selections
    selections=${selections:-"1 2 3 4 5 6 7 8"}

    if [ "$selections" = "all" ]; then
        SELECTED_AGENTS=("explorer" "verifier" "code-reviewer" "security-auditor" "performance-auditor" "browser-tester" "git-automator" "web-researcher" "planner" "implementer" "refactorer" "pattern-researcher" "accessibility-tester" "docs-generator")
    else
        SELECTED_AGENTS=()
        for sel in $selections; do
            case "$sel" in
                1) SELECTED_AGENTS+=("explorer") ;;
                2) SELECTED_AGENTS+=("verifier") ;;
                3) SELECTED_AGENTS+=("code-reviewer") ;;
                4) SELECTED_AGENTS+=("security-auditor") ;;
                5) SELECTED_AGENTS+=("performance-auditor") ;;
                6) SELECTED_AGENTS+=("browser-tester") ;;
                7) SELECTED_AGENTS+=("git-automator") ;;
                8) SELECTED_AGENTS+=("web-researcher") ;;
                9) SELECTED_AGENTS+=("planner") ;;
                10) SELECTED_AGENTS+=("implementer") ;;
                11) SELECTED_AGENTS+=("refactorer") ;;
                12) SELECTED_AGENTS+=("pattern-researcher") ;;
                13) SELECTED_AGENTS+=("accessibility-tester") ;;
                14) SELECTED_AGENTS+=("docs-generator") ;;
            esac
        done
    fi

    success "Selected agents: ${SELECTED_AGENTS[*]}"
}

# Step 5: Confirmation
confirm_setup() {
    section "Step 5/5: Confirmation"

    echo -e "${BOLD}Setup Summary:${NC}"
    echo ""
    echo "  Project:     $PROJECT_DIR"
    echo "  Router:      $ROUTER"
    echo "  State:       $STATE_MANAGER"
    echo "  Hooks:       $INSTALL_HOOKS"
    echo "  MCP:         $INSTALL_MCP"
    echo "  Memory:      $INSTALL_MEMORY"
    echo "  State:       $INSTALL_STATE"
    echo "  Agents:      ${SELECTED_AGENTS[*]}"
    echo ""

    if [ "$(ask_yes_no "Proceed with installation?" "yes")" != "yes" ]; then
        echo "Aborting."
        exit 0
    fi
}

# Generate CLAUDE.md based on selections
generate_claude_md() {
    local output="$PROJECT_DIR/CLAUDE.md"

    # Router-specific content
    local router_line=""
    case "$ROUTER" in
        tanstack) router_line="| Router | TanStack Router | Type-safe, file-based routing |" ;;
        react-router) router_line="| Router | React Router v7 | Framework mode with loaders |" ;;
        nextjs) router_line="| Router | Next.js App Router | Server components, file-based |" ;;
    esac

    # State-specific content
    local state_line=""
    local state_pattern=""
    case "$STATE_MANAGER" in
        zustand)
            state_line="| State | Zustand | UI state only, NOT server state |"
            state_pattern='### Zustand - ALWAYS use useShallow

```typescript
// GOOD
import { useShallow } from '\''zustand/shallow'\'';

const { filters, setFilter } = useFiltersStore(
  useShallow((state) => ({
    filters: state.filters,
    setFilter: state.setFilter,
  }))
);

// BAD - causes infinite re-render loop
const { filters, setFilter } = useFiltersStore((state) => ({
  filters: state.filters,
  setFilter: state.setFilter,
}));
```'
            ;;
        jotai)
            state_line="| State | Jotai | Atomic state management |"
            state_pattern='### Jotai - Atomic State

```typescript
import { atom, useAtom } from '\''jotai'\'';

// Define atoms
const countAtom = atom(0);
const doubleAtom = atom((get) => get(countAtom) * 2);

// Usage
const [count, setCount] = useAtom(countAtom);
```'
            ;;
        redux)
            state_line="| State | Redux Toolkit | Global state with slices |"
            state_pattern='### Redux Toolkit - createSlice Pattern

```typescript
import { createSlice, PayloadAction } from '\''@reduxjs/toolkit'\'';

const userSlice = createSlice({
  name: '\''user'\'',
  initialState: { name: '\'''\'' },
  reducers: {
    setName: (state, action: PayloadAction<string>) => {
      state.name = action.payload;
    },
  },
});
```'
            ;;
        context)
            state_line="| State | React Context | Built-in context API |"
            state_pattern='### React Context - Provider Pattern

```typescript
const ThemeContext = createContext<Theme | null>(null);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('\''useTheme must be within ThemeProvider'\'');
  return context;
};
```'
            ;;
    esac

    cat > "$output" << EOF
# Frontend Development Conventions

## Tech Stack

| Category | Choice | Notes |
|----------|--------|-------|
$router_line
$state_line
| Server State | TanStack Query | \`useSuspenseQuery\` with Suspense boundaries |
| Forms | React Hook Form + Zod | Always use \`zodResolver\` |
| Styling | Tailwind + shadcn/ui | \`cn()\` from \`@/lib/utils\` |
| Validation | Zod | Schema-first, \`z.infer<>\` for types |

---

## Project Structure (Feature-based)

\`\`\`
src/
├── features/
│   └── users/
│       ├── components/
│       │   ├── UserList.tsx
│       │   └── UserCard.tsx
│       ├── hooks/
│       │   └── useUsers.ts
│       ├── api/
│       │   ├── queries.ts      # TanStack Query options
│       │   └── mutations.ts
│       ├── stores/
│       │   └── userFiltersStore.ts
│       ├── schemas/
│       │   └── userSchema.ts   # Zod schemas
│       └── index.ts            # Public exports
├── components/                  # Shared/global components
├── hooks/                       # Shared hooks
├── lib/
│   └── utils.ts                # cn() helper
└── types/                       # Global types
\`\`\`

---

## Enforced Patterns

$state_pattern

### TanStack Query - Query Options Factory

\`\`\`typescript
// features/users/api/queries.ts
import { queryOptions } from '@tanstack/react-query';

export const userQueries = {
  all: () => queryOptions({
    queryKey: ['users'],
    queryFn: fetchUsers,
  }),
  detail: (id: string) => queryOptions({
    queryKey: ['users', id],
    queryFn: () => fetchUser(id),
  }),
  list: (filters: UserFilters) => queryOptions({
    queryKey: ['users', 'list', filters],
    queryFn: () => fetchUsers(filters),
  }),
};

// Usage
const { data } = useSuspenseQuery(userQueries.detail(userId));
\`\`\`

### Forms - React Hook Form + Zod

\`\`\`typescript
const schema = z.object({
  name: z.string().min(1, 'Required'),
  email: z.string().email(),
});

type FormData = z.infer<typeof schema>;

const form = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { name: '', email: '' },
});
\`\`\`

### Tailwind - cn() for conditional classes

\`\`\`typescript
import { cn } from '@/lib/utils';

<div className={cn(
  'rounded-lg p-4',
  isActive && 'bg-primary text-primary-foreground',
  disabled && 'opacity-50 pointer-events-none'
)} />
\`\`\`

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Components | PascalCase | \`UserCard.tsx\` |
| Hooks | camelCase, \`use\` prefix | \`useUsers.ts\` |
| Stores | camelCase, \`Store\` suffix | \`userFiltersStore.ts\` |
| Schemas | camelCase, \`Schema\` suffix | \`userSchema.ts\` |
| Query keys | \`['entity', 'action', params]\` | \`['users', 'list', { page: 1 }]\` |

---

## Exports

\`\`\`typescript
// GOOD - named exports
export const UserCard = () => { ... };
export const useUsers = () => { ... };

// BAD - default exports (harder to refactor)
export default UserCard;
\`\`\`

---

## Performance - Required

1. **useMemo** for filter/sort/map operations
2. **useCallback** for functions passed to children
3. **React.memo** for components in lists
4. **Suspense boundary** at layout level, not per-route

---

## Anti-patterns - NEVER

| Don't | Why | Instead |
|-------|-----|---------|
| Inline functions in JSX for memo children | New reference = re-render | \`useCallback\` |
| \`any\` in TypeScript | No type safety | \`unknown\` + type guard |
| Index as key in lists | Breaks reconciliation | Stable unique ID |
| State in URL + useState | Duplication | URL only (useSearchParams) |
EOF

    success "Generated CLAUDE.md"
}

# Install files to project
install_files() {
    section "Installing Files"

    # Create .claude directory structure
    mkdir -p "$PROJECT_DIR/.claude"
    mkdir -p "$PROJECT_DIR/.claude/plans"
    mkdir -p "$PROJECT_DIR/.claude/reviews"
    mkdir -p "$PROJECT_DIR/.claude/checkpoints"

    # Generate CLAUDE.md
    generate_claude_md

    # Copy settings.json to project root (not .claude/)
    cp "$SCRIPT_DIR/settings.json" "$PROJECT_DIR/settings.json"
    success "Copied settings.json"

    # Install hooks
    if [ "$INSTALL_HOOKS" = "yes" ]; then
        mkdir -p "$PROJECT_DIR/hooks"
        mkdir -p "$PROJECT_DIR/hooks/utils"
        mkdir -p "$PROJECT_DIR/hooks/utils/llm"
        # Copy hook files
        cp -r "$SCRIPT_DIR/hooks/"*.py "$PROJECT_DIR/hooks/" 2>/dev/null || true
        cp -r "$SCRIPT_DIR/hooks/utils/"*.py "$PROJECT_DIR/hooks/utils/" 2>/dev/null || true
        cp -r "$SCRIPT_DIR/hooks/utils/llm/"*.py "$PROJECT_DIR/hooks/utils/llm/" 2>/dev/null || true
        # Copy README
        [ -f "$SCRIPT_DIR/hooks/README.md" ] && cp "$SCRIPT_DIR/hooks/README.md" "$PROJECT_DIR/hooks/" 2>/dev/null || true
        # Copy __init__.py files
        touch "$PROJECT_DIR/hooks/utils/__init__.py"
        touch "$PROJECT_DIR/hooks/utils/llm/__init__.py"
        success "Installed hooks"
    fi

    # Install MCP config
    if [ "$INSTALL_MCP" = "yes" ]; then
        cp "$SCRIPT_DIR/mcp.json" "$PROJECT_DIR/.claude/mcp.json"
        success "Installed MCP configuration"
    fi

    # Install memory system
    if [ "$INSTALL_MEMORY" = "yes" ]; then
        mkdir -p "$PROJECT_DIR/memory"
        mkdir -p "$PROJECT_DIR/memory/knowledge/fragments"
        mkdir -p "$PROJECT_DIR/memory/local/fragments"
        # Copy memory template files if they exist
        [ -f "$SCRIPT_DIR/memory/decisions.md" ] && cp "$SCRIPT_DIR/memory/decisions.md" "$PROJECT_DIR/memory/" 2>/dev/null || true
        [ -f "$SCRIPT_DIR/memory/lessons.md" ] && cp "$SCRIPT_DIR/memory/lessons.md" "$PROJECT_DIR/memory/" 2>/dev/null || true
        [ -f "$SCRIPT_DIR/memory/conventions.md" ] && cp "$SCRIPT_DIR/memory/conventions.md" "$PROJECT_DIR/memory/" 2>/dev/null || true
        # Create index files if not present
        [ ! -f "$PROJECT_DIR/memory/knowledge/index.json" ] && echo '{}' > "$PROJECT_DIR/memory/knowledge/index.json"
        [ ! -f "$PROJECT_DIR/memory/local/index.json" ] && echo '{}' > "$PROJECT_DIR/memory/local/index.json"
        success "Installed memory system"
    fi

    # Install state tracking
    if [ "$INSTALL_STATE" = "yes" ]; then
        mkdir -p "$PROJECT_DIR/.claude/state"
        # Create template state files
        cat > "$PROJECT_DIR/.claude/state/PROJECT.md" << 'STATEEOF'
# Project Overview

## Vision
[Describe what you're building]

## Tech Stack
- Framework:
- Styling:
- State:
- API:

## Key Decisions
-
STATEEOF
        cat > "$PROJECT_DIR/.claude/state/STATE.md" << 'STATEEOF'
# Current State

## Active Phase
Phase 1: Setup

## Current Task
[What you're working on]

## Blockers
None

## Recent Decisions
-
STATEEOF
        cat > "$PROJECT_DIR/.claude/state/ROADMAP.md" << 'STATEEOF'
# Project Roadmap

## Phase 1: Foundation
- [ ] Project setup
- [ ] Core architecture

## Phase 2: Features
- [ ] Feature 1
- [ ] Feature 2

## Phase 3: Polish
- [ ] Testing
- [ ] Documentation
STATEEOF
        success "Installed state tracking templates"
        info "  Run /adx:init-state to configure your project"
    fi

    # Update .gitignore
    update_gitignore
}

# Update .gitignore with ADX entries
update_gitignore() {
    local gitignore="$PROJECT_DIR/.gitignore"

    # Create if doesn't exist
    [ ! -f "$gitignore" ] && touch "$gitignore"

    # Entries to add
    local entries=(
        "# ADX Toolkit - Personal (don't share)"
        ".claude/"
        "memory/local/"
        "logs/"
        ""
        "# Python"
        "__pycache__/"
        "*.pyc"
    )

    # Check and add each entry
    for entry in "${entries[@]}"; do
        if [ -n "$entry" ] && ! grep -qF "$entry" "$gitignore" 2>/dev/null; then
            echo "$entry" >> "$gitignore"
        fi
    done

    success "Updated .gitignore"
}

# Print completion message
print_completion() {
    section "Setup Complete!"

    echo -e "${GREEN}ADX Toolkit has been configured for your project.${NC}"
    echo ""
    echo -e "${BOLD}Files created:${NC}"
    echo "  $PROJECT_DIR/CLAUDE.md"
    echo "  $PROJECT_DIR/settings.json"
    [ "$INSTALL_HOOKS" = "yes" ] && echo "  $PROJECT_DIR/hooks/"
    [ "$INSTALL_MCP" = "yes" ] && echo "  $PROJECT_DIR/.claude/mcp.json"
    [ "$INSTALL_MEMORY" = "yes" ] && echo "  $PROJECT_DIR/memory/"
    [ "$INSTALL_STATE" = "yes" ] && echo "  $PROJECT_DIR/.claude/state/"
    echo "  $PROJECT_DIR/.claude/plans/"
    echo "  $PROJECT_DIR/.claude/reviews/"
    echo ""
    echo -e "${BOLD}Next steps:${NC}"
    echo ""
    echo "  1. Review and customize CLAUDE.md for your project"
    echo ""
    echo "  2. Start using ADX commands:"
    echo -e "     ${CYAN}/adx:ship \"add user auth\"${NC}       - Full autonomous workflow"
    echo -e "     ${CYAN}/adx:plan \"feature\"${NC}            - Create implementation plan"
    echo -e "     ${CYAN}/adx:investigate /url \"bug\"${NC}    - Browser investigation + plan"
    echo -e "     ${CYAN}/adx:verify${NC}                     - Type check, lint, build, test"
    echo -e "     ${CYAN}/adx:review --browser${NC}           - Code review + visual testing"
    echo ""
    echo "  3. Pipeline flow:"
    echo -e "     ${CYAN}PLAN → IMPLEMENT → VERIFY → REVIEW → COMMIT → PR${NC}"
    echo ""
    echo "  4. Read the docs: https://github.com/adxable/adx-toolkit"
    echo ""
    echo -e "${BOLD}${GREEN}Happy coding!${NC}"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    # Check if Claude Code is installed
    if ! command -v claude &> /dev/null; then
        echo -e "${RED}Error: Claude Code CLI not found.${NC}"
        echo ""
        echo "Please install Claude Code first:"
        echo "  npm install -g @anthropic-ai/claude-code"
        echo ""
        exit 1
    fi

    # Check if uv is installed (for hooks)
    if ! command -v uv &> /dev/null; then
        warn "uv not found. Hooks require uv for execution."
        echo ""
        echo "Install uv: https://github.com/astral-sh/uv"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo ""
        if [ "$(ask_yes_no "Continue without uv?" "no")" != "yes" ]; then
            exit 1
        fi
    fi
}

# Main
main() {
    print_banner

    echo "Welcome to ADX Toolkit project setup!"
    echo ""
    echo "This wizard configures ADX for a specific project:"
    echo "  • CLAUDE.md with your tech stack conventions"
    echo "  • Hooks for smart context injection"
    echo "  • Memory system for persistent knowledge"
    echo "  • State tracking for session continuity"
    echo ""
    echo -e "${CYAN}Note: This is project setup. For plugin installation, run:${NC}"
    echo -e "  ${BOLD}bash <(curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install-adx.sh)${NC}"
    echo ""
    echo -e "Press ${BOLD}Enter${NC} to continue or ${BOLD}Ctrl+C${NC} to cancel."
    read

    check_prerequisites
    ask_project_dir
    ask_tech_stack
    ask_features
    ask_agents
    confirm_setup
    install_files
    print_completion
}

main "$@"

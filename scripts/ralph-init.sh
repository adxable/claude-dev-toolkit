#!/bin/bash

# ralph-init.sh - Initialize a RALPH project with frontend-dev-toolkit templates
# Usage: ralph-init.sh "feature description" [--browser]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory (where templates are)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$PLUGIN_DIR/templates/ralph"

# Parse arguments
FEATURE_DESC=""
BROWSER_FLAG=""
BROWSER_CRITERIA=""
BROWSER_TASKS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --browser)
            BROWSER_FLAG="--browser"
            BROWSER_CRITERIA="- [ ] Browser verification passing (visual + interactions)"
            BROWSER_TASKS="- [ ] Run browser verification (\`/review --browser\`)
- [ ] Fix any visual issues
- [ ] Verify interactions work"
            shift
            ;;
        *)
            if [[ -z "$FEATURE_DESC" ]]; then
                FEATURE_DESC="$1"
            fi
            shift
            ;;
    esac
done

# Validate
if [[ -z "$FEATURE_DESC" ]]; then
    echo -e "${RED}Error: Feature description required${NC}"
    echo "Usage: ralph-init.sh \"feature description\" [--browser]"
    exit 1
fi

# Check if RALPH is installed
if ! command -v ralph &> /dev/null; then
    echo -e "${YELLOW}Warning: RALPH not installed globally${NC}"
    echo "Install RALPH first:"
    echo "  git clone https://github.com/frankbria/ralph-claude-code.git"
    echo "  cd ralph-claude-code && ./install.sh"
    echo ""
    echo "Continuing with project setup..."
fi

# Generate project name from feature description
PROJECT_NAME=$(echo "$FEATURE_DESC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-30)
FEATURE_SLUG=$(echo "$FEATURE_DESC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

# Create project directory
PROJECT_DIR=".ralph-projects/$PROJECT_NAME"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  RALPH Project Initialization${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Feature: ${YELLOW}$FEATURE_DESC${NC}"
echo -e "Project: ${YELLOW}$PROJECT_DIR${NC}"
echo -e "Browser: ${YELLOW}${BROWSER_FLAG:-disabled}${NC}"
echo ""

# Create directories
mkdir -p "$PROJECT_DIR"/{specs,src,logs}

# Copy and process PROMPT.md template
echo -e "${BLUE}Creating PROMPT.md...${NC}"
sed -e "s/{{FEATURE_NAME}}/$FEATURE_DESC/g" \
    -e "s/{{FEATURE_DESCRIPTION}}/$FEATURE_DESC/g" \
    -e "s/{{BROWSER_FLAG}}/$BROWSER_FLAG/g" \
    -e "s/{{BROWSER_CRITERIA}}/$BROWSER_CRITERIA/g" \
    "$TEMPLATES_DIR/PROMPT.md" > "$PROJECT_DIR/PROMPT.md"

# Copy and process @fix_plan.md template
echo -e "${BLUE}Creating @fix_plan.md...${NC}"
sed -e "s/{{FEATURE_NAME}}/$FEATURE_DESC/g" \
    -e "s/{{feature}}/$FEATURE_SLUG/g" \
    -e "s/{{BROWSER_TASKS}}/$BROWSER_TASKS/g" \
    "$TEMPLATES_DIR/@fix_plan.md" > "$PROJECT_DIR/@fix_plan.md"

# Create .ralph directory for state
mkdir -p "$PROJECT_DIR/.ralph"

# Create initial specs file
cat > "$PROJECT_DIR/specs/requirements.md" << EOF
# Requirements: $FEATURE_DESC

## Overview
$FEATURE_DESC

## Functional Requirements
- TBD (Claude will analyze and fill in)

## Technical Requirements
- Follow CLAUDE.md conventions
- Use project tech stack (Zustand, TanStack Query, etc.)
- TypeScript with no \`any\` types

## Acceptance Criteria
- Feature works as described
- Code passes type check and lint
- PR created with description
EOF

# Initialize git if not exists
if [[ ! -d "$PROJECT_DIR/.git" ]]; then
    echo -e "${BLUE}Initializing git...${NC}"
    (cd "$PROJECT_DIR" && git init -q)
fi

# Summary
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✓ RALPH Project Created${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Project structure:"
echo -e "  ${YELLOW}$PROJECT_DIR/${NC}"
echo -e "  ├── PROMPT.md          # Main instructions for Claude"
echo -e "  ├── @fix_plan.md       # Task tracking"
echo -e "  ├── specs/"
echo -e "  │   └── requirements.md"
echo -e "  ├── src/               # Implementation (empty)"
echo -e "  ├── logs/              # Execution logs"
echo -e "  └── .ralph/            # RALPH state"
echo ""
echo -e "To start autonomous development:"
echo -e "  ${BLUE}cd $PROJECT_DIR${NC}"
echo -e "  ${BLUE}ralph --monitor${NC}"
echo ""
echo -e "Or with timeout:"
echo -e "  ${BLUE}ralph --monitor --timeout 60${NC}"
echo ""

#!/bin/bash

# ADX Toolkit Git Installer (Alternative to plugin marketplace)
# Usage: curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install.sh | bash
#
# This installs ADX via git clone. For plugin marketplace install, use:
#   bash <(curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install-adx.sh)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

REPO_URL="https://github.com/adxable/adx-toolkit.git"
PLUGIN_DIR="$HOME/.claude/plugins/adx-toolkit"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           ADX Toolkit Git Installer                       ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check for git
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is required but not installed.${NC}"
    exit 1
fi

# Check if already installed
if [ -d "$PLUGIN_DIR" ]; then
    echo -e "${YELLOW}ADX Toolkit is already installed at $PLUGIN_DIR${NC}"
    echo ""
    read -p "Update? [Y/n]: " choice
    choice=${choice:-Y}

    if [[ "$choice" =~ ^[Yy] ]]; then
        echo -e "${CYAN}Updating...${NC}"
        cd "$PLUGIN_DIR" && git pull origin main
        echo -e "${GREEN}✓ Updated${NC}"
    else
        echo "Aborting."
        exit 0
    fi
else
    # Create plugins directory
    mkdir -p "$HOME/.claude/plugins"

    # Clone repository
    echo -e "${CYAN}Cloning ADX Toolkit...${NC}"
    git clone "$REPO_URL" "$PLUGIN_DIR"
    echo -e "${GREEN}✓ Cloned to $PLUGIN_DIR${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ ADX Toolkit installed!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BOLD}Next Steps:${NC}"
echo ""
echo "1. Configure a project (creates hooks, memory, CLAUDE.md):"
echo -e "   ${CYAN}cd /path/to/your/project${NC}"
echo -e "   ${CYAN}$PLUGIN_DIR/setup.sh${NC}"
echo ""
echo "2. Or run setup.sh from any project directory"
echo ""
echo -e "${BOLD}Available Commands (after project setup):${NC}"
echo -e "  ${CYAN}/adx:ship \"task\"${NC}       Full autonomous workflow"
echo -e "  ${CYAN}/adx:plan \"feature\"${NC}   Research and create plan"
echo -e "  ${CYAN}/adx:implement${NC}        Execute from plan"
echo -e "  ${CYAN}/adx:verify${NC}           Type check, lint, build, test"
echo -e "  ${CYAN}/adx:review${NC}           Comprehensive code review"
echo ""
echo -e "Docs: ${CYAN}https://github.com/adxable/adx-toolkit${NC}"
echo ""

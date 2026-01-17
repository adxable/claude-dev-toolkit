#!/bin/bash

# ADX Toolkit Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install.sh | bash

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
echo -e "${CYAN}║              ADX Toolkit Installer                        ║${NC}"
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
    read -p "Update and reconfigure? [Y/n]: " choice
    choice=${choice:-Y}

    if [[ "$choice" =~ ^[Yy] ]]; then
        echo -e "${CYAN}Updating...${NC}"
        cd "$PLUGIN_DIR" && git pull origin main
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
fi

echo -e "${GREEN}✓ Plugin installed at $PLUGIN_DIR${NC}"
echo ""

# Ask about running setup
echo -e "${BOLD}Would you like to configure ADX for a project now?${NC}"
read -p "[Y/n]: " run_setup
run_setup=${run_setup:-Y}

if [[ "$run_setup" =~ ^[Yy] ]]; then
    exec "$PLUGIN_DIR/setup.sh"
else
    echo ""
    echo -e "${GREEN}Installation complete!${NC}"
    echo ""
    echo "To configure a project later, run:"
    echo -e "  ${CYAN}$PLUGIN_DIR/setup.sh${NC}"
    echo ""
    echo "Or navigate to your project and run:"
    echo -e "  ${CYAN}~/.claude/plugins/adx-toolkit/setup.sh${NC}"
    echo ""
fi

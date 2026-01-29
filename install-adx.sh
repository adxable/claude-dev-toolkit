#!/bin/bash
#
# ADX Plugin Installer for Claude Code
# https://github.com/adxable/adx-toolkit
#
# Usage:
#   bash <(curl -fsSL https://raw.githubusercontent.com/adxable/adx-toolkit/main/install-adx.sh)
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║     █████╗ ██████╗ ██╗  ██╗                               ║"
echo "║    ██╔══██╗██╔══██╗╚██╗██╔╝    Plugin Installer           ║"
echo "║    ███████║██║  ██║ ╚███╔╝     for Claude Code            ║"
echo "║    ██╔══██║██║  ██║ ██╔██╗                                ║"
echo "║    ██║  ██║██████╔╝██╔╝ ██╗    v2.0.0                     ║"
echo "║    ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝                               ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: Claude Code CLI not found.${NC}"
    echo ""
    echo "Please install Claude Code first:"
    echo "  npm install -g @anthropic-ai/claude-code"
    echo ""
    exit 1
fi

echo -e "${BOLD}Installing ADX Plugin...${NC}"
echo ""

# Step 1: Add the marketplace
echo -e "${CYAN}[1/2]${NC} Adding ADX marketplace..."
if claude plugin marketplace add adxable/adx-toolkit 2>/dev/null; then
    echo -e "${GREEN}  ✓ Marketplace added${NC}"
else
    echo -e "${YELLOW}  ⚠ Marketplace may already exist (continuing...)${NC}"
fi

# Step 2: Install the plugin
echo -e "${CYAN}[2/2]${NC} Installing ADX plugin..."
if claude plugin install adx@adx-marketplace; then
    echo -e "${GREEN}  ✓ Plugin installed${NC}"
else
    echo -e "${RED}  ✗ Failed to install plugin${NC}"
    echo ""
    echo "Try installing manually:"
    echo "  1. Run: /plugin"
    echo "  2. Go to Marketplaces tab"
    echo "  3. Add: adxable/adx-toolkit"
    echo "  4. Go to Browse tab"
    echo "  5. Install: adx"
    exit 1
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ ADX Plugin installed successfully!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BOLD}Available Commands:${NC}"
echo ""
echo -e "  ${CYAN}/adx:ship${NC}      Single-pass automation workflow"
echo -e "  ${CYAN}/adx:plan${NC}      Research and plan a feature"
echo -e "  ${CYAN}/adx:implement${NC} Execute implementation from plan"
echo -e "  ${CYAN}/adx:review${NC}    Comprehensive code review"
echo -e "  ${CYAN}/adx:verify${NC}    Run type check, lint, and build"
echo -e "  ${CYAN}/adx:commit${NC}    Smart commit with conventional format"
echo -e "  ${CYAN}/adx:pr${NC}        Create pull request"
echo ""
echo -e "${BOLD}Quick Start:${NC}"
echo ""
echo -e "  ${YELLOW}/adx:ship \"add user authentication with JWT\"${NC}"
echo ""
echo -e "For more info: ${CYAN}https://github.com/adxable/adx-toolkit${NC}"
echo ""

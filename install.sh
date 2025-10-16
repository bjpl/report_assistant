#!/bin/bash
# Report Assistant - Installation Script
# Sets up all commands and integrations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Report Assistant - Installation${NC}"
echo "=================================="
echo

# Step 1: Check dependencies
echo -e "${BLUE}[1/7]${NC} Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 not found. Please install Python 3.${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}⚠️  npm not found. Please install Node.js and npm.${NC}"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠️  git not found. Please install git.${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} All required dependencies found"

# Step 2: Create directories
echo -e "${BLUE}[2/7]${NC} Creating directory structure..."
mkdir -p "$SCRIPT_DIR/daily_reports"
mkdir -p "$SCRIPT_DIR/daily_dev_startup_reports"
mkdir -p "$SCRIPT_DIR/docs/templates"
mkdir -p "$SCRIPT_DIR/backups"
mkdir -p "$SCRIPT_DIR/scripts/report_management"
echo -e "${GREEN}✓${NC} Directories created"

# Step 3: Make scripts executable
echo -e "${BLUE}[3/7]${NC} Setting executable permissions..."
chmod +x "$SCRIPT_DIR/report" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/scripts/report_management/report_cli.py" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/install.sh" 2>/dev/null || true
echo -e "${GREEN}✓${NC} Permissions set"

# Step 4: Install Python dependencies
echo -e "${BLUE}[4/7]${NC} Installing Python dependencies..."
if [[ -f "$SCRIPT_DIR/requirements.txt" ]]; then
    pip install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Some Python packages may need manual installation${NC}"
    }
else
    # Create basic requirements.txt if missing
    cat > "$SCRIPT_DIR/requirements.txt" << EOF
# Report Assistant Requirements
pathlib2>=2.3.0
gitpython>=3.1.0
pyyaml>=5.4.0
click>=8.0.0
rich>=10.0.0
EOF
    pip install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || true
fi
echo -e "${GREEN}✓${NC} Python dependencies installed"

# Step 5: Install Node dependencies
echo -e "${BLUE}[5/7]${NC} Installing Node dependencies..."
if [[ -f "$SCRIPT_DIR/package.json" ]]; then
    cd "$SCRIPT_DIR" && npm install --silent 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Some Node packages may need manual installation${NC}"
    }
fi

# Install claude-flow globally if not present
if ! command -v claude-flow &> /dev/null; then
    echo "  Installing claude-flow globally..."
    npm install -g claude-flow@alpha --silent 2>/dev/null || {
        echo -e "${YELLOW}⚠️  claude-flow may need manual installation: npm install -g claude-flow@alpha${NC}"
    }
fi
echo -e "${GREEN}✓${NC} Node dependencies installed"

# Step 6: Setup shell integration
echo -e "${BLUE}[6/7]${NC} Setting up shell integration..."

# Detect shell
SHELL_RC=""
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [[ -n "$SHELL_RC" ]]; then
    # Check if already added
    if ! grep -q "report_aliases.sh" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# Report Assistant" >> "$SHELL_RC"
        echo "source $SCRIPT_DIR/report_aliases.sh" >> "$SHELL_RC"
        echo -e "${GREEN}✓${NC} Added to $SHELL_RC"
    else
        echo -e "${GREEN}✓${NC} Already in $SHELL_RC"
    fi

    # Add to PATH if needed
    if ! echo "$PATH" | grep -q "$SCRIPT_DIR"; then
        echo "export PATH=\"\$PATH:$SCRIPT_DIR\"" >> "$SHELL_RC"
        echo -e "${GREEN}✓${NC} Added to PATH"
    fi
else
    echo -e "${YELLOW}⚠️  Could not detect shell RC file${NC}"
    echo "  Add this line to your shell configuration:"
    echo "  source $SCRIPT_DIR/report_aliases.sh"
fi

# Step 7: Create symlinks for global access
echo -e "${BLUE}[7/7]${NC} Creating command symlinks..."

# Try to create symlinks in common locations
for bindir in /usr/local/bin $HOME/.local/bin $HOME/bin; do
    if [[ -d "$bindir" ]] && [[ -w "$bindir" ]]; then
        ln -sf "$SCRIPT_DIR/report" "$bindir/report" 2>/dev/null && {
            echo -e "${GREEN}✓${NC} Symlinked 'report' to $bindir"
            break
        }
    fi
done

ln -sf "$SCRIPT_DIR/scripts/report_management/report_cli.py" "$bindir/report-cli" 2>/dev/null || true

# Final setup
echo
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}✓ Report Assistant Installation Complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo

echo "Available commands:"
echo "  ${BLUE}make help${NC}         - Show all make commands"
echo "  ${BLUE}./report help${NC}     - Show CLI commands"
echo "  ${BLUE}npm run${NC}          - Show npm scripts"
echo

echo "Quick start:"
echo "  ${BLUE}make today${NC}        - Generate today's reports"
echo "  ${BLUE}report status${NC}     - Check current status"
echo "  ${BLUE}make audit${NC}        - Audit all projects"
echo

echo "Shell aliases (after reloading shell):"
echo "  ${BLUE}rt${NC}                - Report today"
echo "  ${BLUE}rg${NC}                - Report GMS"
echo "  ${BLUE}rp${NC}                - Report progress"
echo "  ${BLUE}rhelp${NC}             - Show all aliases"
echo

echo -e "${YELLOW}⚠️  Reload your shell or run:${NC}"
echo "  source $SCRIPT_DIR/report_aliases.sh"
echo

echo "For full documentation, see:"
echo "  $SCRIPT_DIR/QUICK_REFERENCE.md"
echo

# Optional: Run initial audit
read -p "Run initial audit? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running audit..."
    cd "$SCRIPT_DIR" && make audit
fi
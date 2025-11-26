#!/bin/bash
# ============================================================================
# Agentic Turing Machine - UV Setup Script
# ============================================================================
# This script sets up the project using UV (fast Python package installer)
#
# Authors:
#   - Fouad Azem (040830861) - Fouad.Azem@gmail.com
#   - Tal Goldengorn (207042573) - T.goldengoren@gmail.com
#
# Course: LLM and Multi Agent Orchestration
# Institution: Reichman University
# Instructor: Dr. Yoram Segal
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🤖 Agentic Turing Machine - UV Setup                       ║${NC}"
echo -e "${BLUE}║     Multi-Agent Translation System with Semantic Drift         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check if UV is installed
echo -e "${YELLOW}Step 1/5: Checking for UV installation...${NC}"
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✓ UV is installed ($(uv --version))${NC}"
else
    echo -e "${YELLOW}UV not found. Installing UV...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell config to get uv in PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if command -v uv &> /dev/null; then
        echo -e "${GREEN}✓ UV installed successfully!${NC}"
    else
        echo -e "${RED}✗ Failed to install UV. Please install manually:${NC}"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

# Step 2: Check Python version
echo ""
echo -e "${YELLOW}Step 2/5: Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo -e "${GREEN}✓ Python $PYTHON_VERSION is installed (requires >= $REQUIRED_VERSION)${NC}"
else
    echo -e "${RED}✗ Python $PYTHON_VERSION is too old. Please install Python >= $REQUIRED_VERSION${NC}"
    exit 1
fi

# Step 3: Create virtual environment
echo ""
echo -e "${YELLOW}Step 3/5: Creating virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${YELLOW}  Virtual environment already exists. Removing old one...${NC}"
    rm -rf .venv
fi

uv venv
echo -e "${GREEN}✓ Virtual environment created at .venv/${NC}"

# Step 4: Install dependencies
echo ""
echo -e "${YELLOW}Step 4/5: Installing dependencies with UV (this is FAST!)...${NC}"
source .venv/bin/activate

# Install all dependencies including dev and notebook
uv pip install -e ".[all]"

echo -e "${GREEN}✓ All dependencies installed!${NC}"

# Step 5: Verify installation
echo ""
echo -e "${YELLOW}Step 5/5: Verifying installation...${NC}"

# Check key packages
PACKAGES=("anthropic" "numpy" "matplotlib" "scikit-learn" "pytest")
ALL_OK=true

for pkg in "${PACKAGES[@]}"; do
    if python -c "import $pkg" 2>/dev/null; then
        echo -e "${GREEN}  ✓ $pkg${NC}"
    else
        echo -e "${RED}  ✗ $pkg (not installed)${NC}"
        ALL_OK=false
    fi
done

echo ""
if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ Setup Complete! All dependencies installed successfully!   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ⚠️  Some packages failed to install. Check errors above.       ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi

# Print usage instructions
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}                        NEXT STEPS                                ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}1. Activate the virtual environment:${NC}"
echo "   source .venv/bin/activate"
echo ""
echo -e "${YELLOW}2. Set your Claude API key:${NC}"
echo "   export ANTHROPIC_API_KEY='your-key-here'"
echo ""
echo -e "${YELLOW}3. Run experiments:${NC}"
echo "   # Single noise level"
echo "   uv run python run_with_skills.py --noise 25"
echo ""
echo "   # All noise levels"
echo "   uv run python run_with_skills.py --all"
echo ""
echo -e "${YELLOW}4. Analyze results (no API needed):${NC}"
echo "   uv run python analyze_results_local.py"
echo ""
echo -e "${YELLOW}5. Run tests:${NC}"
echo "   uv run pytest tests/ --cov=src -v"
echo ""
echo -e "${YELLOW}6. Test individual agent:${NC}"
echo "   uv run python test_agent.py english-to-french-translator \"Hello world\""
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""


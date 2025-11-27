#!/bin/bash
#
# Agentic Turing Machine - Dashboard Launcher
# ============================================
#
# MIT-Level Interactive Research Dashboard
# 
# This script launches the Streamlit dashboard for visualizing
# semantic drift analysis results.
#
# Usage:
#   ./scripts/utilities/run_dashboard.sh [OPTIONS]
#
# Options:
#   --port PORT     Run on specific port (default: 8501)
#   --headless      Run in headless mode (no browser)
#   --dark          Use dark theme
#   --help          Show this help message
#
# Examples:
#   ./scripts/utilities/run_dashboard.sh
#   ./scripts/utilities/run_dashboard.sh --port 8080
#   ./scripts/utilities/run_dashboard.sh --dark --headless
#
# Authors: Fouad Azem & Tal Goldengorn
# License: MIT
#

set -e

# Default values
PORT=8501
HEADLESS=""
THEME=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
print_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                  ║"
    echo "║    🤖 Agentic Turing Machine - Interactive Dashboard 🤖          ║"
    echo "║                                                                  ║"
    echo "║    MIT-Level Research Visualization                              ║"
    echo "║                                                                  ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Show help
show_help() {
    print_banner
    echo -e "${CYAN}Usage:${NC}"
    echo "  ./scripts/utilities/run_dashboard.sh [OPTIONS]"
    echo ""
    echo -e "${CYAN}Options:${NC}"
    echo "  --port PORT     Run on specific port (default: 8501)"
    echo "  --headless      Run in headless mode (no browser)"
    echo "  --dark          Use dark theme"
    echo "  --help          Show this help message"
    echo ""
    echo -e "${CYAN}Examples:${NC}"
    echo "  ./scripts/utilities/run_dashboard.sh"
    echo "  ./scripts/utilities/run_dashboard.sh --port 8080"
    echo "  ./scripts/utilities/run_dashboard.sh --dark --headless"
    echo ""
    echo -e "${CYAN}Dashboard Pages:${NC}"
    echo "  🏠 Overview             - Key metrics and findings"
    echo "  🔬 Semantic Drift       - Interactive noise analysis"
    echo "  🔄 Translation Pipeline - EN→FR→HE→EN visualization"
    echo "  📈 Statistical Analysis - Correlation & regression"
    echo "  🎛️ Sensitivity Analysis - Parameter exploration"
    echo "  💰 Cost Tracker         - API usage visualization"
    echo "  ℹ️ About                - Project information"
    echo ""
}

# Check dependencies
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: Python 3 is not installed${NC}"
        exit 1
    fi
    
    # Check Streamlit
    if ! python3 -c "import streamlit" 2>/dev/null; then
        echo -e "${YELLOW}Warning: Streamlit is not installed${NC}"
        echo -e "${CYAN}Installing dashboard dependencies...${NC}"
        
        if command -v uv &> /dev/null; then
            uv pip install streamlit plotly pandas
        else
            pip install streamlit plotly pandas
        fi
    fi
    
    # Check Plotly
    if ! python3 -c "import plotly" 2>/dev/null; then
        echo -e "${YELLOW}Warning: Plotly is not installed${NC}"
        echo -e "${CYAN}Installing Plotly...${NC}"
        
        if command -v uv &> /dev/null; then
            uv pip install plotly
        else
            pip install plotly
        fi
    fi
    
    echo -e "${GREEN}✓ All dependencies installed${NC}"
}

# Check for analysis data
check_data() {
    echo -e "${BLUE}Checking for analysis data...${NC}"
    
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
    
    if [ ! -f "$PROJECT_ROOT/results/analysis_results_local.json" ]; then
        echo -e "${YELLOW}Warning: Analysis results not found${NC}"
        echo -e "${CYAN}The dashboard will show limited data.${NC}"
        echo ""
        echo -e "To generate data, run:"
        echo -e "  ${GREEN}python scripts/experiment/run_with_skills.py --all${NC}"
        echo -e "  ${GREEN}python src/analysis.py${NC}"
        echo ""
    else
        echo -e "${GREEN}✓ Analysis data found${NC}"
    fi
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --port)
                PORT="$2"
                shift 2
                ;;
            --headless)
                HEADLESS="--server.headless true"
                shift
                ;;
            --dark)
                THEME="--theme.base dark"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
}

# Main function
main() {
    # Parse arguments
    parse_args "$@"
    
    # Print banner
    print_banner
    
    # Check dependencies
    check_dependencies
    
    # Check data
    check_data
    
    # Get project root
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
    
    # Change to project root
    cd "$PROJECT_ROOT"
    
    echo ""
    echo -e "${GREEN}🚀 Launching Dashboard...${NC}"
    echo ""
    echo -e "${CYAN}Dashboard URL:${NC} ${GREEN}http://localhost:${PORT}${NC}"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop the dashboard${NC}"
    echo ""
    
    # Launch Streamlit
    streamlit run src/dashboard.py \
        --server.port "$PORT" \
        --browser.gatherUsageStats false \
        $HEADLESS \
        $THEME
}

# Run main
main "$@"


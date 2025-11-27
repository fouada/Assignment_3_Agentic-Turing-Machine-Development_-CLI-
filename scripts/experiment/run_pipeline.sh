#!/bin/bash
# Complete End-to-End Pipeline Execution
# Runs experiments and analysis in one command

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     AGENTIC TURING MACHINE - COMPLETE PIPELINE                   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo ""
    echo "Please set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    exit 1
fi

# Check for required files
if [ ! -f "run_with_skills.py" ] || [ ! -f "analyze_results_local.py" ]; then
    echo "❌ Error: Required scripts not found"
    echo "   Please run this from the project directory"
    exit 1
fi

# Check for skills
if [ ! -d "skills" ]; then
    echo "❌ Error: skills/ directory not found"
    exit 1
fi

SKILL_COUNT=$(find skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SKILL_COUNT" -eq 0 ]; then
    echo "❌ Error: No agent skills found in skills/"
    exit 1
fi

echo "✓ Environment check passed"
echo "✓ Found $SKILL_COUNT agent skills"
echo ""

# Parse arguments
RUN_MODE="all"
SKIP_ANALYSIS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --noise)
            RUN_MODE="single"
            NOISE_LEVEL="$2"
            shift 2
            ;;
        --skip-analysis)
            SKIP_ANALYSIS=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --noise N          Run single noise level (0-50)"
            echo "  --skip-analysis    Skip analysis step"
            echo "  --help, -h         Show this help"
            echo ""
            echo "Examples:"
            echo "  $0                      # Run complete pipeline"
            echo "  $0 --noise 25           # Run single noise level"
            echo "  $0 --skip-analysis      # Run experiments only"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Step 1: Run Experiments
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Running Agent Chain Experiments"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

START_TIME=$(date +%s)

if [ "$RUN_MODE" = "all" ]; then
    echo "Mode: All noise levels (0%, 10%, 20%, 25%, 30%, 40%, 50%)"
    echo ""
    python3 run_with_skills.py --all
else
    echo "Mode: Single noise level ($NOISE_LEVEL%)"
    echo ""
    python3 run_with_skills.py --noise "$NOISE_LEVEL"
fi

EXPERIMENT_TIME=$(($(date +%s) - START_TIME))

echo ""
echo "✅ Experiments complete! (${EXPERIMENT_TIME}s)"
echo ""

# List outputs
OUTPUT_COUNT=$(find outputs -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
echo "📁 Generated $OUTPUT_COUNT output files in outputs/"
echo ""

# Step 2: Analyze Results
if [ "$SKIP_ANALYSIS" = false ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "STEP 2: Analyzing Results (Local - No API Calls)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    ANALYSIS_START=$(date +%s)
    
    python3 analyze_results_local.py
    
    ANALYSIS_TIME=$(($(date +%s) - ANALYSIS_START))
    
    echo ""
    echo "✅ Analysis complete! (${ANALYSIS_TIME}s)"
    echo ""
else
    echo "⏭️  Skipping analysis (--skip-analysis flag set)"
    echo ""
fi

# Step 3: Summary
TOTAL_TIME=$(($(date +%s) - START_TIME))

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PIPELINE COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⏱️  Total time: ${TOTAL_TIME}s"
echo ""

if [ "$SKIP_ANALYSIS" = false ]; then
    echo "📊 Results:"
    echo "   • outputs/ ............................ Agent outputs"
    echo "   • analysis_results_local.json ......... Raw metrics"
    echo "   • semantic_drift_analysis_local.png ... Visualization"
    echo "   • semantic_drift_analysis_local.pdf ... Publication version"
    echo ""
    
    # Check if files exist
    if [ -f "semantic_drift_analysis_local.png" ]; then
        echo "🎯 View results:"
        echo "   open semantic_drift_analysis_local.png"
        echo ""
        
        # Try to open automatically (macOS/Linux)
        if command -v open &> /dev/null; then
            read -p "Open visualization now? [y/N] " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                open semantic_drift_analysis_local.png
            fi
        elif command -v xdg-open &> /dev/null; then
            read -p "Open visualization now? [y/N] " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                xdg-open semantic_drift_analysis_local.png
            fi
        fi
    fi
else
    echo "📊 To analyze results, run:"
    echo "   python3 analyze_results_local.py"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ All done! Your results are ready for analysis."
echo ""


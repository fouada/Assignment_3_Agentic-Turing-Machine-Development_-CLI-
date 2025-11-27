#!/usr/bin/env python3
"""
Master Research Analysis Script
===============================

Runs complete MIT-level research analysis suite including:
1. Standard semantic drift analysis
2. Systematic sensitivity analysis
3. Data-driven comparative analysis
4. Statistical validation tests

This script orchestrates all research components and generates
comprehensive reports suitable for academic publication.

Usage:
    python scripts/experiment/run_research_analysis.py
    python scripts/experiment/run_research_analysis.py --skip-standard
    python scripts/experiment/run_research_analysis.py --output-dir custom_results/

Author: Agentic Turing Machine Team
License: MIT
"""

import argparse
import sys
from pathlib import Path
import time
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from analysis import analyze_semantic_drift
from sensitivity_analysis import SensitivityAnalyzer
from comparative_analysis import ComparativeAnalyzer
from logger import get_logger

logger = get_logger(__name__)


def print_header(title: str):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_step(step_num: int, step_name: str):
    """Print step indicator."""
    print(f"\n[{step_num}/4] {step_name}")
    print("-" * 80)


def run_standard_analysis():
    """Run standard semantic drift analysis."""
    print_step(1, "Standard Semantic Drift Analysis")
    
    try:
        start_time = time.time()
        analyze_semantic_drift()
        elapsed = time.time() - start_time
        
        print(f"\n✓ Standard analysis complete in {elapsed:.2f}s")
        return True
    except Exception as e:
        logger.error(f"Standard analysis failed: {e}", exc_info=True)
        print(f"\n✗ Standard analysis failed: {e}")
        return False


def run_sensitivity_analysis(results_path: str = "results"):
    """Run systematic sensitivity analysis."""
    print_step(2, "Systematic Sensitivity Analysis")
    
    try:
        start_time = time.time()
        analyzer = SensitivityAnalyzer(data_path=results_path)
        
        output_file = f"{results_path}/sensitivity_analysis.json"
        report = analyzer.generate_sensitivity_report(output_file=output_file)
        
        elapsed = time.time() - start_time
        print(f"\n✓ Sensitivity analysis complete in {elapsed:.2f}s")
        
        # Print key findings
        if "bootstrap_analysis" in report and "cosine_distance" in report["bootstrap_analysis"]:
            bootstrap = report["bootstrap_analysis"]["cosine_distance"]
            if "bootstrap_mean" in bootstrap:
                print(f"  Bootstrap mean: {bootstrap['bootstrap_mean']:.6f}")
                print(f"  95% CI: [{bootstrap['ci_lower']:.6f}, {bootstrap['ci_upper']:.6f}]")
        
        return True
    except Exception as e:
        logger.error(f"Sensitivity analysis failed: {e}", exc_info=True)
        print(f"\n✗ Sensitivity analysis failed: {e}")
        return False


def run_comparative_analysis(results_path: str = "results"):
    """Run data-driven comparative analysis."""
    print_step(3, "Data-Driven Comparative Analysis")
    
    try:
        start_time = time.time()
        analyzer = ComparativeAnalyzer(data_path=results_path)
        
        output_file = f"{results_path}/comparative_analysis.json"
        report = analyzer.generate_comparative_report(output_file=output_file)
        
        elapsed = time.time() - start_time
        print(f"\n✓ Comparative analysis complete in {elapsed:.2f}s")
        
        # Print key findings
        if "correlation_analysis" in report and "results" in report["correlation_analysis"]:
            correlations = report["correlation_analysis"]["results"]
            if correlations:
                # Find Pearson correlation for semantic_distance
                for corr in correlations:
                    if (corr.get("variable2") == "semantic_distance" and 
                        corr.get("test_name") == "Pearson r"):
                        print(f"  Noise vs Distance: r={corr['correlation_coefficient']:.4f}, p={corr['p_value']:.6f}")
                        break
        
        return True
    except Exception as e:
        logger.error(f"Comparative analysis failed: {e}", exc_info=True)
        print(f"\n✗ Comparative analysis failed: {e}")
        return False


def generate_summary_report(results_path: str = "results"):
    """Generate master summary report combining all analyses."""
    print_step(4, "Generating Master Summary Report")
    
    try:
        # Load all analysis results
        analysis_file = Path(results_path) / "analysis_results_local.json"
        sensitivity_file = Path(results_path) / "sensitivity_analysis.json"
        comparative_file = Path(results_path) / "comparative_analysis.json"
        
        summary = {
            "title": "MIT-Level Research Analysis Summary",
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "analyses_completed": []
        }
        
        # Check which analyses completed
        if analysis_file.exists():
            summary["analyses_completed"].append("standard_semantic_drift")
            with open(analysis_file, 'r') as f:
                standard_results = json.load(f)
            summary["standard_analysis"] = {
                "embedding_method": standard_results.get("embedding_method"),
                "distance_metric": standard_results.get("distance_metric"),
                "noise_levels": list(standard_results.get("semantic_distances", {}).keys())
            }
        
        if sensitivity_file.exists():
            summary["analyses_completed"].append("systematic_sensitivity")
            with open(sensitivity_file, 'r') as f:
                sensitivity_results = json.load(f)
            summary["sensitivity_analysis"] = {
                "n_bootstrap_iterations": sensitivity_results.get("metadata", {}).get("n_bootstrap_iterations"),
                "parameters_tested": list(sensitivity_results.get("parameter_sensitivity", {}).keys())
            }
        
        if comparative_file.exists():
            summary["analyses_completed"].append("data_driven_comparative")
            with open(comparative_file, 'r') as f:
                comparative_results = json.load(f)
            summary["comparative_analysis"] = {
                "correction_method": comparative_results.get("metadata", {}).get("correction_method"),
                "tests_performed": ["pairwise_comparisons", "correlation_analysis", "regression_analysis"]
            }
        
        # Save summary
        summary_file = Path(results_path) / "research_analysis_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Master summary report saved to: {summary_file}")
        print(f"\nAnalyses completed: {len(summary['analyses_completed'])}/3")
        for analysis in summary['analyses_completed']:
            print(f"  ✓ {analysis}")
        
        return True
    except Exception as e:
        logger.error(f"Summary report generation failed: {e}", exc_info=True)
        print(f"\n✗ Summary report generation failed: {e}")
        return False


def main():
    """Main entry point for master research analysis."""
    parser = argparse.ArgumentParser(
        description="Run complete MIT-level research analysis suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Run all analyses:
    python run_research_analysis.py
  
  Skip standard analysis (use existing results):
    python run_research_analysis.py --skip-standard
  
  Custom output directory:
    python run_research_analysis.py --output-dir custom_results/
        """
    )
    
    parser.add_argument(
        '--skip-standard',
        action='store_true',
        help='Skip standard semantic drift analysis (use existing results)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='results',
        help='Output directory for results (default: results/)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header("MIT-LEVEL RESEARCH ANALYSIS SUITE")
    print("Comprehensive statistical analysis for publication-ready research")
    print(f"Output directory: {args.output_dir}/")
    print(f"Skip standard analysis: {'Yes' if args.skip_standard else 'No'}")
    
    # Create output directory if needed
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Track success
    successes = []
    failures = []
    
    # Run analyses
    try:
        # Step 1: Standard analysis
        if not args.skip_standard:
            if run_standard_analysis():
                successes.append("standard_analysis")
            else:
                failures.append("standard_analysis")
        else:
            print_step(1, "Standard Semantic Drift Analysis")
            print("Skipped (using existing results)")
            successes.append("standard_analysis (skipped)")
        
        # Step 2: Sensitivity analysis
        if run_sensitivity_analysis(results_path=args.output_dir):
            successes.append("sensitivity_analysis")
        else:
            failures.append("sensitivity_analysis")
        
        # Step 3: Comparative analysis
        if run_comparative_analysis(results_path=args.output_dir):
            successes.append("comparative_analysis")
        else:
            failures.append("comparative_analysis")
        
        # Step 4: Summary report
        if generate_summary_report(results_path=args.output_dir):
            successes.append("summary_report")
        else:
            failures.append("summary_report")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        logger.warning("Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    
    # Print final summary
    print("\n" + "=" * 80)
    print("  ANALYSIS COMPLETE")
    print("=" * 80)
    
    print(f"\nSuccessful: {len(successes)}")
    for success in successes:
        print(f"  ✓ {success}")
    
    if failures:
        print(f"\nFailed: {len(failures)}")
        for failure in failures:
            print(f"  ✗ {failure}")
    
    print(f"\nResults saved to: {args.output_dir}/")
    print("\nGenerated files:")
    print(f"  - {args.output_dir}/analysis_results_local.json")
    print(f"  - {args.output_dir}/sensitivity_analysis.json")
    print(f"  - {args.output_dir}/comparative_analysis.json")
    print(f"  - {args.output_dir}/research_analysis_summary.json")
    print(f"  - {args.output_dir}/semantic_drift_analysis_local.png")
    
    print("\n📚 Documentation:")
    print("  - docs/MATHEMATICAL_PROOFS.md - Formal theorems and proofs")
    print("  - docs/RESEARCH_METHODOLOGY.md - Complete research framework")
    print("  - docs/ACADEMIC_PAPER.md - Publication-ready paper")
    
    print("\n" + "=" * 80)
    
    # Exit code
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()


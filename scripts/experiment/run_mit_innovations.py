#!/usr/bin/env python3
"""
MIT-Level Innovations Runner
=============================

Run all MIT-level innovative research components in one command.

This script executes:
1. Information-Theoretic Analysis (Entropy, MI, KL Divergence)
2. Stochastic Resonance Detection
3. Self-Healing Translation Analysis
4. Adversarial Robustness Testing

Usage:
    python scripts/experiment/run_mit_innovations.py

Author: Agentic Turing Machine Team
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def print_header(title: str):
    """Print a formatted header."""
    print()
    print("=" * 80)
    print(f"🔬 {title}")
    print("=" * 80)
    print()


def run_information_theory():
    """Run information-theoretic analysis."""
    print_header("INFORMATION-THEORETIC ANALYSIS")
    print("Analyzing: Shannon Entropy, Mutual Information, KL Divergence")
    print()
    
    try:
        from information_theory import InformationTheoreticAnalyzer
        analyzer = InformationTheoreticAnalyzer(data_path="results")
        report = analyzer.generate_information_theory_report()
        
        if "summary" in report:
            summary = report["summary"]
            print(f"✓ Mean Normalized MI: {summary.get('mean_normalized_mi', 0):.4f}")
            print(f"✓ Mean Jensen-Shannon: {summary.get('mean_jensen_shannon', 0):.4f}")
        
        return True
    except Exception as e:
        print(f"✗ Information theory analysis failed: {e}")
        return False


def run_stochastic_resonance():
    """Run stochastic resonance detection."""
    print_header("STOCHASTIC RESONANCE DETECTION")
    print("Testing: SR in LLM attention mechanisms")
    print()
    
    try:
        from stochastic_resonance import StochasticResonanceDetector
        detector = StochasticResonanceDetector(data_path="results")
        report = detector.generate_stochastic_resonance_report()
        
        if "stochastic_resonance" in report:
            sr = report["stochastic_resonance"]
            detected = "✅ YES" if sr.get('sr_detected') else "❌ NO"
            print(f"✓ SR Detected: {detected}")
            print(f"✓ Optimal Noise: {sr.get('optimal_noise_level', 0):.1f}%")
            print(f"✓ SR Gain: {sr.get('sr_gain', 1):.3f}x")
        
        return True
    except Exception as e:
        print(f"✗ Stochastic resonance analysis failed: {e}")
        return False


def run_self_healing():
    """Run self-healing translation analysis."""
    print_header("SELF-HEALING TRANSLATION ANALYSIS")
    print("Testing: Confidence-based automatic error correction")
    print()
    
    try:
        from self_healing_agent import SelfHealingAnalyzer
        analyzer = SelfHealingAnalyzer(data_path="results")
        report = analyzer.generate_self_healing_report()
        
        if "summary" in report:
            summary = report["summary"]
            print(f"✓ Mean Improvement: {summary.get('mean_improvement', 0):.2%}")
            print(f"✓ Success Rate: {summary.get('mean_success_rate', 0):.2%}")
            print(f"✓ Effectiveness: {summary.get('overall_effectiveness', 'unknown')}")
        
        return True
    except Exception as e:
        print(f"✗ Self-healing analysis failed: {e}")
        return False


def run_adversarial_robustness():
    """Run adversarial robustness testing."""
    print_header("ADVERSARIAL ROBUSTNESS TESTING")
    print("Testing: Homoglyphs, invisible chars, typosquatting, synonyms")
    print()
    
    try:
        from adversarial_robustness import RobustnessEvaluator
        evaluator = RobustnessEvaluator(data_path="results")
        report = evaluator.generate_adversarial_report()
        
        if "robustness_score" in report:
            rs = report["robustness_score"]
            print(f"✓ Overall Score: {rs.get('overall_score', 0):.1f}/100")
            print(f"✓ Grade: {rs.get('robustness_grade', 'N/A')}")
            print(f"✓ Vulnerabilities: {rs.get('vulnerability_count', 0)}")
        
        return True
    except Exception as e:
        print(f"✗ Adversarial robustness analysis failed: {e}")
        return False


def main():
    """Run all MIT-level innovations."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " MIT-LEVEL INNOVATION SUITE ".center(78) + "║")
    print("║" + " Agentic Turing Machine Research Components ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    
    results = {}
    
    # Run all analyses
    results["information_theory"] = run_information_theory()
    results["stochastic_resonance"] = run_stochastic_resonance()
    results["self_healing"] = run_self_healing()
    results["adversarial_robustness"] = run_adversarial_robustness()
    
    # Summary
    print()
    print("=" * 80)
    print("📊 EXECUTION SUMMARY")
    print("=" * 80)
    print()
    
    success_count = sum(results.values())
    total_count = len(results)
    
    for name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {name}: {status}")
    
    print()
    print(f"   Total: {success_count}/{total_count} analyses completed successfully")
    print()
    
    if success_count == total_count:
        print("🎉 All MIT-level innovations executed successfully!")
        print()
        print("📁 Generated Reports:")
        print("   • results/information_theory_analysis.json")
        print("   • results/stochastic_resonance_analysis.json")
        print("   • results/self_healing_analysis.json")
        print("   • results/adversarial_robustness.json")
    else:
        print("⚠️ Some analyses failed. Check the logs above.")
    
    print()
    print("=" * 80)
    
    return 0 if success_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())


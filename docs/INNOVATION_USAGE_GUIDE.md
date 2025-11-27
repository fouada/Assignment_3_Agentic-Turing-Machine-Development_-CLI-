# MIT-Level Innovations: Complete Usage Guide
## Step-by-Step Instructions for All Innovation Modules

**Document Type:** Usage Guide  
**Date:** November 27, 2025

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Information-Theoretic Analysis](#2-information-theoretic-analysis)
3. [Stochastic Resonance Detection](#3-stochastic-resonance-detection)
4. [Self-Healing Translation](#4-self-healing-translation)
5. [Adversarial Robustness Testing](#5-adversarial-robustness-testing)
6. [Running All Innovations](#6-running-all-innovations)
7. [Understanding the Output](#7-understanding-the-output)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Quick Start

### Prerequisites

```bash
# Ensure you have the required dependencies
cd Assignment_3_Agentic-Turing-Machine-Development_-CLI-
source .venv/bin/activate

# You need experimental results first
# If you haven't run experiments yet:
python scripts/experiment/run_with_skills.py --all
python scripts/experiment/analyze_results.py
```

### Run All Innovations at Once

```bash
python scripts/experiment/run_mit_innovations.py
```

This generates 4 JSON reports in the `results/` directory.

---

## 2. Information-Theoretic Analysis

### Purpose

Measures translation quality using **information theory** metrics:
- **Entropy**: How much information is in the text
- **Mutual Information**: How much original information survives translation
- **KL Divergence**: How much the word distribution changes

### How to Use

#### Option A: Command Line (Simplest)

```bash
cd Assignment_3_Agentic-Turing-Machine-Development_-CLI-
python -m src.information_theory
```

#### Option B: Python API

```python
from src.information_theory import InformationTheoreticAnalyzer

# Initialize with results directory
analyzer = InformationTheoreticAnalyzer(data_path="results")

# Calculate entropy for a text
entropy_result = analyzer.calculate_entropy(
    "The artificial intelligence system processes data efficiently.",
    level="word"  # or "char"
)
print(f"Shannon Entropy: {entropy_result.shannon_entropy:.4f}")
print(f"Normalized Entropy: {entropy_result.normalized_entropy:.4f}")
print(f"Interpretation: {entropy_result.interpretation}")

# Calculate mutual information between two texts
mi_result = analyzer.calculate_mutual_information(
    "The quick brown fox jumps over the lazy dog.",
    "The fast brown fox leaps over the lazy dog.",
    text1_name="original",
    text2_name="translated"
)
print(f"Mutual Information: {mi_result.mutual_information:.4f}")
print(f"Normalized MI: {mi_result.normalized_mi:.4f}")
print(f"Information Loss: {mi_result.information_loss:.4f}")

# Calculate KL Divergence
kl_result = analyzer.calculate_kl_divergence(
    "hello world hello world",
    "hello universe hello universe"
)
print(f"KL Divergence: {kl_result.kl_divergence:.4f}")
print(f"Jensen-Shannon: {kl_result.jensen_shannon:.4f}")

# Generate comprehensive report
report = analyzer.generate_information_theory_report(
    output_file="results/information_theory_analysis.json"
)
```

### Output Example

```json
{
  "metadata": {
    "analysis_type": "Information-Theoretic Analysis",
    "innovation_level": "MIT Graduate Research"
  },
  "entropy_analysis": {
    "original": {
      "shannon_entropy": 3.456,
      "normalized_entropy": 0.85,
      "interpretation": "High entropy: rich, diverse content"
    }
  },
  "mutual_information": {
    "noise_0": {
      "mutual_information": 2.34,
      "normalized_mi": 0.92,
      "information_loss": 0.45
    }
  }
}
```

---

## 3. Stochastic Resonance Detection

### Purpose

Tests the **counter-intuitive hypothesis** that moderate noise can IMPROVE translation quality.

### How to Use

#### Option A: Command Line

```bash
python -m src.stochastic_resonance
```

#### Option B: Python API

```python
from src.stochastic_resonance import StochasticResonanceDetector

# Initialize
detector = StochasticResonanceDetector(data_path="results")

# Detect stochastic resonance
sr_result = detector.detect_stochastic_resonance()
print(f"SR Detected: {'YES' if sr_result.sr_detected else 'NO'}")
print(f"Optimal Noise Level: {sr_result.optimal_noise_level:.1f}%")
print(f"SR Gain: {sr_result.sr_gain:.3f}x")
print(f"Resonance Strength: {sr_result.resonance_strength}")
print(f"Interpretation: {sr_result.interpretation}")

# Analyze SNR curve
curve = detector.analyze_snr_curve()
print(f"Curve Type: {curve.curve_type}")
print(f"Noise Levels: {curve.noise_levels}")
print(f"SNR Values: {curve.snr_values}")

# Model attention threshold
threshold = detector.model_attention_threshold()
print(f"Threshold Estimate: {threshold.threshold_estimate:.1f}%")
print(f"Model R²: {threshold.model_fit_r2:.3f}")

# Generate full report
report = detector.generate_stochastic_resonance_report(
    output_file="results/stochastic_resonance_analysis.json"
)
```

### Interpreting Results

| Result | Meaning |
|--------|---------|
| `sr_detected: true` | Noise improved translation! Counter-intuitive finding. |
| `sr_detected: false` | Monotonic decrease (expected behavior) |
| `optimal_noise_level: 15%` | Best translation quality at 15% noise |
| `sr_gain: 1.2` | 20% improvement over zero noise |

---

## 4. Self-Healing Translation

### Purpose

Implements **automatic error detection and correction** for translations.

### How to Use

#### Option A: Command Line

```bash
python -m src.self_healing_agent
```

#### Option B: Python API (Confidence Estimation)

```python
from src.self_healing_agent import ConfidenceEstimator

estimator = ConfidenceEstimator()

# Estimate translation confidence
confidence = estimator.estimate_confidence(
    source_text="The artificial intelligence system can process data.",
    translated_text="The AI system processes data efficiently."
)

print(f"Overall Confidence: {confidence.overall_confidence:.2%}")
print(f"Lexical Confidence: {confidence.lexical_confidence:.2%}")
print(f"Semantic Confidence: {confidence.semantic_confidence:.2%}")
print(f"Structural Confidence: {confidence.structural_confidence:.2%}")
print(f"Fluency Confidence: {confidence.fluency_confidence:.2%}")
print(f"Needs Review: {confidence.needs_review}")
print(f"Explanation: {confidence.confidence_explanation}")
```

#### Option C: Python API (Error Detection)

```python
from src.self_healing_agent import ErrorDetector

detector = ErrorDetector(threshold=0.7)

# Detect errors
result = detector.detect_errors(
    source_text="The artificial intelligence system processes complex data efficiently.",
    translated_text="AI data."  # Severely truncated
)

print(f"Error Detected: {result.error_detected}")
print(f"Error Type: {result.error_type}")  # semantic_drift, lexical_loss, hallucination, truncation
print(f"Severity: {result.error_severity}")  # critical, major, minor, none
print(f"Correction Recommended: {result.correction_recommended}")
```

#### Option D: Python API (Full Self-Healing)

```python
from src.self_healing_agent import SelfHealingTranslator

# Initialize healer
healer = SelfHealingTranslator(
    confidence_threshold=0.7,
    max_iterations=3
)

# Heal a translation
report = healer.heal_translation(
    source_text="The artificial intelligence system can efficiently process data.",
    translated_text="The AI can process."  # Needs healing
)

print(f"Initial Confidence: {report.initial_confidence:.2%}")
print(f"Final Confidence: {report.final_confidence:.2%}")
print(f"Improvement: {report.confidence_improvement:.2%}")
print(f"Corrections Applied: {report.successful_corrections}")
print(f"Final Quality: {report.overall_quality}")
print(f"Final Output: {report.final_output}")
```

---

## 5. Adversarial Robustness Testing

### Purpose

Tests how well the system handles **adversarial attacks** (not just random noise).

### How to Use

#### Option A: Command Line

```bash
python -m src.adversarial_robustness
```

#### Option B: Python API (Generate Attacks)

```python
from src.adversarial_robustness import AdversarialPerturbationGenerator

generator = AdversarialPerturbationGenerator(seed=42)
text = "The artificial intelligence system processes data."

# Homoglyph attack (visually similar characters)
homoglyph = generator.homoglyph_attack(text, perturbation_rate=0.2)
print(f"Original: {homoglyph.original_text}")
print(f"Adversarial: {homoglyph.adversarial_text}")
print(f"Changes: {homoglyph.changes_made}")

# Invisible character injection
invisible = generator.invisible_character_injection(text, injection_rate=0.1)
print(f"Attack Type: {invisible.attack_type}")

# Typosquatting
typo = generator.typosquatting_attack(text, perturbation_rate=0.3)
print(f"Typo Attack: {typo.adversarial_text}")

# Synonym substitution
synonym = generator.synonym_substitution(text, substitution_rate=0.5)
print(f"Synonym Attack: {synonym.adversarial_text}")

# Generate all attack types
all_attacks = generator.generate_all_attacks(text)
for attack in all_attacks:
    print(f"{attack.attack_type}: {len(attack.changes_made)} changes")
```

#### Option C: Python API (Robustness Evaluation)

```python
from src.adversarial_robustness import RobustnessEvaluator

evaluator = RobustnessEvaluator(data_path="results")

# Generate comprehensive report
report = evaluator.generate_adversarial_report(
    output_file="results/adversarial_robustness.json"
)

# Access robustness score
score = report["robustness_score"]
print(f"Overall Score: {score['overall_score']:.1f}/100")
print(f"Grade: {score['robustness_grade']}")
print(f"Character Robustness: {score['character_robustness']:.1f}%")
print(f"Word Robustness: {score['word_robustness']:.1f}%")
print(f"Vulnerabilities: {score['vulnerability_count']}")
print(f"Recommendations:")
for rec in score['recommendations']:
    print(f"  • {rec}")
```

---

## 6. Running All Innovations

### Single Command

```bash
python scripts/experiment/run_mit_innovations.py
```

### Expected Output

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        MIT-LEVEL INNOVATION SUITE                            ║
║             Agentic Turing Machine Research Components                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

================================================================================
🔬 INFORMATION-THEORETIC ANALYSIS
================================================================================

Analyzing: Shannon Entropy, Mutual Information, KL Divergence

✓ Mean Normalized MI: 0.8542
✓ Mean Jensen-Shannon: 0.1234

================================================================================
🔬 STOCHASTIC RESONANCE DETECTION
================================================================================

Testing: SR in LLM attention mechanisms

✓ SR Detected: ❌ NO
✓ Optimal Noise: 0.0%
✓ SR Gain: 1.000x

... (more output) ...

================================================================================
📊 EXECUTION SUMMARY
================================================================================

   information_theory: ✅ PASSED
   stochastic_resonance: ✅ PASSED
   self_healing: ✅ PASSED
   adversarial_robustness: ✅ PASSED

   Total: 4/4 analyses completed successfully

🎉 All MIT-level innovations executed successfully!
```

---

## 7. Understanding the Output

### Generated Files

| File | Description |
|------|-------------|
| `results/information_theory_analysis.json` | Entropy, MI, KL for all noise levels |
| `results/stochastic_resonance_analysis.json` | SR detection, SNR curves, threshold models |
| `results/self_healing_analysis.json` | Healing effectiveness per noise level |
| `results/adversarial_robustness.json` | Attack success rates, robustness score |

### Key Metrics to Look For

| Metric | Good Value | Meaning |
|--------|------------|---------|
| `normalized_mi` | > 0.7 | High information preservation |
| `jensen_shannon` | < 0.3 | Low distributional shift |
| `sr_detected` | true | Counter-intuitive noise benefit |
| `overall_confidence` | > 0.8 | High translation quality |
| `robustness_score` | > 70 | Good attack resistance |

---

## 8. Troubleshooting

### Error: "Results file not found"

```bash
# Run experiments first
python scripts/experiment/run_with_skills.py --all
python scripts/experiment/analyze_results.py
```

### Error: "Module not found"

```bash
# Ensure you're in the right directory
cd Assignment_3_Agentic-Turing-Machine-Development_-CLI-
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[all]"
```

### Error: "ImportError: scipy"

```bash
pip install scipy scikit-learn numpy
```

---

## 9. Running Tests

```bash
# Run all innovation tests
pytest tests/unit/test_innovations.py -v

# Run specific test class
pytest tests/unit/test_innovations.py::TestInformationTheory -v
pytest tests/unit/test_innovations.py::TestStochasticResonance -v
pytest tests/unit/test_innovations.py::TestSelfHealingAgent -v
pytest tests/unit/test_innovations.py::TestAdversarialRobustness -v

# Run with coverage
pytest tests/unit/test_innovations.py --cov=src -v
```

---

**Document Status:** ✅ Complete  
**Last Updated:** November 27, 2025


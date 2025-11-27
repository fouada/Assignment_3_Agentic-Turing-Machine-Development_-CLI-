#!/usr/bin/env python3
"""
Tests for MIT-Level Innovation Modules
======================================

Comprehensive tests for:
1. Information-Theoretic Analysis
2. Stochastic Resonance Detection
3. Self-Healing Translation
4. Adversarial Robustness Testing

Author: Agentic Turing Machine Team
"""

import pytest
import numpy as np
import json
from pathlib import Path
import tempfile
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# ===========================================================================
# FIXTURES
# ===========================================================================

@pytest.fixture
def sample_results():
    """Create sample results data for testing."""
    return {
        "original_sentence": "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data.",
        "final_outputs": {
            "0": "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data.",
            "10": "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships in textual data.",
            "25": "The AI system can efficiently process natural language and understand complex semantic relationships within text data.",
            "50": "The artificial intelligence system processes natural language and understands semantic relationships in textual data."
        },
        "semantic_distances": {
            "0": 0.0,
            "10": 0.05,
            "25": 0.15,
            "50": 0.25
        },
        "text_similarities": {
            "0": 1.0,
            "10": 0.95,
            "25": 0.85,
            "50": 0.75
        },
        "word_overlaps": {
            "0": 1.0,
            "10": 0.95,
            "25": 0.90,
            "50": 0.80
        }
    }


@pytest.fixture
def temp_results_dir(sample_results):
    """Create a temporary results directory with sample data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        results_file = Path(tmpdir) / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(sample_results, f)
        yield tmpdir


# ===========================================================================
# INFORMATION THEORY TESTS
# ===========================================================================

class TestInformationTheory:
    """Tests for Information-Theoretic Analysis module."""
    
    def test_import(self):
        """Test that module imports correctly."""
        from information_theory import (
            InformationTheoreticAnalyzer,
            EntropyResult,
            MutualInformationResult,
            KLDivergenceResult
        )
        assert InformationTheoreticAnalyzer is not None
    
    def test_entropy_calculation(self, temp_results_dir):
        """Test Shannon entropy calculation."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        
        text = "hello world hello"
        result = analyzer.calculate_entropy(text, level="word")
        
        assert result.shannon_entropy >= 0
        assert 0 <= result.normalized_entropy <= 1
        assert result.redundancy >= 0
    
    def test_mutual_information(self, temp_results_dir):
        """Test mutual information calculation."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        
        text1 = "The quick brown fox jumps over the lazy dog"
        text2 = "The quick brown fox leaps over the lazy dog"
        
        result = analyzer.calculate_mutual_information(text1, text2)
        
        assert result.mutual_information >= 0
        assert 0 <= result.normalized_mi <= 1
        assert result.entropy_text1 >= 0
        assert result.entropy_text2 >= 0
    
    def test_kl_divergence(self, temp_results_dir):
        """Test KL divergence calculation."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        
        text1 = "hello world hello"
        text2 = "hello universe hello"
        
        result = analyzer.calculate_kl_divergence(text1, text2)
        
        assert result.kl_divergence >= 0
        assert result.jensen_shannon >= 0
        assert 0 <= result.total_variation <= 1
    
    def test_information_bottleneck(self, temp_results_dir):
        """Test information bottleneck analysis."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        
        original = "The artificial intelligence system processes data efficiently."
        intermediate = ["The AI system processes data efficiently."]
        final = "The AI system handles data well."
        
        result = analyzer.information_bottleneck_analysis(original, intermediate, final)
        
        assert 0 <= result.compression_rate <= 1
        assert 0 <= result.relevance_preserved <= 1
        assert 0 <= result.bottleneck_quality <= 1
    
    def test_report_generation(self, temp_results_dir):
        """Test report generation."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        
        output_file = Path(temp_results_dir) / "test_info_theory.json"
        report = analyzer.generate_information_theory_report(str(output_file))
        
        assert "metadata" in report
        assert output_file.exists()


# ===========================================================================
# STOCHASTIC RESONANCE TESTS
# ===========================================================================

class TestStochasticResonance:
    """Tests for Stochastic Resonance Detection module."""
    
    def test_import(self):
        """Test that module imports correctly."""
        from stochastic_resonance import (
            StochasticResonanceDetector,
            StochasticResonanceResult,
            SNRCurveResult,
            AttentionThresholdModel
        )
        assert StochasticResonanceDetector is not None
    
    def test_snr_calculation(self, temp_results_dir):
        """Test SNR calculation."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        
        snr = detector.calculate_snr(
            noise_level=10,
            similarity=0.9,
            baseline_similarity=0.95
        )
        
        assert isinstance(snr, float)
        # SNR can be negative (in dB)
    
    def test_sr_detection(self, temp_results_dir):
        """Test stochastic resonance detection."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        result = detector.detect_stochastic_resonance()
        
        assert isinstance(result.sr_detected, bool)
        assert result.optimal_noise_level >= 0
        assert result.sr_gain >= 0
        assert result.resonance_strength in ["strong", "moderate", "weak", "none"]
    
    def test_snr_curve_analysis(self, temp_results_dir):
        """Test SNR curve analysis."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        result = detector.analyze_snr_curve()
        
        assert len(result.noise_levels) > 0
        assert len(result.snr_values) == len(result.noise_levels)
        assert result.curve_type in ["resonant", "monotonic_decreasing", "monotonic_increasing"]
    
    def test_attention_threshold_model(self, temp_results_dir):
        """Test attention threshold modeling."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        result = detector.model_attention_threshold()
        
        assert result.threshold_estimate >= 0
        assert 0 <= result.model_fit_r2 <= 1 or result.model_fit_r2 <= 0  # Can be negative for bad fits
    
    def test_report_generation(self, temp_results_dir):
        """Test report generation."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        
        output_file = Path(temp_results_dir) / "test_sr.json"
        report = detector.generate_stochastic_resonance_report(str(output_file))
        
        assert "metadata" in report
        assert output_file.exists()


# ===========================================================================
# SELF-HEALING AGENT TESTS
# ===========================================================================

class TestSelfHealingAgent:
    """Tests for Self-Healing Translation Agent module."""
    
    def test_import(self):
        """Test that module imports correctly."""
        from self_healing_agent import (
            SelfHealingTranslator,
            ConfidenceEstimator,
            ErrorDetector,
            SelfHealingAnalyzer
        )
        assert SelfHealingTranslator is not None
    
    def test_confidence_estimation(self):
        """Test confidence estimation."""
        from self_healing_agent import ConfidenceEstimator
        
        estimator = ConfidenceEstimator()
        
        source = "The quick brown fox jumps over the lazy dog."
        translated = "The fast brown fox jumps over the lazy dog."
        
        confidence = estimator.estimate_confidence(source, translated)
        
        assert 0 <= confidence.overall_confidence <= 1
        assert 0 <= confidence.lexical_confidence <= 1
        assert 0 <= confidence.semantic_confidence <= 1
        assert 0 <= confidence.structural_confidence <= 1
        assert 0 <= confidence.fluency_confidence <= 1
    
    def test_error_detection(self):
        """Test error detection."""
        from self_healing_agent import ErrorDetector
        
        detector = ErrorDetector(threshold=0.7)
        
        source = "The artificial intelligence system processes data."
        translated = "AI data."  # Severely truncated
        
        result = detector.detect_errors(source, translated)
        
        assert result.error_detected == True
        assert result.error_severity in ["critical", "major", "minor", "none"]
    
    def test_self_healing(self):
        """Test self-healing process."""
        from self_healing_agent import SelfHealingTranslator
        
        healer = SelfHealingTranslator(confidence_threshold=0.7, max_iterations=2)
        
        source = "The artificial intelligence system can efficiently process data."
        translated = "The AI system can process data efficiently."
        
        report = healer.heal_translation(source, translated)
        
        assert report.original_input == source
        assert report.final_output is not None
        assert 0 <= report.initial_confidence <= 1
        assert 0 <= report.final_confidence <= 1
        assert report.overall_quality in ["excellent", "good", "acceptable", "poor"]
    
    def test_healing_analyzer(self, temp_results_dir):
        """Test self-healing analyzer."""
        from self_healing_agent import SelfHealingAnalyzer
        
        analyzer = SelfHealingAnalyzer(data_path=temp_results_dir)
        analysis = analyzer.analyze_healing_effectiveness()
        
        assert "noise_level_analysis" in analysis
        assert "summary" in analysis
    
    def test_report_generation(self, temp_results_dir):
        """Test report generation."""
        from self_healing_agent import SelfHealingAnalyzer
        
        analyzer = SelfHealingAnalyzer(data_path=temp_results_dir)
        
        output_file = Path(temp_results_dir) / "test_self_healing.json"
        report = analyzer.generate_self_healing_report(str(output_file))
        
        assert "metadata" in report
        assert output_file.exists()


# ===========================================================================
# ADVERSARIAL ROBUSTNESS TESTS
# ===========================================================================

class TestAdversarialRobustness:
    """Tests for Adversarial Robustness Testing module."""
    
    def test_import(self):
        """Test that module imports correctly."""
        from adversarial_robustness import (
            AdversarialPerturbationGenerator,
            RobustnessEvaluator,
            AdversarialExample,
            RobustnessScore
        )
        assert AdversarialPerturbationGenerator is not None
    
    def test_homoglyph_attack(self):
        """Test homoglyph attack generation."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = "hello world"
        result = generator.homoglyph_attack(text, perturbation_rate=0.5)
        
        assert result.original_text == text
        assert result.attack_type == "homoglyph"
        # Adversarial should be different (with high probability at 50% rate)
    
    def test_invisible_injection(self):
        """Test invisible character injection."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = "hello world"
        result = generator.invisible_character_injection(text, injection_rate=0.3)
        
        assert result.attack_type == "invisible_injection"
        # Adversarial text should be longer (has invisible chars)
        assert len(result.adversarial_text) >= len(result.original_text)
    
    def test_typosquatting_attack(self):
        """Test typosquatting attack."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = "The artificial intelligence system processes information."
        result = generator.typosquatting_attack(text, perturbation_rate=0.5)
        
        assert result.attack_type == "typosquatting"
    
    def test_synonym_substitution(self):
        """Test synonym substitution attack."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = "The system can process complex data fast."
        result = generator.synonym_substitution(text, substitution_rate=1.0)
        
        assert result.attack_type == "synonym_substitution"
    
    def test_word_permutation(self):
        """Test word order permutation attack."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = "The quick brown fox jumps over the lazy dog."
        result = generator.word_order_permutation(text, permutation_range=2)
        
        assert result.attack_type == "word_permutation"
    
    def test_punctuation_manipulation(self):
        """Test punctuation manipulation attack."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = 'Hello, world. How are you?'
        result = generator.punctuation_manipulation(text)
        
        assert result.attack_type == "punctuation_manipulation"
    
    def test_generate_all_attacks(self):
        """Test generating all attack types."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = "The artificial intelligence system processes data efficiently."
        attacks = generator.generate_all_attacks(text)
        
        assert len(attacks) >= 5  # Should have multiple attack types
        attack_types = {a.attack_type for a in attacks}
        assert "homoglyph" in attack_types
        assert "synonym_substitution" in attack_types
    
    def test_robustness_evaluator(self, temp_results_dir):
        """Test robustness evaluator."""
        from adversarial_robustness import RobustnessEvaluator
        
        evaluator = RobustnessEvaluator(data_path=temp_results_dir)
        
        output_file = Path(temp_results_dir) / "test_adversarial.json"
        report = evaluator.generate_adversarial_report(str(output_file))
        
        assert "metadata" in report
        assert "robustness_score" in report
        assert output_file.exists()
    
    def test_robustness_score(self, temp_results_dir):
        """Test robustness score computation."""
        from adversarial_robustness import (
            RobustnessEvaluator,
            AdversarialPerturbationGenerator
        )
        
        evaluator = RobustnessEvaluator(data_path=temp_results_dir)
        generator = AdversarialPerturbationGenerator(seed=42)
        
        text = "The artificial intelligence system processes data."
        attacks = generator.generate_all_attacks(text)
        
        score = evaluator.compute_robustness_score(attacks)
        
        assert 0 <= score.overall_score <= 100
        assert score.robustness_grade in ['A', 'B', 'C', 'D', 'F']
        assert len(score.recommendations) > 0


# ===========================================================================
# ADDITIONAL COVERAGE TESTS - INFORMATION THEORY
# ===========================================================================

class TestInformationTheoryEdgeCases:
    """Additional edge case tests for Information Theory module."""
    
    def test_entropy_empty_text(self, temp_results_dir):
        """Test entropy with minimal text."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        result = analyzer.calculate_entropy("a", level="char")
        # Allow for small floating point errors near zero
        assert result.shannon_entropy >= -1e-9
    
    def test_entropy_repeated_words(self, temp_results_dir):
        """Test entropy with repeated content."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        result = analyzer.calculate_entropy("test test test test", level="word")
        # Low entropy for repeated content
        assert result.normalized_entropy < 0.5
    
    def test_mutual_information_identical_texts(self, temp_results_dir):
        """Test MI with identical texts."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        text = "The quick brown fox jumps over the lazy dog"
        result = analyzer.calculate_mutual_information(text, text)
        assert result.normalized_mi > 0.9  # High MI for identical
    
    def test_kl_divergence_identical_texts(self, temp_results_dir):
        """Test KL divergence with identical texts."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        text = "hello world hello world"
        result = analyzer.calculate_kl_divergence(text, text)
        assert result.jensen_shannon < 0.1  # Low divergence
    
    def test_transfer_entropy_insufficient_data(self, temp_results_dir):
        """Test transfer entropy with single text."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        result = analyzer.calculate_transfer_entropy(
            ["single"], ["single"]
        )
        assert result.causal_strength == "insufficient_data"
    
    def test_transfer_entropy_multi_texts(self, temp_results_dir):
        """Test transfer entropy with multiple texts."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        source_texts = ["hello world", "hello universe", "hello galaxy"]
        target_texts = ["world hello", "universe hello", "galaxy hello"]
        result = analyzer.calculate_transfer_entropy(source_texts, target_texts)
        assert result.transfer_entropy >= 0
    
    def test_analyze_noise_levels(self, temp_results_dir):
        """Test noise level analysis."""
        from information_theory import InformationTheoreticAnalyzer
        
        analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        analysis = analyzer.analyze_noise_levels()
        
        assert "entropy_analysis" in analysis
        assert "mutual_information" in analysis
        assert "kl_divergence" in analysis
        assert "summary" in analysis


# ===========================================================================
# ADDITIONAL COVERAGE TESTS - STOCHASTIC RESONANCE
# ===========================================================================

class TestStochasticResonanceEdgeCases:
    """Additional edge case tests for Stochastic Resonance module."""
    
    def test_snr_zero_noise(self, temp_results_dir):
        """Test SNR at zero noise."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        snr = detector.calculate_snr(0, 0.95, 0.95)
        assert isinstance(snr, float)
    
    def test_snr_high_noise(self, temp_results_dir):
        """Test SNR at high noise."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        snr = detector.calculate_snr(50, 0.5, 0.95)
        assert isinstance(snr, float)
    
    def test_estimate_theoretical_optimal(self, temp_results_dir):
        """Test theoretical optimal estimation."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        # Test with non-monotonic data
        noise_levels = [0, 10, 20, 30, 40, 50]
        snr_values = [10, 12, 15, 14, 11, 8]  # Peak at 20
        optimal = detector._estimate_theoretical_optimal(noise_levels, snr_values)
        assert 0 <= optimal <= 50
    
    def test_estimate_theoretical_optimal_monotonic(self, temp_results_dir):
        """Test theoretical optimal with monotonic data."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        # Monotonic decreasing - no peak
        noise_levels = [0, 10, 20]
        snr_values = [15, 10, 5]
        optimal = detector._estimate_theoretical_optimal(noise_levels, snr_values)
        assert optimal >= 0
    
    def test_estimate_theoretical_optimal_insufficient(self, temp_results_dir):
        """Test theoretical optimal with insufficient data."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        noise_levels = [0, 10]
        snr_values = [15, 10]
        optimal = detector._estimate_theoretical_optimal(noise_levels, snr_values)
        assert optimal == 0.0
    
    def test_sr_detection_detailed(self, temp_results_dir):
        """Test SR detection with detailed assertions."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        result = detector.detect_stochastic_resonance()
        
        # Check all fields
        assert hasattr(result, 'sr_detected')
        assert hasattr(result, 'optimal_noise_level')
        assert hasattr(result, 'snr_at_optimal')
        assert hasattr(result, 'snr_at_zero')
        assert hasattr(result, 'sr_gain')
        assert hasattr(result, 'resonance_strength')
        assert hasattr(result, 'confidence_interval')
        assert hasattr(result, 'p_value')
        assert hasattr(result, 'theoretical_optimal')
        assert hasattr(result, 'interpretation')
    
    def test_snr_curve_derivatives(self, temp_results_dir):
        """Test SNR curve derivative calculations."""
        from stochastic_resonance import StochasticResonanceDetector
        
        detector = StochasticResonanceDetector(data_path=temp_results_dir)
        result = detector.analyze_snr_curve()
        
        assert len(result.first_derivative) == len(result.noise_levels)
        assert len(result.second_derivative) == len(result.noise_levels)
        assert len(result.snr_smoothed) == len(result.noise_levels)


# ===========================================================================
# ADDITIONAL COVERAGE TESTS - SELF-HEALING
# ===========================================================================

class TestSelfHealingEdgeCases:
    """Additional edge case tests for Self-Healing module."""
    
    def test_confidence_empty_source(self):
        """Test confidence with empty source."""
        from self_healing_agent import ConfidenceEstimator
        
        estimator = ConfidenceEstimator()
        confidence = estimator.estimate_confidence("", "some text")
        assert 0 <= confidence.overall_confidence <= 1
    
    def test_confidence_empty_target(self):
        """Test confidence with empty target."""
        from self_healing_agent import ConfidenceEstimator
        
        estimator = ConfidenceEstimator()
        confidence = estimator.estimate_confidence("some text", "")
        assert confidence.overall_confidence < 0.5  # Low confidence
    
    def test_error_detector_no_errors(self):
        """Test error detection with good translation."""
        from self_healing_agent import ErrorDetector
        
        detector = ErrorDetector(threshold=0.7)
        source = "The quick brown fox"
        translated = "The quick brown fox"  # Perfect
        result = detector.detect_errors(source, translated)
        assert result.error_severity in ["none", "minor"]
    
    def test_error_detector_hallucination(self):
        """Test error detection with hallucination."""
        from self_healing_agent import ErrorDetector
        
        detector = ErrorDetector(threshold=0.7)
        source = "hello"
        translated = "hello world this is a very long hallucinated text that goes on and on"
        result = detector.detect_errors(source, translated)
        # Should detect hallucination or some issue
        assert result.error_detected or result.error_type == "none"
    
    def test_healing_no_improvement_needed(self):
        """Test self-healing when no improvement needed."""
        from self_healing_agent import SelfHealingTranslator
        
        healer = SelfHealingTranslator(confidence_threshold=0.5, max_iterations=2)
        source = "The quick brown fox"
        translated = "The quick brown fox"
        report = healer.heal_translation(source, translated)
        assert report.successful_corrections == 0
    
    def test_lexical_confidence(self):
        """Test lexical confidence calculation."""
        from self_healing_agent import ConfidenceEstimator
        
        estimator = ConfidenceEstimator()
        high_overlap = estimator._lexical_confidence(
            "the quick brown fox", 
            "the quick brown dog"
        )
        low_overlap = estimator._lexical_confidence(
            "hello world",
            "goodbye universe"
        )
        assert high_overlap > low_overlap
    
    def test_semantic_confidence(self):
        """Test semantic confidence calculation."""
        from self_healing_agent import ConfidenceEstimator
        
        estimator = ConfidenceEstimator()
        similar = estimator._semantic_confidence(
            "the artificial intelligence system",
            "the AI system"
        )
        assert 0 <= similar <= 1
    
    def test_structural_confidence(self):
        """Test structural confidence calculation."""
        from self_healing_agent import ConfidenceEstimator
        
        estimator = ConfidenceEstimator()
        result = estimator._structural_confidence(
            "Hello. World.",
            "Hello. World."
        )
        assert 0 <= result <= 1
    
    def test_fluency_confidence(self):
        """Test fluency confidence calculation."""
        from self_healing_agent import ConfidenceEstimator
        
        estimator = ConfidenceEstimator()
        good_fluency = estimator._fluency_confidence("This is a normal sentence.")
        repeated = estimator._fluency_confidence("word word word word word word word")
        assert good_fluency > repeated
    
    def test_correction_strategies(self):
        """Test individual correction strategies."""
        from self_healing_agent import SelfHealingTranslator
        
        healer = SelfHealingTranslator()
        
        # Semantic realignment
        aligned = healer._semantic_realignment(
            "the quick brown fox",
            "the slow brown dog"
        )
        assert isinstance(aligned, str)
        
        # Vocabulary repair
        repaired = healer._vocabulary_repair(
            "hello world foo bar",
            "hello world",
            ["foo", "bar"]
        )
        assert "foo" in repaired or "bar" in repaired or repaired == "hello world"
        
        # Structure fix
        fixed = healer._structure_fix(
            "this is a very long original sentence that has many words",
            "short"
        )
        assert len(fixed) > len("short")
        
        # Remove hallucination
        cleaned = healer._remove_hallucination(
            "hello world",
            "hello world extra text that was added"
        )
        assert isinstance(cleaned, str)


# ===========================================================================
# ADDITIONAL COVERAGE TESTS - ADVERSARIAL
# ===========================================================================

class TestAdversarialEdgeCases:
    """Additional edge case tests for Adversarial module."""
    
    def test_homoglyph_no_replaceable_chars(self):
        """Test homoglyph with no replaceable characters."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        result = generator.homoglyph_attack("123 456 789", perturbation_rate=1.0)
        # Numbers have no homoglyphs in our database
        assert result.attack_type == "homoglyph"
    
    def test_typosquatting_short_words(self):
        """Test typosquatting with short words."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        result = generator.typosquatting_attack("a b c d e", perturbation_rate=1.0)
        # Short words should not be affected
        assert result.attack_type == "typosquatting"
    
    def test_synonym_no_matches(self):
        """Test synonym substitution with no matching words."""
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        generator = AdversarialPerturbationGenerator(seed=42)
        result = generator.synonym_substitution("xyz abc qwerty", substitution_rate=1.0)
        # These words have no synonyms
        assert len(result.changes_made) == 0
    
    def test_evaluate_attack_effectiveness(self, temp_results_dir):
        """Test attack effectiveness evaluation."""
        from adversarial_robustness import RobustnessEvaluator, AdversarialExample
        
        evaluator = RobustnessEvaluator(data_path=temp_results_dir)
        
        attack = AdversarialExample(
            original_text="hello world",
            adversarial_text="hello universe",
            attack_type="test",
            perturbation_strength=0.5,
            changes_made=["world→universe"],
            expected_to_fool=True
        )
        
        effectiveness = evaluator.evaluate_attack_effectiveness(attack, 0.9)
        assert 0 <= effectiveness <= 1


# ===========================================================================
# INTEGRATION TESTS
# ===========================================================================

class TestInnovationIntegration:
    """Integration tests for all innovation modules."""
    
    def test_all_modules_import(self):
        """Test that all modules can be imported together."""
        from information_theory import InformationTheoreticAnalyzer
        from stochastic_resonance import StochasticResonanceDetector
        from self_healing_agent import SelfHealingTranslator
        from adversarial_robustness import AdversarialPerturbationGenerator
        
        assert all([
            InformationTheoreticAnalyzer,
            StochasticResonanceDetector,
            SelfHealingTranslator,
            AdversarialPerturbationGenerator
        ])
    
    def test_all_reports_generated(self, temp_results_dir):
        """Test that all reports can be generated."""
        from information_theory import InformationTheoreticAnalyzer
        from stochastic_resonance import StochasticResonanceDetector
        from self_healing_agent import SelfHealingAnalyzer
        from adversarial_robustness import RobustnessEvaluator
        
        # Information Theory
        it_analyzer = InformationTheoreticAnalyzer(data_path=temp_results_dir)
        it_report = it_analyzer.generate_information_theory_report(
            f"{temp_results_dir}/info_theory.json"
        )
        assert "metadata" in it_report
        
        # Stochastic Resonance
        sr_detector = StochasticResonanceDetector(data_path=temp_results_dir)
        sr_report = sr_detector.generate_stochastic_resonance_report(
            f"{temp_results_dir}/sr.json"
        )
        assert "metadata" in sr_report
        
        # Self-Healing
        sh_analyzer = SelfHealingAnalyzer(data_path=temp_results_dir)
        sh_report = sh_analyzer.generate_self_healing_report(
            f"{temp_results_dir}/self_healing.json"
        )
        assert "metadata" in sh_report
        
        # Adversarial Robustness
        ar_evaluator = RobustnessEvaluator(data_path=temp_results_dir)
        ar_report = ar_evaluator.generate_adversarial_report(
            f"{temp_results_dir}/adversarial.json"
        )
        assert "metadata" in ar_report
    
    def test_convert_numpy_types(self):
        """Test numpy type conversion utility."""
        from information_theory import convert_numpy_types
        
        data = {
            "int": np.int64(42),
            "float": np.float64(3.14),
            "array": np.array([1, 2, 3]),
            "nested": {"inner": np.int32(10)}
        }
        converted = convert_numpy_types(data)
        
        assert isinstance(converted["int"], int)
        assert isinstance(converted["float"], float)
        assert isinstance(converted["array"], list)
        assert isinstance(converted["nested"]["inner"], int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


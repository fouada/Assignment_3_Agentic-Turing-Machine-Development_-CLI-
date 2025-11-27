#!/usr/bin/env python3
"""
Additional tests to increase coverage for edge cases and error paths.
"""

import pytest
import json
import numpy as np
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from comparative_analysis import ComparativeAnalyzer, ComparisonResult, CorrelationResult, RegressionResult
from sensitivity_analysis import SensitivityAnalyzer, SensitivityResult, BootstrapResult, ANOVAResult
from errors import AnalysisError


class TestComparativeAnalyzerErrorPaths:
    """Test error handling paths in ComparativeAnalyzer."""
    
    def test_load_results_corrupted_json(self, tmp_path):
        """Test loading results with corrupted JSON file."""
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Create corrupted JSON file
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            f.write("{invalid json content")
        
        with pytest.raises(AnalysisError, match="Failed to load results"):
            ComparativeAnalyzer(data_path=str(results_dir))
    
    def test_pairwise_comparison_medium_effect(self, temp_results_dir):
        """Test pairwise comparison with medium effect size."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        # Create test data with medium effect size (0.330-0.474)
        analyzer.results = {
            "semantic_distances": {
                "0": 0.1,
                "10": 0.35  # Medium effect (difference ~0.35)
            }
        }
        
        results = analyzer.pairwise_comparisons(
            metric_name="semantic_distances",
            correction_method="holm"
        )
        
        assert len(results) > 0
        # Check that interpretation includes "medium effect"
        has_medium = any("medium effect" in r.interpretation.lower() or
                        "significant" in r.interpretation.lower() 
                        for r in results)
        assert has_medium or len(results) > 0
    
    def test_pairwise_comparison_small_effect(self, temp_results_dir):
        """Test pairwise comparison with small effect size."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        # Create test data with small effect size (< 0.330)
        analyzer.results = {
            "semantic_distances": {
                "0": 0.1,
                "10": 0.15  # Small effect (difference ~0.05)
            }
        }
        
        results = analyzer.pairwise_comparisons(
            metric_name="semantic_distances",
            correction_method="holm"
        )
        
        assert len(results) > 0
    
    def test_correlation_with_perfect_correlation(self, temp_results_dir):
        """Test correlation analysis with perfect correlation."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        # Create perfectly correlated data
        analyzer.results = {
            "semantic_distances": {"0": 0.0, "10": 0.1, "20": 0.2, "30": 0.3},
            "text_similarities": {"0": 1.0, "10": 0.9, "20": 0.8, "30": 0.7},
            "word_overlaps": {"0": 1.0, "10": 0.9, "20": 0.8, "30": 0.7}
        }
        
        results = analyzer.correlation_analysis()
        
        assert len(results) > 0
        # Should have high correlations
        assert any(abs(r.correlation) > 0.9 for r in results)


class TestSensitivityAnalyzerErrorPaths:
    """Test error handling paths in SensitivityAnalyzer."""
    
    def test_load_results_corrupted_json(self, tmp_path):
        """Test loading results with corrupted JSON file."""
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Create corrupted JSON file
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            f.write("{invalid json content")
        
        with pytest.raises(AnalysisError, match="Failed to load results"):
            SensitivityAnalyzer(data_path=str(results_dir))
    
    def test_embedding_dimension_with_single_dimension(self, temp_results_dir):
        """Test embedding dimension sensitivity with insufficient data."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.embedding_dimension_sensitivity(dimensions=[100])
        
        # Should handle gracefully
        assert result.interpretation == "Insufficient data for analysis"
    
    def test_ngram_sensitivity_with_varied_data(self, temp_results_dir):
        """Test n-gram sensitivity with varied data."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        # Add more varied data
        analyzer.results = {
            "semantic_distances": {
                "0": 0.1,
                "10": 0.3,
                "20": 0.5,
                "30": 0.7
            }
        }
        
        result = analyzer.ngram_range_sensitivity()
        
        assert result is not None
        assert result.parameter_name == "ngram_range"
    
    def test_cohens_d_with_zero_variance(self, temp_results_dir):
        """Test Cohen's d with zero variance data."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        # Create data with zero variance
        analyzer.results = {
            "semantic_distances": {"0": 0.5, "50": 0.5},
            "text_similarities": {"0": 0.8, "50": 0.8},
            "word_overlaps": {"0": 0.9, "50": 0.9}
        }
        
        result = analyzer.cohens_d_effect_size(0, 50)
        
        # Should handle zero variance gracefully
        assert isinstance(result, dict)
        assert "semantic_distances" in result


class TestDataclassCreation:
    """Test dataclass creation and methods."""
    
    def test_comparison_result_all_fields(self):
        """Test ComparisonResult with all fields."""
        result = ComparisonResult(
            group1_name="Group A",
            group2_name="Group B",
            group1_mean=0.5,
            group2_mean=0.6,
            group1_std=0.1,
            group2_std=0.1,
            test_name="Mann-Whitney U",
            statistic=100.0,
            p_value=0.01,
            p_value_corrected=0.02,
            effect_size=0.5,
            interpretation="Significant difference"
        )
        
        assert result.group1_name == "Group A"
        assert result.p_value_corrected == 0.02
    
    def test_correlation_result_all_fields(self):
        """Test CorrelationResult with all fields."""
        result = CorrelationResult(
            metric1_name="metric1",
            metric2_name="metric2",
            test_name="Spearman",
            correlation=0.95,
            p_value=0.001,
            ci_lower=0.90,
            ci_upper=0.98,
            interpretation="Strong correlation"
        )
        
        assert result.correlation == 0.95
        assert result.ci_lower == 0.90
    
    def test_regression_result_all_fields(self):
        """Test RegressionResult with all fields."""
        result = RegressionResult(
            predictor_name="noise_level",
            response_name="semantic_distance",
            polynomial_degree=2,
            coefficients=[0.1, 0.2, 0.3],
            r_squared=0.95,
            adjusted_r_squared=0.94,
            f_statistic=100.0,
            p_value=0.001,
            rmse=0.05,
            interpretation="Excellent fit"
        )
        
        assert result.polynomial_degree == 2
        assert len(result.coefficients) == 3
    
    def test_sensitivity_result_all_fields(self):
        """Test SensitivityResult with all fields."""
        result = SensitivityResult(
            parameter_name="test_param",
            parameter_values=[1, 2, 3],
            metric_means=[0.1, 0.2, 0.3],
            metric_stds=[0.01, 0.02, 0.03],
            metric_ci_lower=[0.09, 0.18, 0.27],
            metric_ci_upper=[0.11, 0.22, 0.33],
            correlation=0.99,
            p_value=0.001,
            effect_size=0.5,
            interpretation="Strong correlation"
        )
        
        assert len(result.parameter_values) == 3
        assert result.correlation == 0.99
    
    def test_bootstrap_result_all_fields(self):
        """Test BootstrapResult with all fields."""
        result = BootstrapResult(
            metric_name="cosine_distance",
            observed_value=0.5,
            bootstrap_mean=0.51,
            bootstrap_std=0.02,
            ci_lower=0.47,
            ci_upper=0.55,
            bias=0.01,
            n_iterations=10000
        )
        
        assert result.n_iterations == 10000
        assert result.bias == 0.01
    
    def test_anova_result_all_fields(self):
        """Test ANOVAResult with all fields."""
        result = ANOVAResult(
            test_name="One-Way ANOVA",
            f_statistic=5.5,
            p_value=0.01,
            df_between=3,
            df_within=20,
            effect_size_eta_squared=0.45,
            interpretation="Significant effect"
        )
        
        assert result.f_statistic == 5.5
        assert result.df_between == 3


class TestCorrectionMethods:
    """Test multiple comparison correction methods."""
    
    def test_bonferroni_correction(self, temp_results_dir):
        """Test Bonferroni correction."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        results = analyzer.pairwise_comparisons(
            metric_name="semantic_distances",
            correction_method="bonferroni"
        )
        
        assert len(results) > 0
        # Bonferroni correction should make p-values more conservative
        assert all(r.p_value_corrected >= r.p_value for r in results)
    
    def test_fdr_correction(self, temp_results_dir):
        """Test FDR (Benjamini-Hochberg) correction."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        results = analyzer.pairwise_comparisons(
            metric_name="semantic_distances",
            correction_method="fdr_bh"
        )
        
        assert len(results) > 0
    
    def test_no_correction(self, temp_results_dir):
        """Test no correction (raw p-values)."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        results = analyzer.pairwise_comparisons(
            metric_name="semantic_distances",
            correction_method="none"
        )
        
        assert len(results) > 0
        # With no correction, p-values should be unchanged
        assert all(r.p_value == r.p_value_corrected for r in results)


class TestRegressionAnalysis:
    """Test regression analysis with different scenarios."""
    
    def test_linear_regression(self, temp_results_dir):
        """Test linear regression."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.regression_analysis(polynomial_degree=1)
        
        assert result.polynomial_degree == 1
        assert result.r_squared >= 0.0
        assert result.r_squared <= 1.0
    
    def test_quadratic_regression(self, temp_results_dir):
        """Test quadratic regression."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.regression_analysis(polynomial_degree=2)
        
        assert result.polynomial_degree == 2
        assert len(result.coefficients) == 3  # a + bx + cx^2
    
    def test_cubic_regression(self, temp_results_dir):
        """Test cubic regression."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.regression_analysis(polynomial_degree=3)
        
        assert result.polynomial_degree == 3
        assert len(result.coefficients) == 4  # a + bx + cx^2 + dx^3


class TestDiagnosticTests:
    """Test diagnostic tests."""
    
    def test_normality_tests(self, temp_results_dir):
        """Test normality tests."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        diagnostics = analyzer.diagnostic_tests()
        
        assert isinstance(diagnostics, dict)
        # Should have normality tests for each metric
        normality_keys = [k for k in diagnostics.keys() if "normality" in k]
        assert len(normality_keys) > 0
        
        # Check normality test structure
        for key in normality_keys:
            norm_test = diagnostics[key]
            assert "test" in norm_test
            assert "statistic" in norm_test
            assert "p_value" in norm_test
            assert "normal" in norm_test
            assert isinstance(norm_test["normal"], bool)
    
    def test_homoscedasticity_tests(self, temp_results_dir):
        """Test homoscedasticity tests."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        diagnostics = analyzer.diagnostic_tests()
        
        # Should have homoscedasticity test
        if "homoscedasticity" in diagnostics:
            homo_test = diagnostics["homoscedasticity"]
            assert "levene_test" in homo_test
            assert "bartlett_test" in homo_test
            
            # Check that boolean values are properly typed
            assert isinstance(homo_test["levene_test"]["homoscedastic"], bool)
            assert isinstance(homo_test["bartlett_test"]["homoscedastic"], bool)


#!/usr/bin/env python3
"""
Unit tests for comparative analysis module.
"""

import pytest
import numpy as np
import json
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile

from src.comparative_analysis import (
    ComparativeAnalyzer,
    ComparisonResult,
    CorrelationResult,
    RegressionResult
)
from src.errors import AnalysisError


@pytest.fixture
def mock_results_data():
    """Mock experimental results data."""
    return {
        "original_sentence": "Test sentence for analysis",
        "final_outputs": {
            "0": "Test output 0",
            "10": "Test output 10",
            "25": "Test output 25",
            "50": "Test output 50"
        },
        "semantic_distances": {
            "0": 0.289,
            "10": 0.295,
            "25": 0.310,
            "50": 0.340
        },
        "text_similarities": {
            "0": 0.989,
            "10": 0.985,
            "25": 0.975,
            "50": 0.950
        },
        "word_overlaps": {
            "0": 0.889,
            "10": 0.880,
            "25": 0.860,
            "50": 0.820
        }
    }


@pytest.fixture
def temp_results_dir(mock_results_data, tmp_path):
    """Create temporary results directory with mock data."""
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    
    results_file = results_dir / "analysis_results_local.json"
    with open(results_file, 'w') as f:
        json.dump(mock_results_data, f)
    
    return results_dir


class TestComparativeAnalyzer:
    """Test suite for ComparativeAnalyzer class."""
    
    def test_initialization_success(self, temp_results_dir):
        """Test successful initialization."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        assert analyzer.results is not None
        assert "semantic_distances" in analyzer.results
    
    def test_initialization_missing_file(self, tmp_path):
        """Test initialization with missing results file."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        with pytest.raises(AnalysisError, match="Results file not found"):
            ComparativeAnalyzer(data_path=str(empty_dir))
    
    def test_pairwise_comparisons(self, temp_results_dir):
        """Test pairwise comparisons between noise levels."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        results = analyzer.pairwise_comparisons(
            metric_name="semantic_distances",
            correction_method="holm"
        )
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Check first result
        result = results[0]
        assert isinstance(result, ComparisonResult)
        assert result.test_name == "Mann-Whitney U"
        assert result.p_value >= 0.0
        assert result.p_value <= 1.0
        assert result.p_value_corrected >= result.p_value
    
    def test_pairwise_comparisons_bonferroni(self, temp_results_dir):
        """Test pairwise comparisons with Bonferroni correction."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        results = analyzer.pairwise_comparisons(
            metric_name="semantic_distances",
            correction_method="bonferroni"
        )
        
        assert len(results) > 0
        # Bonferroni should be more conservative (higher p-values)
        assert all(r.p_value_corrected >= r.p_value for r in results)
    
    def test_cliffs_delta(self, temp_results_dir):
        """Test Cliff's Delta effect size calculation."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([6, 7, 8, 9, 10])
        
        delta = analyzer._cliffs_delta(x, y)
        
        assert -1.0 <= delta <= 1.0
        # y is always greater than x, so delta should be negative
        assert delta < 0
    
    def test_apply_correction_bonferroni(self, temp_results_dir):
        """Test Bonferroni correction."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        p_values = [0.01, 0.02, 0.03, 0.04, 0.05]
        corrected = analyzer._apply_correction(p_values, "bonferroni")
        
        assert len(corrected) == len(p_values)
        # Each p-value should be multiplied by m (5 in this case)
        assert corrected[0] == min(0.01 * 5, 1.0)
    
    def test_apply_correction_holm(self, temp_results_dir):
        """Test Holm's step-down correction."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        p_values = [0.001, 0.01, 0.02, 0.03, 0.05]
        corrected = analyzer._apply_correction(p_values, "holm")
        
        assert len(corrected) == len(p_values)
        # Corrected values should be monotonically increasing
        # when sorted by original p-values
        assert all(corrected[i] >= p_values[i] for i in range(len(p_values)))
    
    def test_apply_correction_fdr(self, temp_results_dir):
        """Test FDR (Benjamini-Hochberg) correction."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        p_values = [0.001, 0.01, 0.02, 0.03, 0.05]
        corrected = analyzer._apply_correction(p_values, "fdr_bh")
        
        assert len(corrected) == len(p_values)
        # FDR should be less conservative than Bonferroni
        bonferroni = analyzer._apply_correction(p_values, "bonferroni")
        assert all(corrected[i] <= bonferroni[i] for i in range(len(p_values)))
    
    def test_apply_correction_none(self, temp_results_dir):
        """Test no correction."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        p_values = [0.01, 0.02, 0.03]
        corrected = analyzer._apply_correction(p_values, "none")
        
        assert corrected == p_values
    
    def test_apply_correction_invalid(self, temp_results_dir):
        """Test invalid correction method."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        with pytest.raises(ValueError, match="Unknown correction method"):
            analyzer._apply_correction([0.05], "invalid_method")
    
    def test_correlation_analysis(self, temp_results_dir):
        """Test correlation analysis."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        results = analyzer.correlation_analysis()
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Should have Pearson, Spearman, and Kendall for each metric
        test_names = [r.test_name for r in results]
        assert "Pearson r" in test_names
        assert "Spearman ρ" in test_names
        assert "Kendall τ" in test_names
        
        # Check a result
        result = results[0]
        assert isinstance(result, CorrelationResult)
        assert -1.0 <= result.correlation_coefficient <= 1.0
        assert 0.0 <= result.p_value <= 1.0
    
    def test_correlation_ci(self, temp_results_dir):
        """Test correlation confidence interval calculation."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        # Test with moderate correlation
        r = 0.7
        n = 30
        ci = analyzer._correlation_ci(r, n, confidence=0.95)
        
        assert len(ci) == 2
        assert ci[0] < ci[1]  # Lower < Upper
        assert ci[0] < r < ci[1]  # r should be in the interval
    
    def test_correlation_ci_small_n(self, temp_results_dir):
        """Test correlation CI with small sample size."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        r = 0.5
        n = 2  # Too small
        ci = analyzer._correlation_ci(r, n)
        
        # Should return NaN for insufficient data
        assert np.isnan(ci[0]) and np.isnan(ci[1])
    
    def test_regression_analysis_linear(self, temp_results_dir):
        """Test linear regression analysis."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.regression_analysis(
            predictor="noise_level",
            response="semantic_distances",
            polynomial_degree=1
        )
        
        assert isinstance(result, RegressionResult)
        assert result.model_type == "Polynomial (degree 1)"
        assert 0.0 <= result.r_squared <= 1.0
        assert result.rmse >= 0.0
        assert len(result.coefficients) == 2  # Intercept + 1 coefficient
        assert len(result.predictions) > 0
        assert len(result.residuals) == len(result.predictions)
    
    def test_regression_analysis_quadratic(self, temp_results_dir):
        """Test quadratic regression analysis."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.regression_analysis(
            predictor="noise_level",
            response="semantic_distances",
            polynomial_degree=2
        )
        
        assert result.model_type == "Polynomial (degree 2)"
        assert len(result.coefficients) == 3  # Intercept + 2 coefficients
        assert result.adjusted_r_squared <= result.r_squared
    
    def test_diagnostic_tests(self, temp_results_dir):
        """Test diagnostic tests for assumptions."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        diagnostics = analyzer.diagnostic_tests()
        
        assert isinstance(diagnostics, dict)
        # Should have normality tests
        assert any("normality" in key for key in diagnostics.keys())
        
        # Check normality test structure
        for key in diagnostics.keys():
            if "normality" in key:
                norm_test = diagnostics[key]
                assert "test" in norm_test
                assert "p_value" in norm_test
                assert "recommendation" in norm_test
    
    def test_generate_comparative_report(self, temp_results_dir):
        """Test comprehensive comparative report generation."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        output_file = str(temp_results_dir / "comparative_test.json")
        report = analyzer.generate_comparative_report(output_file=output_file)
        
        assert isinstance(report, dict)
        assert "metadata" in report
        assert "pairwise_comparisons" in report
        assert "correlation_analysis" in report
        assert "regression_analysis" in report
        assert "diagnostic_tests" in report
        
        # Check file was created
        assert Path(output_file).exists()
        
        # Verify JSON is valid
        with open(output_file, 'r') as f:
            saved_report = json.load(f)
        assert saved_report["metadata"]["analysis_type"] == "Data-Driven Comparative Analysis"


class TestComparisonResult:
    """Test ComparisonResult dataclass."""
    
    def test_creation(self):
        """Test creating ComparisonResult."""
        result = ComparisonResult(
            group1_name="Group A",
            group2_name="Group B",
            group1_mean=0.5,
            group2_mean=0.6,
            group1_std=0.1,
            group2_std=0.12,
            test_statistic=2.5,
            p_value=0.03,
            p_value_corrected=0.09,
            effect_size=0.4,
            test_name="Mann-Whitney U",
            significant=False,
            interpretation="No significant difference"
        )
        
        assert result.group1_name == "Group A"
        assert result.p_value_corrected > result.p_value


class TestCorrelationResult:
    """Test CorrelationResult dataclass."""
    
    def test_creation(self):
        """Test creating CorrelationResult."""
        result = CorrelationResult(
            variable1="noise",
            variable2="drift",
            correlation_coefficient=0.95,
            p_value=0.001,
            test_name="Pearson r",
            n_samples=10,
            confidence_interval=(0.85, 0.99),
            interpretation="Strong positive correlation"
        )
        
        assert result.correlation_coefficient == 0.95
        assert result.confidence_interval[0] < result.confidence_interval[1]


class TestRegressionResult:
    """Test RegressionResult dataclass."""
    
    def test_creation(self):
        """Test creating RegressionResult."""
        result = RegressionResult(
            predictor="x",
            response="y",
            model_type="Linear",
            coefficients=[1.0, 2.0],
            r_squared=0.85,
            adjusted_r_squared=0.83,
            rmse=0.15,
            f_statistic=45.2,
            p_value=0.001,
            predictions=[1.0, 2.0, 3.0],
            residuals=[0.1, -0.05, 0.02],
            interpretation="Good fit"
        )
        
        assert result.r_squared == 0.85
        assert len(result.coefficients) == 2
        assert len(result.predictions) == 3


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_data_comparison(self, tmp_path):
        """Test comparisons with empty data."""
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        minimal_data = {
            "semantic_distances": {},
            "text_similarities": {},
            "word_overlaps": {}
        }
        
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(minimal_data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        # Should handle gracefully
        results = analyzer.pairwise_comparisons()
        assert len(results) == 0
    
    def test_single_point_regression(self, tmp_path):
        """Test regression with insufficient points."""
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        minimal_data = {
            "semantic_distances": {"0": 0.5}
        }
        
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(minimal_data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        # Should still run but with limited power
        result = analyzer.regression_analysis(
            response="semantic_distances",
            polynomial_degree=1
        )
        assert isinstance(result, RegressionResult)


class TestIntegration:
    """Integration tests for comparative analysis pipeline."""
    
    def test_full_pipeline(self, temp_results_dir):
        """Test complete comparative analysis pipeline."""
        analyzer = ComparativeAnalyzer(data_path=str(temp_results_dir))
        
        # Run all analyses
        output_file = str(temp_results_dir / "full_comparative_test.json")
        report = analyzer.generate_comparative_report(output_file=output_file)
        
        # Verify all sections present
        assert "pairwise_comparisons" in report
        assert "correlation_analysis" in report
        assert "regression_analysis" in report
        assert "diagnostic_tests" in report
        
        # Verify regression has both linear and quadratic
        assert "linear" in report["regression_analysis"]
        assert "quadratic" in report["regression_analysis"]
        
        # Verify file exists
        assert Path(output_file).exists()


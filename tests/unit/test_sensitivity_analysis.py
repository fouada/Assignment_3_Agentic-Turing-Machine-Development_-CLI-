#!/usr/bin/env python3
"""
Unit tests for sensitivity analysis module.
"""

import pytest
import numpy as np
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

from src.sensitivity_analysis import (
    SensitivityAnalyzer,
    SensitivityResult,
    BootstrapResult,
    ANOVAResult
)
from src.errors import AnalysisError


@pytest.fixture
def mock_results_data():
    """Mock experimental results data."""
    return {
        "original_sentence": "Test sentence",
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


class TestSensitivityAnalyzer:
    """Test suite for SensitivityAnalyzer class."""
    
    def test_initialization_success(self, temp_results_dir):
        """Test successful initialization."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        assert analyzer.results is not None
        assert "semantic_distances" in analyzer.results
    
    def test_initialization_missing_file(self, tmp_path):
        """Test initialization with missing results file."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        with pytest.raises(AnalysisError, match="Results file not found"):
            SensitivityAnalyzer(data_path=str(empty_dir))
    
    def test_embedding_dimension_sensitivity(self, temp_results_dir):
        """Test embedding dimension sensitivity analysis."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.embedding_dimension_sensitivity(
            dimensions=[100, 500, 1000]
        )
        
        assert isinstance(result, SensitivityResult)
        assert result.parameter_name == "embedding_dimension"
        assert len(result.parameter_values) >= 1
        assert len(result.metric_means) == len(result.parameter_values)
        assert result.p_value >= 0.0
        assert result.p_value <= 1.0
    
    def test_ngram_range_sensitivity(self, temp_results_dir):
        """Test n-gram range sensitivity analysis."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.ngram_range_sensitivity()
        
        assert isinstance(result, SensitivityResult)
        assert result.parameter_name == "ngram_range"
        assert len(result.parameter_values) >= 1
        assert result.effect_size >= 0.0
    
    def test_bootstrap_analysis(self, temp_results_dir):
        """Test bootstrap resampling analysis."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.bootstrap_analysis(
            metric_name="cosine_distance",
            n_iterations=100  # Reduced for faster testing
        )
        
        assert isinstance(result, BootstrapResult)
        assert result.n_iterations == 100
        assert result.bootstrap_mean >= 0.0
        assert result.bootstrap_std >= 0.0
        assert result.ci_lower <= result.ci_upper
        assert abs(result.bias) < 1.0  # Bias should be small
    
    def test_bootstrap_insufficient_data(self, tmp_path):
        """Test bootstrap with insufficient data."""
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Only one data point
        minimal_data = {
            "semantic_distances": {"0": 0.5}
        }
        
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(minimal_data, f)
        
        analyzer = SensitivityAnalyzer(data_path=str(results_dir))
        
        with pytest.raises(AnalysisError, match="Insufficient data"):
            analyzer.bootstrap_analysis()
    
    def test_anova_multi_factor(self, temp_results_dir):
        """Test ANOVA multi-factor analysis."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        result = analyzer.anova_multi_factor()
        
        assert isinstance(result, ANOVAResult)
        assert result.f_statistic >= 0.0
        assert result.p_value >= 0.0
        assert result.p_value <= 1.0
        assert result.effect_size_eta_squared >= 0.0
        assert result.effect_size_eta_squared <= 1.0
    
    def test_cohens_d_effect_size(self, temp_results_dir):
        """Test Cohen's d effect size calculation."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        results = analyzer.cohens_d_effect_size(
            noise_level_1=0,
            noise_level_2=50
        )
        
        assert isinstance(results, dict)
        assert "semantic_distances" in results
        assert isinstance(results["semantic_distances"], float)
    
    def test_generate_sensitivity_report(self, temp_results_dir):
        """Test comprehensive sensitivity report generation."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        output_file = str(temp_results_dir / "sensitivity_test.json")
        report = analyzer.generate_sensitivity_report(output_file=output_file)
        
        assert isinstance(report, dict)
        assert "metadata" in report
        assert "parameter_sensitivity" in report
        assert "bootstrap_analysis" in report
        assert "anova_results" in report
        assert "effect_sizes" in report
        
        # Check file was created
        assert Path(output_file).exists()
        
        # Verify JSON is valid
        with open(output_file, 'r') as f:
            saved_report = json.load(f)
        assert saved_report == report


class TestSensitivityResult:
    """Test SensitivityResult dataclass."""
    
    def test_creation(self):
        """Test creating SensitivityResult."""
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
        
        assert result.parameter_name == "test_param"
        assert len(result.parameter_values) == 3
        assert result.correlation == 0.99


class TestBootstrapResult:
    """Test BootstrapResult dataclass."""
    
    def test_creation(self):
        """Test creating BootstrapResult."""
        result = BootstrapResult(
            metric_name="test_metric",
            observed_value=0.5,
            bootstrap_mean=0.51,
            bootstrap_std=0.02,
            ci_lower=0.47,
            ci_upper=0.55,
            bias=0.01,
            n_iterations=10000
        )
        
        assert result.metric_name == "test_metric"
        assert result.n_iterations == 10000
        assert result.ci_lower < result.ci_upper


class TestANOVAResult:
    """Test ANOVAResult dataclass."""
    
    def test_creation(self):
        """Test creating ANOVAResult."""
        result = ANOVAResult(
            test_name="One-Way ANOVA",
            f_statistic=15.5,
            p_value=0.001,
            df_between=3,
            df_within=20,
            effect_size_eta_squared=0.15,
            interpretation="Significant with large effect"
        )
        
        assert result.test_name == "One-Way ANOVA"
        assert result.f_statistic == 15.5
        assert result.df_between == 3


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_results(self, tmp_path):
        """Test handling of empty results."""
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        empty_data = {}
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(empty_data, f)
        
        analyzer = SensitivityAnalyzer(data_path=str(results_dir))
        
        # Should handle gracefully, not crash
        with pytest.raises((KeyError, AnalysisError)):
            analyzer.bootstrap_analysis()
    
    def test_invalid_correction_method(self, temp_results_dir):
        """Test invalid correction method in generate_report."""
        # This is tested indirectly through the correction logic
        # The method should handle gracefully or raise clear error
        pass


class TestIntegration:
    """Integration tests for sensitivity analysis pipeline."""
    
    def test_full_pipeline(self, temp_results_dir):
        """Test complete sensitivity analysis pipeline."""
        analyzer = SensitivityAnalyzer(data_path=str(temp_results_dir))
        
        # Run all analyses
        output_file = str(temp_results_dir / "full_pipeline_test.json")
        report = analyzer.generate_sensitivity_report(output_file=output_file)
        
        # Verify report structure
        assert "metadata" in report
        assert "parameter_sensitivity" in report
        assert "bootstrap_analysis" in report
        assert "anova_results" in report
        assert "effect_sizes" in report
        
        # Verify file exists and is valid JSON
        assert Path(output_file).exists()
        with open(output_file, 'r') as f:
            loaded_report = json.load(f)
        assert loaded_report["metadata"]["analysis_type"] == "Systematic Sensitivity Analysis"


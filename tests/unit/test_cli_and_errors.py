#!/usr/bin/env python3
"""
Tests for CLI entry points and error handling paths.
These tests target specific uncovered lines to achieve >85% coverage.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import numpy as np

from errors import AnalysisError
from comparative_analysis import main as comparative_main
from sensitivity_analysis import main as sensitivity_main


class TestMainFunctions:
    """Test the main() entry point functions."""

    def test_comparative_main_runs(self, tmp_path, capsys):
        """Test that comparative_analysis.main() runs without errors."""
        # Create test data
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4},
            "text_similarities": {"0": 0.9, "10": 0.8, "20": 0.7, "30": 0.6},
            "word_overlaps": {"0": 0.95, "10": 0.85, "20": 0.75, "30": 0.65}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        # Patch the default path
        with patch('comparative_analysis.ComparativeAnalyzer') as MockAnalyzer:
            mock_instance = MockAnalyzer.return_value
            mock_instance.generate_comparative_report.return_value = {
                "correlation_analysis": {
                    "results": [
                        {
                            "variable1": "semantic_distances",
                            "variable2": "text_similarities",
                            "test_name": "Pearson",
                            "correlation_coefficient": 0.95,
                            "p_value": 0.001,
                            "interpretation": "Strong correlation"
                        }
                    ]
                },
                "regression_analysis": {
                    "linear": {
                        "r_squared": 0.9,
                        "rmse": 0.01,
                        "interpretation": "Good fit"
                    }
                },
                "diagnostic_tests": {
                    "semantic_distances_normality": {
                        "normal": True,
                        "recommendation": "Use parametric tests"
                    }
                }
            }
            
            comparative_main()
            
            # Verify output was printed
            captured = capsys.readouterr()
            assert "COMPARATIVE ANALYSIS" in captured.out

    def test_sensitivity_main_runs(self, tmp_path, capsys):
        """Test that sensitivity_analysis.main() runs without errors."""
        with patch('sensitivity_analysis.SensitivityAnalyzer') as MockAnalyzer:
            mock_instance = MockAnalyzer.return_value
            mock_instance.generate_sensitivity_report.return_value = {
                "parameter_sensitivity": {
                    "embedding_dimension": {
                        "correlation": 0.5,
                        "p_value": 0.05,
                        "interpretation": "Moderate sensitivity"
                    }
                },
                "bootstrap_analysis": {
                    "cosine_distance": {
                        "observed_value": 0.3,
                        "bootstrap_mean": 0.3,
                        "ci_lower": 0.25,
                        "ci_upper": 0.35,
                        "bias": 0.001
                    }
                },
                "anova_results": {
                    "multi_factor": {
                        "f_statistic": 2.5,
                        "p_value": 0.1,
                        "df_between": 3,
                        "df_within": 20,
                        "effect_size_eta_squared": 0.1,
                        "interpretation": "Small effect"
                    }
                }
            }
            
            sensitivity_main()
            
            # Verify output was printed
            captured = capsys.readouterr()
            assert "SENSITIVITY ANALYSIS" in captured.out

    def test_comparative_main_missing_keys(self, capsys):
        """Test main() handles missing report keys gracefully."""
        with patch('comparative_analysis.ComparativeAnalyzer') as MockAnalyzer:
            mock_instance = MockAnalyzer.return_value
            # Return minimal report
            mock_instance.generate_comparative_report.return_value = {}
            
            comparative_main()
            
            captured = capsys.readouterr()
            assert "COMPARATIVE ANALYSIS COMPLETE" in captured.out

    def test_sensitivity_main_partial_report(self, capsys):
        """Test main() handles partial report gracefully."""
        with patch('sensitivity_analysis.SensitivityAnalyzer') as MockAnalyzer:
            mock_instance = MockAnalyzer.return_value
            # Return partial report
            mock_instance.generate_sensitivity_report.return_value = {
                "parameter_sensitivity": {},
                "bootstrap_analysis": {},
                "anova_results": {}
            }
            
            sensitivity_main()
            
            captured = capsys.readouterr()
            assert "SENSITIVITY ANALYSIS COMPLETE" in captured.out


class TestComparativeAnalyzerCLI:
    """Test CLI-related functionality for ComparativeAnalyzer."""

    def test_main_function_exists(self):
        """Test that main function can be imported."""
        from comparative_analysis import main
        assert callable(main)

    def test_analyzer_with_valid_data(self, tmp_path):
        """Test analyzer initialization with valid data."""
        from comparative_analysis import ComparativeAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4},
            "text_similarities": {"0": 0.9, "10": 0.8, "20": 0.7, "30": 0.6},
            "word_overlaps": {"0": 0.95, "10": 0.85, "20": 0.75, "30": 0.65}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        assert analyzer.results is not None
        assert "semantic_distances" in analyzer.results

    def test_pairwise_comparisons_handles_exceptions(self, tmp_path):
        """Test that pairwise_comparisons handles statistical exceptions gracefully."""
        from comparative_analysis import ComparativeAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Create valid data
        data = {
            "semantic_distances": {"0": 0.1, "10": 0.2},
            "text_similarities": {"0": 0.9, "10": 0.8},
            "word_overlaps": {"0": 0.95, "10": 0.85}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        # Should return results without crashing
        results = analyzer.pairwise_comparisons()
        assert isinstance(results, list)

    def test_diagnostic_tests_with_small_sample(self, tmp_path):
        """Test diagnostic tests with small sample size."""
        from comparative_analysis import ComparativeAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Very small sample
        data = {
            "semantic_distances": {"0": 0.1},
            "text_similarities": {"0": 0.9},
            "word_overlaps": {"0": 0.95}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        # Should handle gracefully
        diagnostics = analyzer.diagnostic_tests()
        assert isinstance(diagnostics, dict)


class TestSensitivityAnalyzerCLI:
    """Test CLI-related functionality for SensitivityAnalyzer."""

    def test_main_function_exists(self):
        """Test that main function can be imported."""
        from sensitivity_analysis import main
        assert callable(main)

    def test_analyzer_with_valid_data(self, tmp_path):
        """Test analyzer initialization with valid data."""
        from sensitivity_analysis import SensitivityAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = SensitivityAnalyzer(data_path=str(results_dir))
        assert analyzer.results is not None

    def test_bootstrap_with_sufficient_data(self, tmp_path):
        """Test bootstrap analysis with sufficient data."""
        from sensitivity_analysis import SensitivityAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Provide enough data points for bootstrap
        data = {
            "semantic_distances": {
                "0": 0.1, "10": 0.15, "20": 0.2, "30": 0.25, "40": 0.3, "50": 0.35
            },
            "text_similarities": {
                "0": 0.9, "10": 0.85, "20": 0.8, "30": 0.75, "40": 0.7, "50": 0.65
            },
            "word_overlaps": {
                "0": 0.95, "10": 0.9, "20": 0.85, "30": 0.8, "40": 0.75, "50": 0.7
            }
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = SensitivityAnalyzer(data_path=str(results_dir))
        
        # Should work with sufficient data
        result = analyzer.bootstrap_analysis(n_iterations=100)
        assert result is not None
        assert hasattr(result, 'metric_name')


class TestErrorHandlingPaths:
    """Test specific error handling paths."""

    def test_comparative_corrupted_json(self, tmp_path):
        """Test loading corrupted JSON raises AnalysisError."""
        from comparative_analysis import ComparativeAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Create corrupted JSON
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            f.write("{invalid json content")
        
        with pytest.raises(AnalysisError):
            ComparativeAnalyzer(data_path=str(results_dir))

    def test_sensitivity_corrupted_json(self, tmp_path):
        """Test loading corrupted JSON raises AnalysisError."""
        from sensitivity_analysis import SensitivityAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Create corrupted JSON
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            f.write("{invalid json content")
        
        with pytest.raises(AnalysisError):
            SensitivityAnalyzer(data_path=str(results_dir))

    def test_comparative_missing_directory(self, tmp_path):
        """Test missing directory raises AnalysisError."""
        from comparative_analysis import ComparativeAnalyzer
        
        with pytest.raises(AnalysisError):
            ComparativeAnalyzer(data_path=str(tmp_path / "nonexistent"))

    def test_sensitivity_missing_directory(self, tmp_path):
        """Test missing directory raises AnalysisError."""
        from sensitivity_analysis import SensitivityAnalyzer
        
        with pytest.raises(AnalysisError):
            SensitivityAnalyzer(data_path=str(tmp_path / "nonexistent"))


class TestNumpyConversionInAnalysis:
    """Test numpy conversion in real analysis scenarios."""

    def test_comparative_report_handles_numpy(self, tmp_path):
        """Test that comparative report handles numpy types."""
        from comparative_analysis import ComparativeAnalyzer, convert_numpy_types
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4},
            "text_similarities": {"0": 0.9, "10": 0.8, "20": 0.7, "30": 0.6},
            "word_overlaps": {"0": 0.95, "10": 0.85, "20": 0.75, "30": 0.65}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        # Test convert_numpy_types with actual numpy values
        test_data = {
            "int_val": np.int64(42),
            "float_val": np.float64(3.14),
            "bool_val": np.bool_(True),
            "array_val": np.array([1, 2, 3])
        }
        
        converted = convert_numpy_types(test_data)
        
        assert converted["int_val"] == 42
        assert isinstance(converted["int_val"], int)
        assert converted["float_val"] == 3.14
        assert isinstance(converted["float_val"], float)
        assert converted["bool_val"] is True
        assert isinstance(converted["bool_val"], bool)
        assert converted["array_val"] == [1, 2, 3]

    def test_sensitivity_report_handles_numpy(self, tmp_path):
        """Test that sensitivity report handles numpy types."""
        from sensitivity_analysis import convert_numpy_types
        
        test_data = {
            "int_val": np.int64(42),
            "float_val": np.float64(3.14),
            "bool_val": np.bool_(True),
            "nested": {
                "inner_int": np.int32(100),
                "inner_float": np.float32(2.5)
            }
        }
        
        converted = convert_numpy_types(test_data)
        
        assert converted["int_val"] == 42
        assert isinstance(converted["int_val"], int)
        assert converted["nested"]["inner_int"] == 100


class TestReportGeneration:
    """Test report generation functionality."""

    def test_comparative_report_output(self, tmp_path):
        """Test that comparative report can be generated and saved."""
        from comparative_analysis import ComparativeAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4},
            "text_similarities": {"0": 0.9, "10": 0.8, "20": 0.7, "30": 0.6},
            "word_overlaps": {"0": 0.95, "10": 0.85, "20": 0.75, "30": 0.65}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        output_file = results_dir / "test_report.json"
        report = analyzer.generate_comparative_report(output_file=str(output_file))
        
        assert report is not None
        assert output_file.exists()
        
        # Verify the saved file is valid JSON
        with open(output_file) as f:
            saved_report = json.load(f)
        
        assert "metadata" in saved_report

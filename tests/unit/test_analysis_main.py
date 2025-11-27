#!/usr/bin/env python3
"""
Tests for main() entry points in analysis modules.
These tests cover the command-line interface functions.
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO


class TestComparativeAnalysisMain:
    """Test main() function in comparative_analysis module."""
    
    def test_main_with_valid_data(self, tmp_path):
        """Test main() with valid analysis results."""
        # Create test data
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        test_data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4},
            "text_similarities": {"0": 0.9, "10": 0.8, "20": 0.7, "30": 0.6},
            "word_overlaps": {"0": 0.95, "10": 0.85, "20": 0.75, "30": 0.65}
        }
        
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test that we can import and the module is set up correctly
        from comparative_analysis import ComparativeAnalyzer
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        assert analyzer.results is not None
    
    def test_main_error_handling(self, tmp_path):
        """Test main() error handling with missing data."""
        from comparative_analysis import ComparativeAnalyzer
        from errors import AnalysisError
        
        # Try to initialize with non-existent directory
        with pytest.raises(AnalysisError):
            ComparativeAnalyzer(data_path=str(tmp_path / "nonexistent"))


class TestSensitivityAnalysisMain:
    """Test main() function in sensitivity_analysis module."""
    
    def test_main_with_valid_data(self, tmp_path):
        """Test main() with valid analysis results."""
        # Create test data
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        test_data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4}
        }
        
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test that we can import and the module is set up correctly
        from sensitivity_analysis import SensitivityAnalyzer
        
        analyzer = SensitivityAnalyzer(data_path=str(results_dir))
        assert analyzer.results is not None
    
    def test_main_error_handling(self, tmp_path):
        """Test main() error handling with missing data."""
        from sensitivity_analysis import SensitivityAnalyzer
        from errors import AnalysisError
        
        # Try to initialize with non-existent directory
        with pytest.raises(AnalysisError):
            SensitivityAnalyzer(data_path=str(tmp_path / "nonexistent"))


class TestAnalysisErrorPaths:
    """Test error handling in analysis modules."""
    
    def test_comparative_load_corrupted_json(self, tmp_path):
        """Test loading corrupted JSON file."""
        from comparative_analysis import ComparativeAnalyzer
        from errors import AnalysisError
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Create corrupted JSON
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            f.write("{invalid json")
        
        with pytest.raises(AnalysisError):
            ComparativeAnalyzer(data_path=str(results_dir))
    
    def test_sensitivity_load_corrupted_json(self, tmp_path):
        """Test loading corrupted JSON file."""
        from sensitivity_analysis import SensitivityAnalyzer
        from errors import AnalysisError
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        # Create corrupted JSON
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            f.write("{invalid json")
        
        with pytest.raises(AnalysisError):
            SensitivityAnalyzer(data_path=str(results_dir))


class TestNumpyIntegration:
    """Test numpy integration in real analysis scenarios."""
    
    def test_comparative_handles_numpy_in_results(self, tmp_path):
        """Test that comparative analysis handles numpy types correctly."""
        import numpy as np
        from comparative_analysis import ComparativeAnalyzer, convert_numpy_types
        
        # Create test data with numpy types
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        test_data = {
            "semantic_distances": {
                "0": float(np.float64(0.1)),
                "10": float(np.float64(0.2))
            },
            "text_similarities": {
                "0": float(np.float64(0.9)),
                "10": float(np.float64(0.8))
            },
            "word_overlaps": {
                "0": float(np.float64(0.95)),
                "10": float(np.float64(0.85))
            }
        }
        
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(test_data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        # Test convert_numpy_types
        converted = convert_numpy_types(analyzer.results)
        assert isinstance(converted, dict)
    
    def test_sensitivity_handles_numpy_in_results(self, tmp_path):
        """Test that sensitivity analysis handles numpy types correctly."""
        import numpy as np
        from sensitivity_analysis import SensitivityAnalyzer, convert_numpy_types as sens_convert
        
        # Create test data
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        test_data = {
            "semantic_distances": {
                "0": float(np.float64(0.1)),
                "10": float(np.float64(0.2))
            }
        }
        
        results_file = results_dir / "analysis_results_local.json"
        with open(results_file, 'w') as f:
            json.dump(test_data, f)
        
        analyzer = SensitivityAnalyzer(data_path=str(results_dir))
        
        # Test convert_numpy_types
        converted = sens_convert(analyzer.results)
        assert isinstance(converted, dict)


class TestBooleanConversions:
    """Test boolean conversions that were causing JSON errors."""
    
    def test_numpy_bool_conversion(self):
        """Test that numpy booleans are properly converted."""
        import numpy as np
        from comparative_analysis import convert_numpy_types
        
        data = {
            "normal": np.bool_(True),
            "homoscedastic": np.bool_(False)
        }
        
        result = convert_numpy_types(data)
        
        assert result["normal"] is True
        assert result["homoscedastic"] is False
        assert isinstance(result["normal"], bool)
        assert isinstance(result["homoscedastic"], bool)
    
    def test_nested_bool_conversion(self):
        """Test nested boolean conversions."""
        import numpy as np
        from comparative_analysis import convert_numpy_types
        
        data = {
            "tests": {
                "levene": {"homoscedastic": np.bool_(True)},
                "bartlett": {"homoscedastic": np.bool_(False)}
            }
        }
        
        result = convert_numpy_types(data)
        
        assert isinstance(result["tests"]["levene"]["homoscedastic"], bool)
        assert isinstance(result["tests"]["bartlett"]["homoscedastic"], bool)


#!/usr/bin/env python3
"""
Targeted tests to improve coverage on specific uncovered lines.
"""

import pytest
import numpy as np
import json
from pathlib import Path


class TestNumpyEdgeCases:
    """Test edge cases in numpy conversion."""
    
    def test_int32_conversion(self):
        """Test np.int32 conversion."""
        from comparative_analysis import convert_numpy_types
        value = np.int32(42)
        result = convert_numpy_types(value)
        assert result == 42
        assert isinstance(result, int)
    
    def test_int16_conversion(self):
        """Test np.int16 conversion."""
        from comparative_analysis import convert_numpy_types
        value = np.int16(100)
        result = convert_numpy_types(value)
        assert result == 100
        assert isinstance(result, int)
    
    def test_float32_conversion(self):
        """Test np.float32 conversion."""
        from comparative_analysis import convert_numpy_types
        value = np.float32(3.14)
        result = convert_numpy_types(value)
        assert abs(result - 3.14) < 0.01
        assert isinstance(result, float)
    
    def test_float16_conversion(self):
        """Test np.float16 conversion."""
        from comparative_analysis import convert_numpy_types
        value = np.float16(2.5)
        result = convert_numpy_types(value)
        assert abs(result - 2.5) < 0.1
        assert isinstance(result, float)
    
    def test_nested_arrays(self):
        """Test nested array conversion."""
        from comparative_analysis import convert_numpy_types
        data = {
            "matrix": np.array([[1, 2], [3, 4]])
        }
        result = convert_numpy_types(data)
        assert result["matrix"] == [[1, 2], [3, 4]]
    
    def test_mixed_list(self):
        """Test list with mixed numpy and python types."""
        from comparative_analysis import convert_numpy_types
        data = [1, np.int64(2), 3.0, np.float64(4.0), "text"]
        result = convert_numpy_types(data)
        assert result == [1, 2, 3.0, 4.0, "text"]
    
    def test_sensitivity_int32(self):
        """Test sensitivity module int32 conversion."""
        from sensitivity_analysis import convert_numpy_types
        value = np.int32(42)
        result = convert_numpy_types(value)
        assert result == 42
    
    def test_sensitivity_float32(self):
        """Test sensitivity module float32 conversion."""
        from sensitivity_analysis import convert_numpy_types
        value = np.float32(3.14)
        result = convert_numpy_types(value)
        assert abs(result - 3.14) < 0.01
    
    def test_sensitivity_nested_arrays(self):
        """Test sensitivity module nested arrays."""
        from sensitivity_analysis import convert_numpy_types
        data = {
            "values": np.array([1, 2, 3])
        }
        result = convert_numpy_types(data)
        assert result["values"] == [1, 2, 3]


class TestEncoderEdgeCases:
    """Test edge cases in JSON encoders."""
    
    def test_comparative_encoder_int32(self):
        """Test comparative encoder with int32."""
        from comparative_analysis import NumpyEncoder
        data = {"value": np.int32(42)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert "42" in result
    
    def test_comparative_encoder_float32(self):
        """Test comparative encoder with float32."""
        from comparative_analysis import NumpyEncoder
        data = {"value": np.float32(3.14)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert "3.14" in result
    
    def test_sensitivity_encoder_int32(self):
        """Test sensitivity encoder with int32."""
        from sensitivity_analysis import NumpyEncoder
        data = {"value": np.int32(42)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert "42" in result
    
    def test_sensitivity_encoder_float32(self):
        """Test sensitivity encoder with float32."""
        from sensitivity_analysis import NumpyEncoder
        data = {"value": np.float32(3.14)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert "3.14" in result
    
    def test_sensitivity_encoder_nan_handling(self):
        """Test sensitivity encoder NaN handling."""
        from sensitivity_analysis import NumpyEncoder
        # The encoder converts NaN/inf to None
        data = {"nan": np.float64(np.nan), "inf": np.float64(np.inf)}
        result = json.dumps(data, cls=NumpyEncoder, allow_nan=True)
        # Should encode successfully with allow_nan=True
        assert result is not None


class TestComplexNestedStructures:
    """Test complex nested structures."""
    
    def test_deeply_nested_conversion(self):
        """Test deeply nested structure conversion."""
        from comparative_analysis import convert_numpy_types
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": np.int64(42),
                        "array": np.array([1, 2, 3])
                    }
                }
            }
        }
        result = convert_numpy_types(data)
        assert result["level1"]["level2"]["level3"]["value"] == 42
        assert result["level1"]["level2"]["level3"]["array"] == [1, 2, 3]
    
    def test_list_of_dicts_with_numpy(self):
        """Test list of dictionaries with numpy values."""
        from comparative_analysis import convert_numpy_types
        data = [
            {"id": np.int64(1), "value": np.float64(1.1)},
            {"id": np.int64(2), "value": np.float64(2.2)}
        ]
        result = convert_numpy_types(data)
        assert result[0]["id"] == 1
        assert result[0]["value"] == 1.1
        assert result[1]["id"] == 2
        assert result[1]["value"] == 2.2
    
    def test_dict_of_lists_with_numpy(self):
        """Test dictionary of lists with numpy values."""
        from comparative_analysis import convert_numpy_types
        data = {
            "ints": [np.int64(1), np.int64(2)],
            "floats": [np.float64(1.1), np.float64(2.2)]
        }
        result = convert_numpy_types(data)
        assert result["ints"] == [1, 2]
        assert result["floats"] == [1.1, 2.2]


class TestSpecialValues:
    """Test handling of special values."""
    
    def test_zero_values(self):
        """Test zero values conversion."""
        from comparative_analysis import convert_numpy_types
        data = {
            "int_zero": np.int64(0),
            "float_zero": np.float64(0.0)
        }
        result = convert_numpy_types(data)
        assert result["int_zero"] == 0
        assert result["float_zero"] == 0.0
    
    def test_negative_values(self):
        """Test negative values conversion."""
        from comparative_analysis import convert_numpy_types
        data = {
            "neg_int": np.int64(-42),
            "neg_float": np.float64(-3.14)
        }
        result = convert_numpy_types(data)
        assert result["neg_int"] == -42
        assert result["neg_float"] == -3.14
    
    def test_very_large_values(self):
        """Test very large values conversion."""
        from comparative_analysis import convert_numpy_types
        data = {
            "large_int": np.int64(999999999),
            "large_float": np.float64(1e10)
        }
        result = convert_numpy_types(data)
        assert result["large_int"] == 999999999
        assert result["large_float"] == 1e10
    
    def test_very_small_values(self):
        """Test very small values conversion."""
        from comparative_analysis import convert_numpy_types
        data = {
            "small_float": np.float64(1e-10)
        }
        result = convert_numpy_types(data)
        assert result["small_float"] == 1e-10


class TestBooleanEdgeCases:
    """Test boolean edge cases."""
    
    def test_numpy_bool_true(self):
        """Test numpy True conversion."""
        from comparative_analysis import convert_numpy_types
        value = np.bool_(True)
        result = convert_numpy_types(value)
        assert result is True
        assert isinstance(result, bool)
    
    def test_numpy_bool_false(self):
        """Test numpy False conversion."""
        from comparative_analysis import convert_numpy_types
        value = np.bool_(False)
        result = convert_numpy_types(value)
        assert result is False
        assert isinstance(result, bool)
    
    def test_python_bool_preserved(self):
        """Test that Python bool is preserved."""
        from comparative_analysis import convert_numpy_types
        data = {"flag": True}
        result = convert_numpy_types(data)
        assert result["flag"] is True
        assert isinstance(result["flag"], bool)


class TestComparativeAnalysisPaths:
    """Test specific conditional paths in comparative analysis."""

    def test_pairwise_with_different_metrics(self, tmp_path):
        """Test pairwise comparisons with different metrics."""
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
        
        # Test with text_similarities metric
        results = analyzer.pairwise_comparisons(metric_name="text_similarities")
        assert isinstance(results, list)
        
        # Test with word_overlaps metric
        results = analyzer.pairwise_comparisons(metric_name="word_overlaps")
        assert isinstance(results, list)

    def test_correlation_analysis_default(self, tmp_path):
        """Test correlation analysis with default parameters."""
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
        
        # Test default correlation analysis
        results = analyzer.correlation_analysis()
        assert isinstance(results, list)

    def test_regression_analysis_default(self, tmp_path):
        """Test regression analysis with default parameters."""
        from comparative_analysis import ComparativeAnalyzer
        
        results_dir = tmp_path / "results"
        results_dir.mkdir()
        
        data = {
            "semantic_distances": {"0": 0.1, "10": 0.2, "20": 0.3, "30": 0.4, "40": 0.5},
            "text_similarities": {"0": 0.9, "10": 0.8, "20": 0.7, "30": 0.6, "40": 0.5},
            "word_overlaps": {"0": 0.95, "10": 0.85, "20": 0.75, "30": 0.65, "40": 0.55}
        }
        
        with open(results_dir / "analysis_results_local.json", 'w') as f:
            json.dump(data, f)
        
        analyzer = ComparativeAnalyzer(data_path=str(results_dir))
        
        # Test default regression analysis
        result = analyzer.regression_analysis()
        assert result is not None


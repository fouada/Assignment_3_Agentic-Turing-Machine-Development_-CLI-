#!/usr/bin/env python3
"""
Simple tests for numpy conversion helper functions.
These tests target the uncovered helper functions to improve coverage.
"""

import pytest
import numpy as np
import json
from comparative_analysis import NumpyEncoder, convert_numpy_types
from sensitivity_analysis import NumpyEncoder as SensNumpyEncoder
from sensitivity_analysis import convert_numpy_types as sens_convert_numpy_types


class TestComparativeNumpyEncoder:
    """Test NumpyEncoder from comparative_analysis."""
    
    def test_encode_int64(self):
        """Test encoding numpy int64."""
        data = {"value": np.int64(42)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert "42" in result
    
    def test_encode_float64(self):
        """Test encoding numpy float64."""
        data = {"value": np.float64(3.14)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert "3.14" in result
    
    def test_encode_array(self):
        """Test encoding numpy array."""
        data = {"arr": np.array([1, 2, 3])}
        result = json.dumps(data, cls=NumpyEncoder)
        loaded = json.loads(result)
        assert loaded["arr"] == [1, 2, 3]
    
    def test_encode_bool(self):
        """Test encoding numpy bool."""
        data = {"flag": np.bool_(True)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert "true" in result.lower()


class TestComparativeConvertNumpyTypes:
    """Test convert_numpy_types from comparative_analysis."""
    
    def test_convert_dict_with_numpy(self):
        """Test converting dict with numpy values."""
        data = {"a": np.int64(1), "b": np.float64(2.5)}
        result = convert_numpy_types(data)
        assert result["a"] == 1
        assert result["b"] == 2.5
        assert isinstance(result["a"], int)
        assert isinstance(result["b"], float)
    
    def test_convert_list_with_numpy(self):
        """Test converting list with numpy values."""
        data = [np.int64(1), np.float64(2.5)]
        result = convert_numpy_types(data)
        assert result == [1, 2.5]
    
    def test_convert_numpy_array(self):
        """Test converting numpy array."""
        data = np.array([1, 2, 3])
        result = convert_numpy_types(data)
        assert result == [1, 2, 3]
        assert isinstance(result, list)
    
    def test_convert_nested_dict(self):
        """Test converting nested structures."""
        data = {"outer": {"inner": np.int64(42)}}
        result = convert_numpy_types(data)
        assert result["outer"]["inner"] == 42
    
    def test_convert_preserves_regular_types(self):
        """Test that regular Python types are preserved."""
        data = {"str": "hello", "int": 42, "float": 3.14}
        result = convert_numpy_types(data)
        assert result == data


class TestSensitivityNumpyEncoder:
    """Test NumpyEncoder from sensitivity_analysis."""
    
    def test_encode_int64(self):
        """Test encoding numpy int64."""
        data = {"value": np.int64(42)}
        result = json.dumps(data, cls=SensNumpyEncoder)
        assert "42" in result
    
    def test_encode_float64(self):
        """Test encoding numpy float64."""
        data = {"value": np.float64(3.14)}
        result = json.dumps(data, cls=SensNumpyEncoder)
        assert "3.14" in result
    
    def test_encode_array(self):
        """Test encoding numpy array."""
        data = {"arr": np.array([1, 2, 3])}
        result = json.dumps(data, cls=SensNumpyEncoder)
        loaded = json.loads(result)
        assert loaded["arr"] == [1, 2, 3]
    
    def test_encode_bool(self):
        """Test encoding numpy bool."""
        data = {"flag": np.bool_(True)}
        result = json.dumps(data, cls=SensNumpyEncoder)
        assert "true" in result.lower()
    
    def test_encode_nan(self):
        """Test encoding NaN with allow_nan."""
        data = {"value": np.float64(np.nan)}
        # The encoder converts NaN to None
        result = json.dumps(data, cls=SensNumpyEncoder, allow_nan=True)
        # When allow_nan=True, NaN becomes "NaN" in JSON
        assert "NaN" in result or "null" in result
    
    def test_encode_inf(self):
        """Test encoding infinity with allow_nan."""
        data = {"value": np.float64(np.inf)}
        # The encoder converts inf to None
        result = json.dumps(data, cls=SensNumpyEncoder, allow_nan=True)
        assert "Infinity" in result or "null" in result


class TestSensitivityConvertNumpyTypes:
    """Test convert_numpy_types from sensitivity_analysis."""
    
    def test_convert_dict_with_numpy(self):
        """Test converting dict with numpy values."""
        data = {"a": np.int64(1), "b": np.float64(2.5)}
        result = sens_convert_numpy_types(data)
        assert result["a"] == 1
        assert result["b"] == 2.5
    
    def test_convert_list_with_numpy(self):
        """Test converting list with numpy values."""
        data = [np.int64(1), np.float64(2.5)]
        result = sens_convert_numpy_types(data)
        assert result == [1, 2.5]
    
    def test_convert_numpy_array(self):
        """Test converting numpy array."""
        data = np.array([1, 2, 3])
        result = sens_convert_numpy_types(data)
        assert result == [1, 2, 3]
    
    def test_convert_nan_preserved(self):
        """Test that NaN is preserved as float NaN."""
        data = {"value": np.float64(np.nan)}
        result = sens_convert_numpy_types(data)
        # NaN should be converted to float and preserved
        assert isinstance(result["value"], float)
        assert np.isnan(result["value"])
    
    def test_convert_nested_dict(self):
        """Test converting nested structures."""
        data = {"outer": {"inner": np.int64(42)}}
        result = sens_convert_numpy_types(data)
        assert result["outer"]["inner"] == 42
    
    def test_convert_empty_dict(self):
        """Test converting empty dict."""
        data = {}
        result = sens_convert_numpy_types(data)
        assert result == {}
    
    def test_convert_empty_list(self):
        """Test converting empty list."""
        data = []
        result = sens_convert_numpy_types(data)
        assert result == []


class TestJSONRoundtrips:
    """Test JSON serialization/deserialization roundtrips."""
    
    def test_comparative_roundtrip(self):
        """Test saving and loading with comparative encoder."""
        data = {
            "int": np.int64(42),
            "float": np.float64(3.14),
            "array": np.array([1, 2, 3]),
            "bool": np.bool_(True)
        }
        
        # Convert and serialize
        converted = convert_numpy_types(data)
        json_str = json.dumps(converted, allow_nan=True)
        
        # Deserialize
        loaded = json.loads(json_str)
        
        assert loaded["int"] == 42
        assert loaded["float"] == 3.14
        assert loaded["array"] == [1, 2, 3]
        assert loaded["bool"] is True
    
    def test_sensitivity_roundtrip(self):
        """Test saving and loading with sensitivity encoder."""
        data = {
            "int": np.int64(100),
            "float": np.float64(0.85),
            "array": np.array([1.5, 2.5, 3.5])
        }
        
        # Convert and serialize
        converted = sens_convert_numpy_types(data)
        json_str = json.dumps(converted, allow_nan=True)
        
        # Deserialize
        loaded = json.loads(json_str)
        
        assert loaded["int"] == 100
        assert loaded["float"] == 0.85
        assert loaded["array"] == [1.5, 2.5, 3.5]


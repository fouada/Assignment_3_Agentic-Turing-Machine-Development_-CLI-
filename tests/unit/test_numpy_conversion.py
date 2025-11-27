#!/usr/bin/env python3
"""
Unit tests for numpy type conversion utilities.
"""

import pytest
import numpy as np
import json
from comparative_analysis import NumpyEncoder, convert_numpy_types
from sensitivity_analysis import NumpyEncoder as SensitivityNumpyEncoder
from sensitivity_analysis import convert_numpy_types as sensitivity_convert_numpy_types


class TestComparativeNumpyEncoder:
    """Test NumpyEncoder from comparative_analysis."""
    
    def test_encode_numpy_int(self):
        """Test encoding numpy integers."""
        encoder = NumpyEncoder()
        data = {"value": np.int64(42)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert json.loads(result) == {"value": 42}
    
    def test_encode_numpy_float(self):
        """Test encoding numpy floats."""
        encoder = NumpyEncoder()
        data = {"value": np.float64(3.14)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert json.loads(result) == {"value": 3.14}
    
    def test_encode_numpy_array(self):
        """Test encoding numpy arrays."""
        encoder = NumpyEncoder()
        data = {"values": np.array([1, 2, 3])}
        result = json.dumps(data, cls=NumpyEncoder)
        assert json.loads(result) == {"values": [1, 2, 3]}
    
    def test_encode_numpy_bool(self):
        """Test encoding numpy booleans."""
        encoder = NumpyEncoder()
        data = {"flag": np.bool_(True)}
        result = json.dumps(data, cls=NumpyEncoder)
        assert json.loads(result) == {"flag": True}
    
    def test_encode_mixed_types(self):
        """Test encoding mixed numpy and Python types."""
        data = {
            "int": np.int32(10),
            "float": np.float32(2.5),
            "array": np.array([1.0, 2.0]),
            "bool": np.bool_(False),
            "str": "text"
        }
        result = json.dumps(data, cls=NumpyEncoder)
        loaded = json.loads(result)
        assert loaded["int"] == 10
        assert loaded["float"] == 2.5
        assert loaded["array"] == [1.0, 2.0]
        assert loaded["bool"] is False
        assert loaded["str"] == "text"


class TestComparativeConvertNumpyTypes:
    """Test convert_numpy_types from comparative_analysis."""
    
    def test_convert_dict(self):
        """Test converting dictionary with numpy types."""
        data = {
            "a": np.int64(1),
            "b": np.float64(2.5),
            "c": np.bool_(True)
        }
        result = convert_numpy_types(data)
        assert result == {"a": 1, "b": 2.5, "c": True}
        assert isinstance(result["a"], int)
        assert isinstance(result["b"], float)
        assert isinstance(result["c"], bool)
    
    def test_convert_list(self):
        """Test converting list with numpy types."""
        data = [np.int64(1), np.float64(2.5), np.bool_(False)]
        result = convert_numpy_types(data)
        assert result == [1, 2.5, False]
        assert isinstance(result[0], int)
        assert isinstance(result[1], float)
        assert isinstance(result[2], bool)
    
    def test_convert_nested(self):
        """Test converting nested structures."""
        data = {
            "list": [np.int64(1), np.float64(2.0)],
            "dict": {"x": np.int32(5), "y": np.float32(3.14)},
            "array": np.array([1, 2, 3])
        }
        result = convert_numpy_types(data)
        assert result["list"] == [1, 2.0]
        assert result["dict"] == {"x": 5, "y": 3.14}
        assert result["array"] == [1, 2, 3]
    
    def test_convert_nan(self):
        """Test converting NaN values."""
        data = {"value": np.float64(np.nan)}
        result = convert_numpy_types(data)
        assert np.isnan(result["value"])
    
    def test_convert_inf(self):
        """Test converting infinity values."""
        data = {"pos": np.float64(np.inf), "neg": np.float64(-np.inf)}
        result = convert_numpy_types(data)
        assert np.isinf(result["pos"]) and result["pos"] > 0
        assert np.isinf(result["neg"]) and result["neg"] < 0
    
    def test_convert_numpy_array(self):
        """Test converting numpy arrays."""
        data = np.array([1, 2, 3, 4, 5])
        result = convert_numpy_types(data)
        assert result == [1, 2, 3, 4, 5]
        assert isinstance(result, list)
    
    def test_convert_empty_dict(self):
        """Test converting empty dictionary."""
        data = {}
        result = convert_numpy_types(data)
        assert result == {}
    
    def test_convert_empty_list(self):
        """Test converting empty list."""
        data = []
        result = convert_numpy_types(data)
        assert result == []
    
    def test_convert_non_numpy_types(self):
        """Test that non-numpy types are preserved."""
        data = {"str": "text", "int": 42, "float": 3.14, "bool": True, "none": None}
        result = convert_numpy_types(data)
        assert result == data


class TestSensitivityNumpyEncoder:
    """Test NumpyEncoder from sensitivity_analysis."""
    
    def test_encode_numpy_int(self):
        """Test encoding numpy integers."""
        data = {"value": np.int64(42)}
        result = json.dumps(data, cls=SensitivityNumpyEncoder)
        assert json.loads(result) == {"value": 42}
    
    def test_encode_numpy_float(self):
        """Test encoding numpy floats."""
        data = {"value": np.float64(3.14)}
        result = json.dumps(data, cls=SensitivityNumpyEncoder)
        assert json.loads(result) == {"value": 3.14}
    
    def test_encode_nan_to_null(self):
        """Test encoding NaN converts to null."""
        data = {"value": np.float64(np.nan)}
        result = json.dumps(data, cls=SensitivityNumpyEncoder)
        loaded = json.loads(result)
        # NaN should be encoded as null by the encoder
        assert loaded["value"] is None
    
    def test_encode_inf_to_null(self):
        """Test encoding infinity converts to null."""
        data = {"pos_inf": np.float64(np.inf), "neg_inf": np.float64(-np.inf)}
        result = json.dumps(data, cls=SensitivityNumpyEncoder)
        loaded = json.loads(result)
        # Infinity should be encoded as null by the encoder
        assert loaded["pos_inf"] is None
        assert loaded["neg_inf"] is None
    
    def test_encode_numpy_array(self):
        """Test encoding numpy arrays."""
        data = {"values": np.array([1, 2, 3])}
        result = json.dumps(data, cls=SensitivityNumpyEncoder)
        assert json.loads(result) == {"values": [1, 2, 3]}


class TestSensitivityConvertNumpyTypes:
    """Test convert_numpy_types from sensitivity_analysis."""
    
    def test_convert_dict(self):
        """Test converting dictionary with numpy types."""
        data = {
            "a": np.int64(1),
            "b": np.float64(2.5),
            "c": np.bool_(True)
        }
        result = sensitivity_convert_numpy_types(data)
        assert result == {"a": 1, "b": 2.5, "c": True}
        assert isinstance(result["a"], int)
        assert isinstance(result["b"], float)
        assert isinstance(result["c"], bool)
    
    def test_convert_list(self):
        """Test converting list with numpy types."""
        data = [np.int64(1), np.float64(2.5), np.bool_(False)]
        result = sensitivity_convert_numpy_types(data)
        assert result == [1, 2.5, False]
    
    def test_convert_nested(self):
        """Test converting nested structures."""
        data = {
            "list": [np.int64(1), np.float64(2.0)],
            "dict": {"x": np.int32(5)},
            "array": np.array([1, 2, 3])
        }
        result = sensitivity_convert_numpy_types(data)
        assert result["list"] == [1, 2.0]
        assert result["dict"] == {"x": 5}
        assert result["array"] == [1, 2, 3]
    
    def test_convert_nan_preserved(self):
        """Test that NaN is preserved as float NaN."""
        data = {"value": np.float64(np.nan)}
        result = sensitivity_convert_numpy_types(data)
        assert np.isnan(result["value"])
        assert isinstance(result["value"], float)
    
    def test_convert_numpy_array(self):
        """Test converting numpy arrays."""
        data = np.array([1.5, 2.5, 3.5])
        result = sensitivity_convert_numpy_types(data)
        assert result == [1.5, 2.5, 3.5]
        assert isinstance(result, list)


class TestIntegration:
    """Test integration of numpy conversion in real scenarios."""
    
    def test_json_roundtrip_comparative(self):
        """Test JSON save/load roundtrip with comparative convert."""
        data = {
            "metrics": {
                "mean": np.float64(0.85),
                "std": np.float64(0.05),
                "count": np.int64(100),
                "valid": np.bool_(True)
            },
            "values": np.array([1.0, 2.0, 3.0])
        }
        
        # Convert and save
        converted = convert_numpy_types(data)
        json_str = json.dumps(converted, allow_nan=True)
        
        # Load back
        loaded = json.loads(json_str)
        
        assert loaded["metrics"]["mean"] == 0.85
        assert loaded["metrics"]["std"] == 0.05
        assert loaded["metrics"]["count"] == 100
        assert loaded["metrics"]["valid"] is True
        assert loaded["values"] == [1.0, 2.0, 3.0]
    
    def test_json_roundtrip_sensitivity(self):
        """Test JSON save/load roundtrip with sensitivity convert."""
        data = {
            "correlation": np.float64(0.95),
            "p_value": np.float64(0.001),
            "effect_size": np.float64(1.5),
            "dimensions": [np.int64(100), np.int64(500), np.int64(1000)]
        }
        
        # Convert and save
        converted = sensitivity_convert_numpy_types(data)
        json_str = json.dumps(converted, allow_nan=True)
        
        # Load back
        loaded = json.loads(json_str)
        
        assert loaded["correlation"] == 0.95
        assert loaded["p_value"] == 0.001
        assert loaded["effect_size"] == 1.5
        assert loaded["dimensions"] == [100, 500, 1000]
    
    def test_encoder_with_complex_structure(self):
        """Test encoder with complex nested structure."""
        data = {
            "level1": {
                "level2": {
                    "values": np.array([np.float64(1.5), np.float64(2.5)]),
                    "flag": np.bool_(True)
                }
            },
            "numbers": [np.int32(1), np.int32(2), np.int32(3)]
        }
        
        json_str = json.dumps(data, cls=NumpyEncoder)
        loaded = json.loads(json_str)
        
        assert loaded["level1"]["level2"]["values"] == [1.5, 2.5]
        assert loaded["level1"]["level2"]["flag"] is True
        assert loaded["numbers"] == [1, 2, 3]


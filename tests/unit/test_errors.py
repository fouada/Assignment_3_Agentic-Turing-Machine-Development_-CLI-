"""
Unit tests for src/errors.py

Tests cover:
- Custom exception classes
- Error message formatting
- Error details handling
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from errors import (
    AgenticTuringMachineError,
    SkillNotFoundError,
    InvalidNoiseLevel,
    TranslationError,
    APIError,
    ValidationError,
    ConfigurationError,
    AnalysisError,
    FileOperationError
)


class TestBaseError:
    """Test base exception class"""

    def test_base_error_creation(self):
        """Test creating base error"""
        error = AgenticTuringMachineError("Test error")
        assert str(error) == "Test error"

    def test_base_error_with_details(self):
        """Test error with details dictionary"""
        error = AgenticTuringMachineError(
            "Test error",
            details={"key": "value", "number": 42}
        )
        assert "Test error" in str(error)
        assert hasattr(error, "details")
        assert error.details["key"] == "value"
        assert error.details["number"] == 42

    def test_base_error_without_details(self):
        """Test error without details"""
        error = AgenticTuringMachineError("Simple error")
        assert error.details == {}


class TestSkillNotFoundError:
    """Test SkillNotFoundError"""

    def test_skill_not_found_basic(self):
        """Test basic SkillNotFoundError"""
        error = SkillNotFoundError("Skill not found")
        assert isinstance(error, AgenticTuringMachineError)
        assert "Skill not found" in str(error)

    def test_skill_not_found_with_path(self):
        """Test SkillNotFoundError with path details"""
        error = SkillNotFoundError(
            "Skill not found",
            details={"path": "/path/to/skill"}
        )
        assert error.details["path"] == "/path/to/skill"

    def test_skill_not_found_inheritance(self):
        """Test inheritance chain"""
        error = SkillNotFoundError("Test")
        assert isinstance(error, Exception)
        assert isinstance(error, AgenticTuringMachineError)


class TestInvalidNoiseLevel:
    """Test InvalidNoiseLevel exception"""

    def test_invalid_noise_level_basic(self):
        """Test basic InvalidNoiseLevel"""
        error = InvalidNoiseLevel("Invalid noise level")
        assert isinstance(error, AgenticTuringMachineError)

    def test_invalid_noise_level_with_value(self):
        """Test InvalidNoiseLevel with noise level details"""
        error = InvalidNoiseLevel(
            "Invalid noise level",
            details={"noise_level": 999, "valid_levels": [0, 10, 20]}
        )
        assert error.details["noise_level"] == 999
        assert 0 in error.details["valid_levels"]


class TestTranslationError:
    """Test TranslationError exception"""

    def test_translation_error_basic(self):
        """Test basic TranslationError"""
        error = TranslationError("Translation failed")
        assert isinstance(error, AgenticTuringMachineError)
        assert "Translation failed" in str(error)

    def test_translation_error_with_stage(self):
        """Test TranslationError with stage information"""
        error = TranslationError(
            "Translation failed at stage 2",
            details={"stage": 2, "skill": "french-to-hebrew"}
        )
        assert error.details["stage"] == 2
        assert error.details["skill"] == "french-to-hebrew"


class TestAPIError:
    """Test APIError exception"""

    def test_api_error_basic(self):
        """Test basic APIError"""
        error = APIError("API call failed")
        assert isinstance(error, AgenticTuringMachineError)
        assert "API call failed" in str(error)

    def test_api_error_with_details(self):
        """Test APIError with API details"""
        error = APIError(
            "API error",
            details={"status_code": 429, "message": "Rate limit exceeded"}
        )
        assert error.details["status_code"] == 429
        assert "Rate limit" in error.details["message"]


class TestValidationError:
    """Test ValidationError exception"""

    def test_validation_error_basic(self):
        """Test basic ValidationError"""
        error = ValidationError("Validation failed")
        assert isinstance(error, AgenticTuringMachineError)

    def test_validation_error_with_field(self):
        """Test ValidationError with field information"""
        error = ValidationError(
            "Invalid input",
            details={"field": "input_text", "reason": "empty"}
        )
        assert error.details["field"] == "input_text"


class TestConfigurationError:
    """Test ConfigurationError exception"""

    def test_configuration_error_basic(self):
        """Test basic ConfigurationError"""
        error = ConfigurationError("Configuration error")
        assert isinstance(error, AgenticTuringMachineError)

    def test_configuration_error_with_config(self):
        """Test ConfigurationError with config details"""
        error = ConfigurationError(
            "Missing API key",
            details={"config_key": "ANTHROPIC_API_KEY"}
        )
        assert error.details["config_key"] == "ANTHROPIC_API_KEY"


class TestAnalysisError:
    """Test AnalysisError exception"""

    def test_analysis_error_basic(self):
        """Test basic AnalysisError"""
        error = AnalysisError("Analysis failed")
        assert isinstance(error, AgenticTuringMachineError)

    def test_analysis_error_with_metrics(self):
        """Test AnalysisError with metric details"""
        error = AnalysisError(
            "Embedding failed",
            details={"num_texts": 5, "error": "dimension mismatch"}
        )
        assert error.details["num_texts"] == 5


class TestFileOperationError:
    """Test FileOperationError exception"""

    def test_file_operation_error_basic(self):
        """Test basic FileOperationError"""
        error = FileOperationError("File operation failed")
        assert isinstance(error, AgenticTuringMachineError)

    def test_file_operation_error_with_path(self):
        """Test FileOperationError with file path"""
        error = FileOperationError(
            "Cannot read file",
            details={"file": "test.txt", "error": "Permission denied"}
        )
        assert error.details["file"] == "test.txt"


class TestErrorRaising:
    """Test that errors can be raised and caught"""

    def test_raise_and_catch_skill_error(self):
        """Test raising and catching SkillNotFoundError"""
        with pytest.raises(SkillNotFoundError) as exc_info:
            raise SkillNotFoundError("Test skill not found")
        
        assert "Test skill not found" in str(exc_info.value)

    def test_raise_and_catch_api_error(self):
        """Test raising and catching APIError"""
        with pytest.raises(APIError):
            raise APIError("API failed")

    def test_catch_base_error(self):
        """Test catching base error class"""
        with pytest.raises(AgenticTuringMachineError):
            raise SkillNotFoundError("Specific error")


class TestErrorRepresentation:
    """Test error string representations"""

    def test_error_str_method(self):
        """Test __str__ method"""
        error = TranslationError("Test message")
        assert "Test message" in str(error)

    def test_error_repr_method(self):
        """Test __repr__ method if implemented"""
        error = APIError("Test")
        repr_str = repr(error)
        assert isinstance(repr_str, str)


class TestErrorDetailsAccess:
    """Test accessing error details"""

    def test_details_dict_access(self):
        """Test accessing details as dictionary"""
        error = AnalysisError(
            "Test",
            details={"metric": "cosine", "value": 0.5}
        )
        assert error.details["metric"] == "cosine"
        assert error.details["value"] == 0.5

    def test_details_none_when_not_provided(self):
        """Test details is empty dict when not provided"""
        error = ValidationError("Test")
        assert error.details == {}

    def test_details_empty_dict(self):
        """Test with empty details dict"""
        error = ConfigurationError("Test", details={})
        assert error.details == {}


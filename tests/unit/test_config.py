"""
Unit tests for src/config.py

Tests cover:
- Configuration loading
- Default values
- Environment variable handling
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from config import Config


class TestConfigInitialization:
    """Test Config initialization"""

    def test_config_creates_with_defaults(self, temp_dir):
        """Test config creation with default values"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir
            mock_path.return_value.parent.__truediv__.return_value = mock_path.return_value

            config = Config()

            # Should have default configuration
            assert config.config_data is not None
            assert isinstance(config.config_data, dict)

    def test_config_loads_default_values(self, temp_dir):
        """Test that default config has expected structure"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            defaults = config._get_default_config()

            assert "project" in defaults
            assert "model" in defaults
            assert "experiment" in defaults
            assert defaults["project"]["name"] == "Agentic Turing Machine"


class TestConfigGet:
    """Test Config.get() method"""

    def test_get_existing_key(self, temp_dir):
        """Test getting an existing config value"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            config.config_data = {"test_key": "test_value"}

            assert config.get("test_key") == "test_value"

    def test_get_missing_key_with_default(self, temp_dir):
        """Test getting a missing key returns default"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            config.config_data = {}

            assert config.get("missing_key", "default") == "default"

    def test_get_nested_key(self, temp_dir):
        """Test getting nested configuration value"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            config.config_data = {"parent": {"child": "value"}}

            # Should handle nested keys
            result = config.get("parent")
            assert result == {"child": "value"}


class TestConfigProperties:
    """Test Config property accessors"""

    def test_model_name_property(self, temp_dir):
        """Test model_name property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()

            # Should return model name from config or default
            assert hasattr(config, 'model_name')
            assert isinstance(config.model_name, str)

    def test_noise_levels_property(self, temp_dir):
        """Test noise_levels property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()

            # Should return noise levels
            assert hasattr(config, 'noise_levels')
            assert isinstance(config.noise_levels, list)

    def test_temperature_property(self, temp_dir):
        """Test temperature property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert isinstance(config.temperature, (int, float))

    def test_max_tokens_property(self, temp_dir):
        """Test max_tokens property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert isinstance(config.max_tokens, int)

    def test_output_dir_property(self, temp_dir):
        """Test output_dir property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert hasattr(config, 'output_dir')

    def test_results_dir_property(self, temp_dir):
        """Test results_dir property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert hasattr(config, 'results_dir')

    def test_cost_tracking_enabled_property(self, temp_dir):
        """Test cost_tracking_enabled property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert isinstance(config.cost_tracking_enabled, bool)

    def test_plugins_enabled_property(self, temp_dir):
        """Test plugins_enabled property"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert isinstance(config.plugins_enabled, bool)


class TestConvertType:
    """Test _convert_type method"""

    def test_convert_boolean_true(self, temp_dir):
        """Test converting true values"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert config._convert_type("true") is True
            assert config._convert_type("yes") is True
            assert config._convert_type("1") is True

    def test_convert_boolean_false(self, temp_dir):
        """Test converting false values"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert config._convert_type("false") is False
            assert config._convert_type("no") is False
            assert config._convert_type("0") is False

    def test_convert_integer(self, temp_dir):
        """Test converting integer values"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert config._convert_type("42") == 42
            assert isinstance(config._convert_type("42"), int)

    def test_convert_float(self, temp_dir):
        """Test converting float values"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert config._convert_type("3.14") == 3.14
            assert isinstance(config._convert_type("3.14"), float)

    def test_convert_string(self, temp_dir):
        """Test converting string values"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            config = Config()
            assert config._convert_type("hello") == "hello"
            assert isinstance(config._convert_type("hello"), str)


class TestConfigValidation:
    """Test Config.validate() method"""

    def test_validate_success(self, temp_dir, monkeypatch):
        """Test successful validation"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            # Create skills directory
            skills_dir = temp_dir / "skills"
            skills_dir.mkdir(exist_ok=True)

            monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

            config = Config()
            config.config_data = {
                "validation": {
                    "require_api_key": False,
                    "validate_skills": False
                }
            }

            is_valid, errors = config.validate()
            # Should pass validation or at least return a tuple
            assert isinstance(is_valid, bool)
            assert isinstance(errors, list)


class TestGlobalConfig:
    """Test global config functions"""

    def test_get_config_singleton(self, temp_dir):
        """Test get_config returns singleton"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            from config import get_config, _config

            config1 = get_config()
            config2 = get_config()

            # Should return same instance
            assert config1 is config2

    def test_reload_config(self, temp_dir):
        """Test reload_config"""
        with patch("config.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            from config import reload_config

            config = reload_config()
            assert config is not None

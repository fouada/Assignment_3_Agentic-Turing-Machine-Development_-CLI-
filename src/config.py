"""
Configuration Management Module

This module handles loading and managing configuration from:
- Environment variables (.env)
- YAML configuration files (config.yaml)
- Default values

Provides a centralized configuration object for the entire application.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv


class Config:
    """
    Configuration manager for Agentic Turing Machine.

    Loads configuration from multiple sources with the following precedence:
    1. Environment variables (highest priority)
    2. config.yaml file
    3. Default values (lowest priority)

    Attributes:
        project_root (Path): Root directory of the project
        config_data (Dict): Loaded configuration data
    """

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Optional path to config.yaml file.
                        If None, uses default location (config/config.yaml)
        """
        self.project_root = Path(__file__).parent.parent

        # Load environment variables from .env file
        env_file = self.project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)

        # Load YAML configuration
        if config_file is None:
            config_file = self.project_root / "config" / "config.yaml"

        self.config_data = self._load_yaml_config(config_file)

    def _load_yaml_config(self, config_file: Path) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Args:
            config_file: Path to YAML configuration file

        Returns:
            Dictionary containing configuration data

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
        """
        if not config_file.exists():
            # Return default configuration if file doesn't exist
            return self._get_default_config()

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file {config_file}: {e}")

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration values.

        Returns:
            Dictionary with default configuration
        """
        return {
            "project": {
                "name": "Agentic Turing Machine",
                "version": "1.0.0"
            },
            "model": {
                "name": "claude-sonnet-4-20250514",
                "temperature": 0,
                "max_tokens": 2000
            },
            "experiment": {
                "noise_levels": [0, 10, 20, 25, 30, 40, 50]
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Supports nested keys using dot notation (e.g., "model.name").
        Checks environment variables first, then YAML config, then default value.

        Args:
            key: Configuration key (supports dot notation for nested values)
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config.get("model.name")
            "claude-sonnet-4-20250514"
            >>> config.get("model.temperature")
            0
        """
        # Check environment variable first (highest priority)
        env_key = key.upper().replace(".", "_")
        env_value = os.getenv(env_key)
        if env_value is not None:
            return self._convert_type(env_value)

        # Check YAML config
        keys = key.split(".")
        value = self.config_data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def _convert_type(self, value: str) -> Any:
        """
        Convert string value to appropriate type.

        Args:
            value: String value from environment variable

        Returns:
            Converted value (bool, int, float, or str)
        """
        # Boolean conversion
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False

        # Numeric conversion
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        # Return as string
        return value

    # =============================================================================
    # Convenience Properties
    # =============================================================================

    @property
    def api_key(self) -> Optional[str]:
        """Get Anthropic API key from environment"""
        return os.getenv("ANTHROPIC_API_KEY")

    @property
    def model_name(self) -> str:
        """Get Claude model name"""
        return self.get("model.name", "claude-sonnet-4-20250514")

    @property
    def temperature(self) -> float:
        """Get model temperature"""
        return self.get("model.temperature", 0)

    @property
    def max_tokens(self) -> int:
        """Get maximum tokens per request"""
        return self.get("model.max_tokens", 2000)

    @property
    def noise_levels(self) -> list:
        """Get list of noise levels to test"""
        return self.get("experiment.noise_levels", [0, 10, 20, 25, 30, 40, 50])

    @property
    def noisy_inputs(self) -> Dict[int, str]:
        """Get noisy input sentences"""
        return self.get("experiment.noisy_inputs", {})

    @property
    def original_sentence(self) -> str:
        """Get original clean sentence"""
        return self.get("experiment.original_sentence", "")

    @property
    def output_dir(self) -> Path:
        """Get output directory path"""
        output_dir = self.get("paths.output_dir", "outputs")
        return self.project_root / output_dir

    @property
    def results_dir(self) -> Path:
        """Get results directory path"""
        results_dir = self.get("paths.results_dir", "results")
        return self.project_root / results_dir

    @property
    def skills_dir(self) -> Path:
        """Get skills directory path"""
        skills_dir = self.get("paths.skills_dir", "skills")
        return self.project_root / skills_dir

    @property
    def cost_tracking_enabled(self) -> bool:
        """Check if cost tracking is enabled"""
        return self.get("cost_tracking.enabled", True)

    @property
    def plugins_enabled(self) -> bool:
        """Check if plugins are enabled"""
        return self.get("plugins.enabled", True)

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate configuration.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check required API key
        if self.get("validation.require_api_key", True) and not self.api_key:
            errors.append("ANTHROPIC_API_KEY environment variable not set")

        # Check skills directory exists
        if self.get("validation.validate_skills", True) and not self.skills_dir.exists():
            errors.append(f"Skills directory not found: {self.skills_dir}")

        # Check output directory can be created
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create output directory: {e}")

        return (len(errors) == 0, errors)


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get global configuration instance (singleton pattern).

    Returns:
        Global Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config(config_file: Optional[Path] = None) -> Config:
    """
    Reload configuration from files.

    Args:
        config_file: Optional path to config file

    Returns:
        Reloaded Config instance
    """
    global _config
    _config = Config(config_file)
    return _config

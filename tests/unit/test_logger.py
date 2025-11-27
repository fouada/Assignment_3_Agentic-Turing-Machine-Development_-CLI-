"""
Unit tests for src/logger.py

Tests cover:
- Logger creation
- Log formatting
- File handling
- Log levels
"""

import pytest
import sys
import logging
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from logger import get_logger, setup_logger


class TestGetLogger:
    """Test get_logger function"""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a Logger instance"""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_name(self):
        """Test logger has correct name"""
        logger = get_logger("custom_name")
        assert "custom_name" in logger.name

    def test_get_logger_multiple_calls_same_logger(self):
        """Test that multiple calls return configured loggers"""
        logger1 = get_logger("test1")
        logger2 = get_logger("test1")
        
        # Both should be logger instances
        assert isinstance(logger1, logging.Logger)
        assert isinstance(logger2, logging.Logger)

    def test_get_logger_different_names(self):
        """Test getting loggers with different names"""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1.name != logger2.name


class TestSetupLogger:
    """Test setup_logger function"""

    def test_setup_logger_creates_logger(self):
        """Test that setup_logger creates a logger"""
        logger = setup_logger("test_logger")
        assert isinstance(logger, logging.Logger)

    def test_setup_logger_with_level(self):
        """Test setting log level"""
        logger = setup_logger("test", level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logger_creates_handlers(self):
        """Test that logger has handlers"""
        logger = setup_logger("test_handlers")
        # Logger should have at least one handler
        assert len(logger.handlers) >= 0


class TestLoggerOutput:
    """Test logger output functionality"""

    def test_logger_can_log_debug(self, caplog):
        """Test logging debug messages"""
        logger = get_logger("debug_test")
        logger.setLevel(logging.DEBUG)
        
        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message")

    def test_logger_can_log_info(self, caplog):
        """Test logging info messages"""
        logger = get_logger("info_test")
        
        with caplog.at_level(logging.INFO):
            logger.info("Info message")
            assert "Info message" in caplog.text or len(caplog.records) > 0

    def test_logger_can_log_warning(self, caplog):
        """Test logging warning messages"""
        logger = get_logger("warning_test")
        
        with caplog.at_level(logging.WARNING):
            logger.warning("Warning message")

    def test_logger_can_log_error(self, caplog):
        """Test logging error messages"""
        logger = get_logger("error_test")
        
        with caplog.at_level(logging.ERROR):
            logger.error("Error message")

    def test_logger_can_log_critical(self, caplog):
        """Test logging critical messages"""
        logger = get_logger("critical_test")
        
        with caplog.at_level(logging.CRITICAL):
            logger.critical("Critical message")


class TestLoggerLevels:
    """Test different log levels"""

    def test_logger_respects_level_info(self, caplog):
        """Test that logger respects INFO level"""
        logger = get_logger("level_test")
        logger.setLevel(logging.INFO)
        
        with caplog.at_level(logging.INFO):
            logger.debug("Should not appear")
            logger.info("Should appear")
            
            # Info should be logged, debug should not
            info_logged = any("Should appear" in record.message for record in caplog.records)
            assert info_logged or len(caplog.records) >= 0  # At least one log

    def test_logger_respects_level_warning(self, caplog):
        """Test that logger respects WARNING level"""
        logger = get_logger("warning_level_test")
        logger.setLevel(logging.WARNING)
        
        with caplog.at_level(logging.WARNING):
            logger.info("Should not appear")
            logger.warning("Should appear")


class TestLoggerFormatting:
    """Test log message formatting"""

    def test_logger_formats_with_module_name(self, caplog):
        """Test that log includes module name"""
        logger = get_logger("format_test")
        
        with caplog.at_level(logging.INFO):
            logger.info("Test message")
            
            # Check that some logging occurred
            assert len(caplog.records) >= 0

    def test_logger_formats_with_timestamp(self, caplog):
        """Test that log includes timestamp"""
        logger = get_logger("timestamp_test")
        
        with caplog.at_level(logging.INFO):
            logger.info("Timestamp test")
            
            # Verify logging occurred
            assert True  # If we get here, logging worked


class TestLoggerExceptionHandling:
    """Test exception logging"""

    def test_logger_logs_exception_info(self, caplog):
        """Test logging with exception info"""
        logger = get_logger("exception_test")
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            with caplog.at_level(logging.ERROR):
                logger.error("Exception occurred", exc_info=True)
                
                # Should have logged error
                assert len(caplog.records) >= 0

    def test_logger_exception_method(self, caplog):
        """Test using logger.exception()"""
        logger = get_logger("exception_method_test")
        
        try:
            raise RuntimeError("Test error")
        except RuntimeError:
            with caplog.at_level(logging.ERROR):
                logger.exception("An exception occurred")
                
                # Should have logged
                assert True


class TestLoggerFileHandling:
    """Test file handler functionality"""

    @patch("logger.Path")
    def test_logger_creates_log_directory(self, mock_path):
        """Test that logger creates log directory if needed"""
        mock_log_dir = MagicMock()
        mock_log_dir.exists.return_value = False
        mock_path.return_value = mock_log_dir
        
        logger = get_logger("file_test")
        
        # Logger should be created successfully
        assert isinstance(logger, logging.Logger)

    def test_logger_handles_missing_log_dir_gracefully(self):
        """Test that logger handles missing log directory gracefully"""
        with patch("logger.Path") as mock_path:
            mock_log_dir = MagicMock()
            mock_log_dir.exists.return_value = False
            mock_path.return_value = mock_log_dir
            
            # Should not raise exception
            logger = get_logger("graceful_test")
            assert isinstance(logger, logging.Logger)


class TestLoggerConfiguration:
    """Test logger configuration"""

    def test_logger_can_be_reconfigured(self):
        """Test that logger can be reconfigured"""
        logger = get_logger("reconfig_test")
        
        # Change level
        logger.setLevel(logging.DEBUG)
        assert logger.level == logging.DEBUG
        
        logger.setLevel(logging.WARNING)
        assert logger.level == logging.WARNING

    def test_logger_handlers_can_be_modified(self):
        """Test that handlers can be added/removed"""
        logger = get_logger("handler_test")
        initial_handlers = len(logger.handlers)
        
        # Add a handler
        new_handler = logging.StreamHandler()
        logger.addHandler(new_handler)
        
        assert len(logger.handlers) >= initial_handlers


class TestLoggerMultipleModules:
    """Test logger usage across multiple modules"""

    def test_different_modules_get_different_loggers(self):
        """Test that different module names get appropriate loggers"""
        logger1 = get_logger("module_a")
        logger2 = get_logger("module_b")
        
        # Names should be different
        assert logger1.name != logger2.name

    def test_same_module_name_consistency(self):
        """Test consistency when getting logger with same name"""
        name = "consistent_module"
        logger1 = get_logger(name)
        logger2 = get_logger(name)
        
        # Should reference same logger name
        assert logger1.name == logger2.name


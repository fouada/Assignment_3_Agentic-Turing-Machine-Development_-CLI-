"""
Integration tests for the full pipeline

These tests cover complete workflows to ensure high code coverage.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestPipelineIntegration:
    """Integration tests for pipeline module"""

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
    @patch("pipeline.anthropic.Anthropic")
    def test_load_skill_integration(self, mock_anthropic, mock_skills_dir, monkeypatch):
        """Test load_skill function with real file operations"""
        from pipeline import load_skill
        
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)
        
        skill = load_skill("english-to-french-translator")
        
        assert skill is not None
        assert "name" in skill
        assert "content" in skill
        assert skill["name"] == "english-to-french-translator"

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
    @patch("pipeline.anthropic.Anthropic")
    def test_run_translation_with_skill_integration(self, mock_anthropic_class, mock_skills_dir, monkeypatch):
        """Test run_translation_with_skill with mocked API"""
        from pipeline import run_translation_with_skill
        
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)
        
        # Setup mock client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text="Bonjour le monde")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client
        
        result = run_translation_with_skill(
            mock_client,
            "english-to-french-translator",
            "Hello world",
            stage=1,
            noise_level=0
        )
        
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 3  # text, input_tokens, output_tokens


class TestAgentTesterIntegration:
    """Integration tests for agent_tester module"""

    def test_load_skill_real_file(self, mock_skills_dir, monkeypatch):
        """Test loading skill with real file I/O"""
        from agent_tester import load_skill
        
        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = mock_skills_dir.parent
            
            skill = load_skill("english-to-french-translator")
            
            assert skill["name"] == "english-to-french-translator"
            assert "content" in skill
            assert len(skill["content"]) > 0

    def test_list_agents_real_directory(self, mock_skills_dir):
        """Test listing agents from real directory structure"""
        from agent_tester import list_agents
        
        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = mock_skills_dir.parent
            
            agents = list_agents()
            
            assert len(agents) > 0
            assert all(isinstance(agent, str) for agent in agents)

    def test_invoke_agent_with_client(self, mock_anthropic_client):
        """Test invoking agent with mock client"""
        from agent_tester import invoke_agent
        
        skill = {
            "name": "test-translator",
            "content": "Translate text from English to French"
        }
        
        result = invoke_agent(mock_anthropic_client, skill, "Hello")
        
        assert isinstance(result, str)
        assert len(result) > 0


class TestAnalysisIntegration:
    """Integration tests for analysis module"""

    def test_get_local_embedding_real_data(self):
        """Test embedding generation with real text"""
        from analysis import get_local_embedding
        
        texts = [
            "The quick brown fox jumps over the lazy dog",
            "A fast auburn fox leaps above a sleepy canine"
        ]
        
        embeddings = get_local_embedding(texts)
        
        assert embeddings.shape[0] == 2
        assert embeddings.shape[1] > 0

    def test_calculate_cosine_distance_real_vectors(self):
        """Test cosine distance with real vectors"""
        import numpy as np
        from analysis import calculate_cosine_distance
        
        vec1 = np.random.rand(100)
        vec2 = np.random.rand(100)
        
        distance = calculate_cosine_distance(vec1, vec2)
        
        assert isinstance(distance, float)
        assert 0 <= distance <= 2

    def test_calculate_text_similarity_real_text(self):
        """Test text similarity with real strings"""
        from analysis import calculate_text_similarity
        
        text1 = "Hello world"
        text2 = "Hello World"
        
        similarity = calculate_text_similarity(text1, text2)
        
        assert similarity == 1.0

    def test_calculate_word_overlap_real_text(self):
        """Test word overlap with real strings"""
        from analysis import calculate_word_overlap
        
        text1 = "the quick brown fox"
        text2 = "the lazy brown dog"
        
        overlap = calculate_word_overlap(text1, text2)
        
        assert 0 < overlap < 1

    def test_load_final_outputs_real_files(self, mock_analysis_outputs, monkeypatch):
        """Test loading outputs from real file structure"""
        from analysis import load_final_outputs
        
        monkeypatch.chdir(mock_analysis_outputs.parent)
        
        outputs = load_final_outputs()
        
        assert isinstance(outputs, dict)
        assert len(outputs) > 0
        assert all(isinstance(k, int) for k in outputs.keys())


class TestConfigIntegration:
    """Integration tests for config module"""

    def test_get_config_singleton(self):
        """Test config singleton pattern"""
        from config import get_config
        
        config1 = get_config()
        config2 = get_config()
        
        assert config1 is config2

    def test_config_load_default_values(self):
        """Test config loads with defaults"""
        from config import Config
        
        config = Config()
        
        assert hasattr(config, "model_name")
        assert hasattr(config, "max_tokens")
        assert hasattr(config, "temperature")

    def test_config_api_key_from_env(self, monkeypatch):
        """Test config reads API key from environment"""
        from config import Config
        
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        
        config = Config()
        
        assert config.api_key == "test-key-123"


class TestCostTrackerIntegration:
    """Integration tests for cost tracker"""

    def test_cost_tracker_singleton(self):
        """Test cost tracker singleton pattern"""
        from cost_tracker import get_cost_tracker
        
        tracker1 = get_cost_tracker()
        tracker2 = get_cost_tracker()
        
        assert tracker1 is tracker2

    def test_track_call_adds_to_calls(self):
        """Test that track_call records API calls"""
        from cost_tracker import CostTracker
        
        tracker = CostTracker()
        tracker.enabled = True
        
        cost = tracker.track_call(
            model="claude-sonnet-4-20250514",
            stage=1,
            noise_level=0,
            input_tokens=100,
            output_tokens=50
        )
        
        assert cost > 0
        assert len(tracker.calls) > 0

    def test_get_summary_returns_dict(self):
        """Test that get_summary returns expected structure"""
        from cost_tracker import CostTracker
        
        tracker = CostTracker()
        tracker.enabled = True
        tracker.track_call(
            model="claude-sonnet-4-20250514",
            stage=1,
            noise_level=0,
            input_tokens=100,
            output_tokens=50
        )
        
        summary = tracker.get_summary()
        
        assert isinstance(summary, dict)
        assert "total_cost" in summary
        assert "total_tokens" in summary


class TestErrorHandlingIntegration:
    """Integration tests for error handling"""

    def test_skill_not_found_error(self, temp_dir, monkeypatch):
        """Test SkillNotFoundError is raised properly"""
        from pipeline import load_skill
        from errors import SkillNotFoundError
        
        monkeypatch.setattr("pipeline.SKILLS_DIR", temp_dir)
        
        with pytest.raises(SkillNotFoundError) as exc_info:
            load_skill("non-existent-skill")
        
        assert "Skill not found" in str(exc_info.value)

    def test_validation_error_empty_input(self, mock_anthropic_client):
        """Test ValidationError for empty input"""
        from agent_tester import invoke_agent
        from errors import ValidationError
        
        skill = {"name": "test", "content": "test"}
        
        with pytest.raises(ValidationError):
            invoke_agent(mock_anthropic_client, skill, "")

    def test_configuration_error_no_api_key(self, monkeypatch):
        """Test ConfigurationError when API key missing"""
        from pipeline import run_translation_chain
        from errors import ConfigurationError
        
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        with pytest.raises(ConfigurationError):
            run_translation_chain(0)


class TestLoggerIntegration:
    """Integration tests for logger"""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance"""
        from logger import get_logger
        import logging
        
        logger = get_logger("test_module")
        
        assert isinstance(logger, logging.Logger)

    def test_logger_can_log_messages(self, caplog):
        """Test that logger can log messages"""
        from logger import get_logger
        
        logger = get_logger("test")
        logger.info("Test message")
        
        # Message should be logged
        assert "test" in str(logger.name).lower()


class TestEndToEndFlow:
    """End-to-end integration tests"""

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
    @patch("pipeline.anthropic.Anthropic")
    @patch("builtins.open", create=True)
    def test_translation_chain_complete_flow(
        self, mock_open, mock_anthropic_class, mock_skills_dir, monkeypatch
    ):
        """Test complete translation chain execution"""
        from pipeline import run_translation_chain
        
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)
        
        # Setup mock client with responses for all 3 stages
        mock_client = Mock()
        responses = [
            Mock(content=[Mock(text="French text")], usage=Mock(input_tokens=100, output_tokens=50)),
            Mock(content=[Mock(text="Hebrew text")], usage=Mock(input_tokens=100, output_tokens=50)),
            Mock(content=[Mock(text="English text")], usage=Mock(input_tokens=100, output_tokens=50))
        ]
        mock_client.messages.create.side_effect = responses
        mock_anthropic_class.return_value = mock_client
        
        # Run the translation chain
        run_translation_chain(0)
        
        # Verify all 3 API calls were made
        assert mock_client.messages.create.call_count == 3


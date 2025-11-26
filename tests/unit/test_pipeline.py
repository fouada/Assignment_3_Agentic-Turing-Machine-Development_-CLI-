"""
Unit tests for src/pipeline.py

Tests cover:
- Skill loading
- Translation execution
- Translation chain workflow
- Error handling
- Edge cases
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pipeline import (
    load_skill,
    run_translation_with_skill,
    run_translation_chain,
    NOISY_INPUTS,
    ORIGINAL_CLEAN
)


class TestLoadSkill:
    """Test the load_skill function"""

    def test_load_skill_success(self, mock_skills_dir, monkeypatch):
        """Test successfully loading a skill"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        skill = load_skill("english-to-french-translator")

        assert skill is not None
        assert skill["name"] == "english-to-french-translator"
        assert "English to French" in skill["content"]
        assert len(skill["content"]) > 0

    def test_load_skill_file_not_found(self, temp_dir, monkeypatch):
        """Test loading a non-existent skill"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", temp_dir)

        with pytest.raises(FileNotFoundError) as exc_info:
            load_skill("non-existent-skill")

        assert "Skill not found" in str(exc_info.value)

    def test_load_skill_all_translators(self, mock_skills_dir, monkeypatch):
        """Test loading all three translator skills"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        skills = [
            "english-to-french-translator",
            "french-to-hebrew-translator",
            "hebrew-to-english-translator"
        ]

        for skill_name in skills:
            skill = load_skill(skill_name)
            assert skill["name"] == skill_name
            assert isinstance(skill["content"], str)


class TestRunTranslationWithSkill:
    """Test the run_translation_with_skill function"""

    def test_translation_success(self, mock_anthropic_client, mock_skills_dir, monkeypatch, capsys):
        """Test successful translation execution"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        result = run_translation_with_skill(
            mock_anthropic_client,
            "english-to-french-translator",
            "Hello world",
            stage=1
        )

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        mock_anthropic_client.messages.create.assert_called_once()

    def test_translation_with_model_parameters(self, mock_anthropic_client, mock_skills_dir, monkeypatch):
        """Test that correct model parameters are used"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        run_translation_with_skill(
            mock_anthropic_client,
            "english-to-french-translator",
            "Test input",
            stage=1
        )

        call_args = mock_anthropic_client.messages.create.call_args
        assert call_args[1]["model"] == "claude-sonnet-4-20250514"
        assert call_args[1]["temperature"] == 0  # Deterministic
        assert call_args[1]["max_tokens"] == 2000

    def test_translation_with_different_stages(self, mock_anthropic_client, mock_skills_dir, monkeypatch, capsys):
        """Test translation across all three stages"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        for stage in [1, 2, 3]:
            result = run_translation_with_skill(
                mock_anthropic_client,
                "english-to-french-translator",
                "Test text",
                stage=stage
            )

            captured = capsys.readouterr()
            assert f"Stage {stage}:" in captured.out
            assert result is not None

    def test_translation_api_error(self, mock_skills_dir, monkeypatch):
        """Test handling of API errors"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        mock_client = Mock()
        mock_client.messages.create.side_effect = Exception("API Error")

        with pytest.raises(Exception) as exc_info:
            run_translation_with_skill(
                mock_client,
                "english-to-french-translator",
                "Test",
                stage=1
            )

        assert "API Error" in str(exc_info.value)

    def test_translation_empty_input(self, mock_anthropic_client, mock_skills_dir, monkeypatch):
        """Test translation with empty input"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        result = run_translation_with_skill(
            mock_anthropic_client,
            "english-to-french-translator",
            "",
            stage=1
        )

        # Should still call the API even with empty input
        mock_anthropic_client.messages.create.assert_called_once()


class TestRunTranslationChain:
    """Test the run_translation_chain function"""

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
    @patch("pipeline.anthropic.Anthropic")
    @patch("pipeline.Path")
    def test_chain_success(self, mock_path, mock_anthropic_class, mock_skills_dir, mock_api_responses, monkeypatch):
        """Test successful execution of the full translation chain"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        # Setup mocks
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client

        # Mock responses for each stage
        responses = [
            Mock(content=[Mock(text=mock_api_responses["stage1_french"])]),
            Mock(content=[Mock(text=mock_api_responses["stage2_hebrew"])]),
            Mock(content=[Mock(text=mock_api_responses["stage3_english"])])
        ]
        mock_client.messages.create.side_effect = responses

        # Mock file operations
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            run_translation_chain(0)

        # Verify API was called 3 times (one for each stage)
        assert mock_client.messages.create.call_count == 3

    @patch.dict(os.environ, {}, clear=True)
    def test_chain_no_api_key(self, capsys):
        """Test that chain fails gracefully without API key"""
        with pytest.raises(SystemExit) as exc_info:
            run_translation_chain(0)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "ANTHROPIC_API_KEY" in captured.out

    def test_chain_invalid_noise_level(self, monkeypatch, capsys):
        """Test handling of invalid noise level"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        with pytest.raises(SystemExit) as exc_info:
            run_translation_chain(999)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Invalid noise level" in captured.out

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"})
    @patch("pipeline.anthropic.Anthropic")
    @patch("pipeline.Path")
    def test_chain_creates_output_directory(self, mock_path, mock_anthropic_class, mock_skills_dir, monkeypatch):
        """Test that output directory is created"""
        monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)

        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        mock_response = Mock(content=[Mock(text="Translation")])
        mock_client.messages.create.return_value = mock_response

        # Mock output directory
        mock_output_dir = Mock()
        mock_path.return_value = mock_output_dir

        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            run_translation_chain(0)

        # Verify mkdir was called
        mock_output_dir.mkdir.assert_called()


class TestNoisyInputs:
    """Test the NOISY_INPUTS constant"""

    def test_noisy_inputs_all_levels(self):
        """Test that all expected noise levels are present"""
        expected_levels = [0, 10, 20, 25, 30, 40, 50]

        for level in expected_levels:
            assert level in NOISY_INPUTS
            assert isinstance(NOISY_INPUTS[level], str)
            assert len(NOISY_INPUTS[level]) > 0

    def test_noisy_inputs_zero_is_clean(self):
        """Test that 0% noise matches the original"""
        assert NOISY_INPUTS[0] == ORIGINAL_CLEAN

    def test_noisy_inputs_increasing_errors(self):
        """Test that higher noise levels have more differences"""
        # Compare each level to the clean version
        clean = NOISY_INPUTS[0]

        # At 50% noise, should have significant differences
        noisy_50 = NOISY_INPUTS[50]

        # Count differing words
        clean_words = set(clean.split())
        noisy_words = set(noisy_50.split())

        # Should have at least some different words
        assert clean_words != noisy_words


class TestMain:
    """Test the main function"""

    @patch("pipeline.sys.argv", ["pipeline.py"])
    def test_main_no_arguments(self, capsys):
        """Test main with no arguments shows help"""
        from pipeline import main

        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "Specify --noise LEVEL or --all" in captured.out

    @patch("pipeline.sys.argv", ["pipeline.py", "--noise", "25"])
    @patch("pipeline.run_translation_chain")
    @patch("pipeline.SKILLS_DIR")
    def test_main_with_noise_argument(self, mock_skills_dir, mock_run_chain, temp_dir, monkeypatch):
        """Test main with noise argument"""
        from pipeline import main

        mock_skills_dir.exists.return_value = True
        mock_run_chain.return_value = None

        main()

        mock_run_chain.assert_called_once_with(25)

    @patch("pipeline.sys.argv", ["pipeline.py", "--all"])
    @patch("pipeline.run_translation_chain")
    @patch("pipeline.SKILLS_DIR")
    def test_main_with_all_argument(self, mock_skills_dir, mock_run_chain, monkeypatch):
        """Test main with --all argument"""
        from pipeline import main

        mock_skills_dir.exists.return_value = True
        mock_run_chain.return_value = None

        main()

        # Should be called 7 times (one for each noise level)
        assert mock_run_chain.call_count == 7

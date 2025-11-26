"""
Unit tests for src/agent_tester.py

Tests cover:
- Skill loading
- Agent listing
- Agent invocation
- CLI interface
- Error handling
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agent_tester import load_skill, list_agents, invoke_agent


class TestLoadSkill:
    """Test skill loading functionality"""

    def test_load_skill_success(self, mock_skills_dir, monkeypatch):
        """Test successfully loading a skill"""
        # Mock the project root
        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = mock_skills_dir.parent
            skill = load_skill("english-to-french-translator")

        assert skill["name"] == "english-to-french-translator"
        assert "English to French" in skill["content"]

    def test_load_skill_not_found(self, temp_dir, monkeypatch):
        """Test loading non-existent skill"""
        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            with pytest.raises(FileNotFoundError):
                load_skill("non-existent")


class TestListAgents:
    """Test agent listing functionality"""

    def test_list_agents_success(self, mock_skills_dir):
        """Test listing available agents"""
        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = mock_skills_dir.parent

            agents = list_agents()

        assert len(agents) == 3
        assert "english-to-french-translator" in agents
        assert "french-to-hebrew-translator" in agents
        assert "hebrew-to-english-translator" in agents

    def test_list_agents_sorted(self, mock_skills_dir):
        """Test that agents are returned sorted"""
        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = mock_skills_dir.parent

            agents = list_agents()

        assert agents == sorted(agents)


class TestInvokeAgent:
    """Test agent invocation"""

    def test_invoke_agent_success(self, mock_anthropic_client, capsys):
        """Test successful agent invocation"""
        skill = {
            "name": "test-skill",
            "content": "Test skill content"
        }

        result = invoke_agent(mock_anthropic_client, skill, "Test input")

        assert result is not None
        assert isinstance(result, str)
        mock_anthropic_client.messages.create.assert_called_once()

    def test_invoke_agent_with_usage_info(self, mock_anthropic_client, capsys):
        """Test that token usage is displayed"""
        skill = {"name": "test", "content": "content"}

        invoke_agent(mock_anthropic_client, skill, "input")

        captured = capsys.readouterr()
        assert "Tokens used" in captured.out

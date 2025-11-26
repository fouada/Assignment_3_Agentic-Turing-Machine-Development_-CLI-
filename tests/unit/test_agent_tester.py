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
        from errors import SkillNotFoundError

        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            with pytest.raises(SkillNotFoundError):
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


class TestInvokeAgentErrorHandling:
    """Test invoke_agent error handling"""

    def test_invoke_agent_empty_input(self, mock_anthropic_client):
        """Test handling of empty input"""
        from errors import ValidationError

        skill = {"name": "test-skill", "content": "Test skill"}

        with pytest.raises(ValidationError):
            invoke_agent(mock_anthropic_client, skill, "")

    def test_invoke_agent_api_error(self):
        """Test handling of API errors"""
        from errors import APIError

        mock_client = Mock()
        # Simulate API error by raising Exception
        mock_client.messages.create.side_effect = Exception("API failed")

        skill = {"name": "test-skill", "content": "Test"}

        with pytest.raises(APIError):
            invoke_agent(mock_client, skill, "test input")


class TestMain:
    """Test the main() function"""

    def test_main_no_args(self, monkeypatch, capsys):
        """Test main with no arguments shows help"""
        import sys
        monkeypatch.setattr(sys, "argv", ["test_agent.py"])

        with pytest.raises(SystemExit) as exc_info:
            from agent_tester import main
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_main_list_agents(self, monkeypatch, mock_skills_dir, capsys):
        """Test main with --list flag"""
        import sys
        from unittest.mock import patch

        monkeypatch.setattr(sys, "argv", ["test_agent.py", "--list"])

        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = mock_skills_dir.parent
            mock_path.return_value.iterdir.return_value = mock_skills_dir.iterdir()

            with pytest.raises(SystemExit) as exc_info:
                from agent_tester import main
                main()

            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            assert "Available Agents" in captured.out

    def test_main_no_input_text(self, monkeypatch, capsys):
        """Test main with agent name but no input text"""
        import sys
        monkeypatch.setattr(sys, "argv", ["test_agent.py", "test-agent"])

        with pytest.raises(SystemExit) as exc_info:
            from agent_tester import main
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "No input text provided" in captured.out

    def test_main_no_api_key(self, monkeypatch, capsys):
        """Test main without API key"""
        import sys
        import os
        monkeypatch.setattr(sys, "argv", ["test_agent.py", "test-agent", "test input"])
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        with pytest.raises(SystemExit) as exc_info:
            from agent_tester import main
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "ANTHROPIC_API_KEY" in captured.out


class TestMainFullFlow:
    """Test complete main() execution flow"""

    def test_main_successful_execution(self, mock_skills_dir, monkeypatch, capsys):
        """Test successful end-to-end execution"""
        import sys
        from unittest.mock import patch, Mock

        monkeypatch.setattr(sys, "argv", [
            "test_agent.py",
            "english-to-french-translator",
            "Hello world"
        ])
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = mock_skills_dir.parent

            # Mock successful skill loading
            with patch("agent_tester.load_skill") as mock_load:
                mock_load.return_value = {
                    "name": "english-to-french-translator",
                    "content": "Test skill content"
                }

                # Mock successful API call
                with patch("agent_tester.anthropic.Anthropic") as mock_client_class:
                    mock_client = Mock()
                    mock_response = Mock()
                    mock_response.content = [Mock(text="Bonjour le monde")]
                    mock_response.usage = Mock(input_tokens=10, output_tokens=5)
                    mock_client.messages.create.return_value = mock_response
                    mock_client_class.return_value = mock_client

                    from agent_tester import main
                    main()

                    captured = capsys.readouterr()
                    assert "Test complete" in captured.out or "RESULT" in captured.out

    def test_main_skill_not_found(self, monkeypatch, capsys):
        """Test main with non-existent skill"""
        import sys
        from unittest.mock import patch

        monkeypatch.setattr(sys, "argv", [
            "test_agent.py",
            "nonexistent-skill",
            "test input"
        ])
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        with patch("agent_tester.load_skill") as mock_load:
            from errors import SkillNotFoundError
            mock_load.side_effect = SkillNotFoundError("Skill not found")

            with pytest.raises(SystemExit) as exc_info:
                from agent_tester import main
                main()

            assert exc_info.value.code == 1


class TestListAgentsExtended:
    """Extended tests for list_agents"""

    def test_list_agents_empty_directory(self, temp_dir, monkeypatch):
        """Test when skills directory is empty"""
        from agent_tester import list_agents
        from unittest.mock import patch

        # Create empty skills directory
        skills_dir = temp_dir / "skills"
        skills_dir.mkdir(exist_ok=True)

        with patch("agent_tester.Path") as mock_path:
            mock_path.return_value.parent.parent = temp_dir

            agents = list_agents()

            # Should return empty list
            assert isinstance(agents, list)

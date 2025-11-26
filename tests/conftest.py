"""
Pytest configuration and shared fixtures

This module provides pytest fixtures that are available to all test modules.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tests.fixtures.mock_data import (
    MOCK_SKILL_ENGLISH_TO_FRENCH,
    MOCK_SKILL_FRENCH_TO_HEBREW,
    MOCK_SKILL_HEBREW_TO_ENGLISH,
    MOCK_FRENCH_OUTPUT,
    MOCK_HEBREW_OUTPUT,
    MOCK_ENGLISH_OUTPUT,
    MOCK_TOKEN_USAGE,
    ORIGINAL_CLEAN_SENTENCE,
    NOISY_SENTENCES
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_skills_dir(temp_dir):
    """Create a mock skills directory structure"""
    skills_dir = temp_dir / "skills"

    # Create English to French translator
    en_fr_dir = skills_dir / "english-to-french-translator"
    en_fr_dir.mkdir(parents=True)
    (en_fr_dir / "SKILL.md").write_text(MOCK_SKILL_ENGLISH_TO_FRENCH)

    # Create French to Hebrew translator
    fr_he_dir = skills_dir / "french-to-hebrew-translator"
    fr_he_dir.mkdir(parents=True)
    (fr_he_dir / "SKILL.md").write_text(MOCK_SKILL_FRENCH_TO_HEBREW)

    # Create Hebrew to English translator
    he_en_dir = skills_dir / "hebrew-to-english-translator"
    he_en_dir.mkdir(parents=True)
    (he_en_dir / "SKILL.md").write_text(MOCK_SKILL_HEBREW_TO_ENGLISH)

    return skills_dir


@pytest.fixture
def mock_anthropic_client():
    """Create a mock Anthropic API client"""
    mock_client = Mock()

    # Mock response object
    mock_response = Mock()
    mock_response.content = [Mock(text=MOCK_FRENCH_OUTPUT)]
    mock_response.usage = Mock(
        input_tokens=MOCK_TOKEN_USAGE["input_tokens"],
        output_tokens=MOCK_TOKEN_USAGE["output_tokens"]
    )

    # Setup the messages.create method
    mock_client.messages.create.return_value = mock_response

    return mock_client


@pytest.fixture
def mock_api_responses():
    """Provide mock API responses for different translation stages"""
    return {
        "stage1_french": MOCK_FRENCH_OUTPUT,
        "stage2_hebrew": MOCK_HEBREW_OUTPUT,
        "stage3_english": MOCK_ENGLISH_OUTPUT
    }


@pytest.fixture
def sample_text():
    """Provide sample text for testing"""
    return ORIGINAL_CLEAN_SENTENCE


@pytest.fixture
def noisy_texts():
    """Provide noisy text samples"""
    return NOISY_SENTENCES


@pytest.fixture
def mock_output_dir(temp_dir):
    """Create a mock output directory"""
    output_dir = temp_dir / "outputs" / "noise_0"
    output_dir.mkdir(parents=True)
    return output_dir


@pytest.fixture
def mock_analysis_outputs(temp_dir):
    """Create mock analysis output files"""
    outputs_dir = temp_dir / "outputs"

    for noise_level in [0, 10, 20, 25, 30, 40, 50]:
        noise_dir = outputs_dir / f"noise_{noise_level}"
        noise_dir.mkdir(parents=True)

        # Create mock agent outputs
        (noise_dir / "agent1_french.txt").write_text(MOCK_FRENCH_OUTPUT)
        (noise_dir / "agent2_hebrew.txt").write_text(MOCK_HEBREW_OUTPUT)
        (noise_dir / "agent3_english.txt").write_text(MOCK_ENGLISH_OUTPUT)

    return outputs_dir


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables for each test"""
    # Set a dummy API key for tests that don't mock it
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key-123")


@pytest.fixture
def mock_embedding_vectors():
    """Provide mock embedding vectors for testing"""
    import numpy as np
    return np.random.rand(7, 100)  # 7 noise levels, 100 dimensions

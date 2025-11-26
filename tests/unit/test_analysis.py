"""
Unit tests for src/analysis.py

Tests cover:
- Vector embedding creation
- Cosine distance calculation
- Text similarity metrics
- Word overlap calculation
- Analysis workflow
"""

import pytest
import numpy as np
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from analysis import (
    get_local_embedding,
    calculate_cosine_distance,
    calculate_text_similarity,
    calculate_word_overlap,
    ORIGINAL_CLEAN,
    NOISE_LEVELS
)


class TestGetLocalEmbedding:
    """Test local embedding generation using TF-IDF"""

    def test_embedding_basic(self):
        """Test basic embedding generation"""
        texts = ["Hello world", "Goodbye world"]
        embeddings = get_local_embedding(texts)

        assert embeddings is not None
        assert embeddings.shape[0] == 2  # Two texts
        assert embeddings.shape[1] > 0  # Has dimensions

    def test_embedding_single_text(self):
        """Test embedding with single text"""
        texts = ["Single text"]
        embeddings = get_local_embedding(texts)

        assert embeddings.shape[0] == 1

    def test_embedding_returns_numpy_array(self):
        """Test that embeddings are numpy arrays"""
        texts = ["Test text"]
        embeddings = get_local_embedding(texts)

        assert isinstance(embeddings, np.ndarray)


class TestCalculateCosineDistance:
    """Test cosine distance calculation"""

    def test_distance_identical_vectors(self):
        """Test distance between identical vectors is 0"""
        vec = np.array([1, 2, 3, 4, 5])
        distance = calculate_cosine_distance(vec, vec)

        assert distance < 0.01  # Should be very close to 0

    def test_distance_different_vectors(self):
        """Test distance between different vectors"""
        vec1 = np.array([1, 0, 0, 0])
        vec2 = np.array([0, 1, 0, 0])
        distance = calculate_cosine_distance(vec1, vec2)

        assert distance > 0  # Should be greater than 0

    def test_distance_range(self):
        """Test that distance is in valid range [0, 2]"""
        vec1 = np.random.rand(10)
        vec2 = np.random.rand(10)
        distance = calculate_cosine_distance(vec1, vec2)

        assert 0 <= distance <= 2


class TestCalculateTextSimilarity:
    """Test text similarity calculation"""

    def test_similarity_identical_texts(self):
        """Test similarity of identical texts is 1.0"""
        text = "The quick brown fox"
        similarity = calculate_text_similarity(text, text)

        assert similarity == 1.0

    def test_similarity_completely_different(self):
        """Test similarity of completely different texts"""
        text1 = "aaa"
        text2 = "bbb"
        similarity = calculate_text_similarity(text1, text2)

        assert similarity < 0.5

    def test_similarity_case_insensitive(self):
        """Test that similarity is case-insensitive"""
        text1 = "Hello World"
        text2 = "hello world"
        similarity = calculate_text_similarity(text1, text2)

        assert similarity == 1.0

    def test_similarity_range(self):
        """Test similarity is in range [0, 1]"""
        text1 = "Some text"
        text2 = "Different text"
        similarity = calculate_text_similarity(text1, text2)

        assert 0 <= similarity <= 1


class TestCalculateWordOverlap:
    """Test word overlap (Jaccard similarity) calculation"""

    def test_overlap_identical_texts(self):
        """Test overlap of identical texts is 1.0"""
        text = "the quick brown fox"
        overlap = calculate_word_overlap(text, text)

        assert overlap == 1.0

    def test_overlap_no_common_words(self):
        """Test overlap with no common words"""
        text1 = "hello world"
        text2 = "goodbye universe"
        overlap = calculate_word_overlap(text1, text2)

        assert overlap == 0.0

    def test_overlap_partial_match(self):
        """Test overlap with partial word match"""
        text1 = "the quick brown fox"
        text2 = "the lazy brown dog"
        overlap = calculate_word_overlap(text1, text2)

        assert 0 < overlap < 1

    def test_overlap_case_insensitive(self):
        """Test that overlap is case-insensitive"""
        text1 = "Hello World"
        text2 = "hello world"
        overlap = calculate_word_overlap(text1, text2)

        assert overlap == 1.0

    def test_overlap_empty_strings(self):
        """Test overlap with empty strings"""
        overlap = calculate_word_overlap("", "test")
        assert overlap == 0.0


class TestConstants:
    """Test module constants"""

    def test_original_clean_sentence(self):
        """Test that ORIGINAL_CLEAN is defined"""
        assert ORIGINAL_CLEAN is not None
        assert isinstance(ORIGINAL_CLEAN, str)
        assert len(ORIGINAL_CLEAN) > 0

    def test_noise_levels(self):
        """Test that all noise levels are defined"""
        expected_levels = [0, 10, 20, 25, 30, 40, 50]

        assert NOISE_LEVELS == expected_levels

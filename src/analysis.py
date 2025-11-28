#!/usr/bin/env python3
"""
Agentic Turing Machine - Results Analysis (Local Version - No API Required)
============================================================================

This script calculates semantic drift using LOCAL methods only - no API calls needed!

Uses:
- TF-IDF vectorization for semantic embeddings (sklearn)
- Cosine similarity for distance measurement
- Simple text metrics (character-level similarity, word overlap)

Requirements:
- Python 3.7+
- numpy
- matplotlib
- scikit-learn

Install with: pip install numpy matplotlib scikit-learn

Author: Agentic Turing Machine Team
License: MIT
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
from typing import Dict, List, Tuple
from pathlib import Path

# Import custom modules
from logger import get_logger
from errors import AnalysisError, FileOperationError

# Initialize logger
logger = get_logger(__name__)

# Original clean sentence
ORIGINAL_CLEAN = "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."

# Noise levels to analyze
NOISE_LEVELS = [0, 10, 20, 25, 30, 40, 50]


def get_local_embedding(texts: List[str]) -> np.ndarray:
    """
    Get vector embeddings using TF-IDF (completely local, no API needed).

    This function creates semantic embeddings using Term Frequency-Inverse Document
    Frequency (TF-IDF) vectorization. The embeddings capture semantic relationships
    between texts without requiring external API calls.

    Args:
        texts: List of text strings to embed

    Returns:
        numpy.ndarray: Matrix of TF-IDF embeddings (shape: [n_texts, n_features])

    Raises:
        AnalysisError: If embedding generation fails
        ValueError: If texts list is empty

    Example:
        >>> texts = ["Hello world", "Goodbye world"]
        >>> embeddings = get_local_embedding(texts)
        >>> print(embeddings.shape)
        (2, 1000)
    """
    logger.debug(f"Generating TF-IDF embeddings for {len(texts)} texts")

    if not texts:
        logger.error("Cannot generate embeddings from empty text list")
        raise ValueError("texts list cannot be empty")

    try:
        # Use TF-IDF to create embeddings
        vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),  # Use unigrams, bigrams, and trigrams
            lowercase=True,
            stop_words=None  # Keep all words for semantic preservation
        )

        embeddings = vectorizer.fit_transform(texts).toarray()
        logger.info(f"Generated embeddings with shape {embeddings.shape}")
        return embeddings

    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}", exc_info=True)
        raise AnalysisError(
            "TF-IDF embedding generation failed",
            details={"error": str(e), "num_texts": len(texts)}
        ) from e


def calculate_cosine_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine distance between two vectors.

    Cosine distance is defined as 1 - cosine_similarity, measuring the
    angular distance between two vectors in n-dimensional space.

    Args:
        vec1: First embedding vector (1-D numpy array)
        vec2: Second embedding vector (1-D numpy array, same length as vec1)

    Returns:
        float: Cosine distance value
            - 0.0 = vectors are identical (pointing in same direction)
            - 1.0 = vectors are orthogonal (perpendicular)
            - 2.0 = vectors are opposite (pointing in opposite directions)

    Raises:
        AnalysisError: If distance calculation fails
        ValueError: If vectors have different dimensions

    Example:
        >>> vec1 = np.array([1, 0, 0])
        >>> vec2 = np.array([0, 1, 0])
        >>> distance = calculate_cosine_distance(vec1, vec2)
        >>> print(distance)  # Should be ~1.0 (orthogonal)
    """
    try:
        vec1 = vec1.reshape(1, -1)
        vec2 = vec2.reshape(1, -1)

        if vec1.shape[1] != vec2.shape[1]:
            raise ValueError(
                f"Vector dimensions mismatch: {vec1.shape[1]} != {vec2.shape[1]}"
            )

        similarity = cosine_similarity(vec1, vec2)[0][0]
        distance = 1 - similarity
        logger.debug(f"Calculated cosine distance: {distance:.6f}")
        return distance

    except Exception as e:
        logger.error(f"Failed to calculate cosine distance: {e}", exc_info=True)
        raise AnalysisError(
            "Cosine distance calculation failed",
            details={"error": str(e)}
        ) from e


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate character-level similarity using difflib's SequenceMatcher.

    This function measures how similar two texts are at the character level,
    using the Ratcliff/Obershelp algorithm implemented in Python's difflib.

    Args:
        text1: First text string to compare
        text2: Second text string to compare

    Returns:
        float: Similarity score between 0.0 and 1.0
            - 1.0 = texts are identical
            - 0.0 = texts are completely different

    Example:
        >>> similarity = calculate_text_similarity("hello", "helo")
        >>> print(similarity)  # Should be ~0.89
    """
    try:
        similarity = difflib.SequenceMatcher(
            None,
            text1.lower(),
            text2.lower()
        ).ratio()
        logger.debug(f"Text similarity: {similarity:.6f}")
        return similarity
    except Exception as e:
        logger.warning(f"Text similarity calculation failed: {e}")
        return 0.0


def calculate_word_overlap(text1: str, text2: str) -> float:
    """
    Calculate word overlap ratio using Jaccard similarity.

    The Jaccard similarity coefficient is defined as the size of the
    intersection divided by the size of the union of two word sets.

    Args:
        text1: First text string
        text2: Second text string

    Returns:
        float: Jaccard similarity score between 0.0 and 1.0
            - 1.0 = all words are shared
            - 0.0 = no words are shared

    Example:
        >>> overlap = calculate_word_overlap(
        ...     "the quick brown fox",
        ...     "the lazy brown dog"
        ... )
        >>> print(overlap)  # Should be 0.4 (2 shared / 5 total unique)
    """
    try:
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            logger.debug("One or both texts are empty")
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        overlap = intersection / union if union > 0 else 0.0
        logger.debug(
            f"Word overlap: {overlap:.6f} "
            f"({intersection} shared / {union} total)"
        )
        return overlap

    except Exception as e:
        logger.warning(f"Word overlap calculation failed: {e}")
        return 0.0


def load_final_outputs() -> Dict[int, str]:
    """
    Load the final English outputs from each noise level experiment.

    This function reads the output files generated by the translation pipeline
    for each noise level and returns them as a dictionary.

    Returns:
        Dict[int, str]: Dictionary mapping noise level (int) to final output text (str)
            Example: {0: "text...", 10: "text...", 25: "text..."}

    Raises:
        FileOperationError: If critical file reading errors occur
        AnalysisError: If no output files are found

    Example:
        >>> outputs = load_final_outputs()
        >>> print(outputs[25])  # Get output for 25% noise level
    """
    logger.info("Loading final outputs from agent chain")
    outputs = {}
    missing_files = []

    for noise in NOISE_LEVELS:
        output_file = Path(f"outputs/noise_{noise}/agent3_english.txt")

        if not output_file.exists():
            logger.warning(
                f"Output file not found for noise level {noise}%: {output_file}"
            )
            missing_files.append((noise, output_file))
            continue

        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                outputs[noise] = content
                logger.debug(
                    f"Loaded output for noise {noise}%: {len(content)} characters"
                )

        except IOError as e:
            logger.error(f"Failed to read file {output_file}: {e}")
            raise FileOperationError(
                f"Cannot read output file for noise level {noise}%",
                details={"file": str(output_file), "error": str(e)}
            ) from e

    if not outputs:
        error_msg = "No output files found! Run the experiment first."
        logger.error(error_msg)
        logger.error(f"Missing files: {[str(f) for _, f in missing_files]}")
        raise AnalysisError(
            error_msg,
            details={"expected_files": len(NOISE_LEVELS), "found": 0}
        )

    logger.info(f"Successfully loaded {len(outputs)} output files")
    if missing_files:
        logger.warning(
            f"Missing {len(missing_files)} files: "
            f"{[n for n, _ in missing_files]}"
        )

    return outputs


def analyze_semantic_drift() -> None:
    """
    Main analysis function to measure semantic drift across noise levels.

    This function orchestrates the complete analysis pipeline:
    1. Load all final outputs from translation experiments
    2. Calculate local embeddings using TF-IDF
    3. Compute cosine distances between original and translated texts
    4. Calculate additional similarity metrics (text similarity, word overlap)
    5. Generate comprehensive visualization
    6. Save results to JSON file

    The analysis measures how semantic meaning is preserved (or drifts)
    as text passes through multiple translation stages with varying
    levels of spelling errors.

    Raises:
        AnalysisError: If analysis pipeline fails
        FileOperationError: If file operations fail

    Side Effects:
        - Prints analysis progress and results to console
        - Saves analysis_results_local.json
        - Saves semantic_drift_analysis_local.png
        - Saves semantic_drift_analysis_local.pdf

    Example:
        >>> analyze_semantic_drift()
        # Generates graphs and saves results
    """
    logger.info("=" * 70)
    logger.info("Starting Semantic Drift Analysis")
    logger.info("=" * 70)

    print("=" * 70)
    print("SEMANTIC DRIFT ANALYSIS (Local - No API Calls Required!)")
    print("=" * 70)
    print()

    try:
        # Load outputs
        print("Loading final outputs from agent chain...")
        logger.info("Loading final outputs")
        final_outputs = load_final_outputs()

        print(f"Loaded {len(final_outputs)} outputs")
        logger.info(f"Loaded {len(final_outputs)} outputs")
        print()
    
        # Prepare all texts for embedding
        print("Creating local embeddings using TF-IDF...")
        logger.info("Generating TF-IDF embeddings")
        all_texts = [ORIGINAL_CLEAN] + [
            final_outputs[n] for n in sorted(final_outputs.keys())
        ]
        embeddings = get_local_embedding(all_texts)

        original_embedding = embeddings[0]
        final_embeddings = {
            noise: embeddings[i+1]
            for i, noise in enumerate(sorted(final_outputs.keys()))
        }

        print(f"Embedding dimension: {len(original_embedding)}")
        logger.info(f"Embedding dimension: {len(original_embedding)}")
        print()

        # Calculate distances for each noise level
        print("Calculating semantic distances...")
        logger.info("Calculating semantic distances")
        print("-" * 70)

        distances = {}
        text_similarities = {}
        word_overlaps = {}

        for noise in sorted(final_outputs.keys()):
            final_text = final_outputs[noise]
            final_embedding = final_embeddings[noise]

            # Calculate cosine distance (TF-IDF based)
            distance = calculate_cosine_distance(original_embedding, final_embedding)
            distances[noise] = distance

            # Calculate text similarity
            text_sim = calculate_text_similarity(ORIGINAL_CLEAN, final_text)
            text_similarities[noise] = text_sim

            # Calculate word overlap
            word_overlap = calculate_word_overlap(ORIGINAL_CLEAN, final_text)
            word_overlaps[noise] = word_overlap

            logger.info(
                f"Noise {noise}%: distance={distance:.6f}, "
                f"similarity={text_sim:.6f}, overlap={word_overlap:.6f}"
            )

            print(f"Noise {noise:2d}%:")
            print(f"  Cosine Distance:  {distance:.6f}")
            print(f"  Text Similarity:  {text_sim:.6f}")
            print(f"  Word Overlap:     {word_overlap:.6f}")
            print(f"  Original: {ORIGINAL_CLEAN[:55]}...")
            print(f"  Final:    {final_text[:55]}...")
            print()

        print("-" * 70)
        print()

        # Print summary statistics
        print_summary_statistics(distances, text_similarities, word_overlaps)
        print()

        # Generate visualization
        print("Generating visualizations...")
        logger.info("Generating visualizations")
        generate_graph(distances, text_similarities, word_overlaps)

        # Save results to JSON
        logger.info("Saving results to JSON")
        results = {
            "original_sentence": ORIGINAL_CLEAN,
            "final_outputs": final_outputs,
            "semantic_distances": distances,
            "text_similarities": text_similarities,
            "word_overlaps": word_overlaps,
            "embedding_method": "TF-IDF (local, no API)",
            "distance_metric": "cosine_distance",
            "api_provider": "NONE - All local computation"
        }

        # Ensure results directory exists
        results_dir = Path(__file__).parent.parent / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            results_file = results_dir / "analysis_results_local.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to: {results_file}")
            logger.info(f"Results saved to: {results_file}")
        except IOError as e:
            logger.error(f"Failed to save results: {e}")
            raise FileOperationError(
                "Cannot save analysis results",
                details={"error": str(e)}
            ) from e

        print("=" * 70)
        logger.info("Analysis complete!")
        print()

    except (AnalysisError, FileOperationError) as e:
        logger.error(f"Analysis failed: {e}")
        print(f"\n❌ Error: {e}")
        print("Please run the experiment first:")
        print("  python3 run_with_skills.py --all")
        raise

    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
        raise AnalysisError(
            "Analysis pipeline failed unexpectedly",
            details={"error": str(e)}
        ) from e


def generate_graph(
    distances: Dict[int, float],
    text_similarities: Dict[int, float],
    word_overlaps: Dict[int, float],
    output_dir: Path = None
) -> None:
    """
    Generate and save comprehensive visualizations of semantic drift analysis.

    Creates a 2x2 subplot figure showing:
    1. Cosine Distance vs. Noise Level
    2. Text Similarity vs. Noise Level
    3. Word Overlap vs. Noise Level
    4. Combined normalized metrics

    Args:
        distances: Dictionary mapping noise level to cosine distance
        text_similarities: Dictionary mapping noise level to text similarity
        word_overlaps: Dictionary mapping noise level to word overlap
        output_dir: Optional output directory path. If None, saves to results/ folder.

    Side Effects:
        - Saves semantic_drift_analysis_local.png (300 DPI)
        - Saves semantic_drift_analysis_local.pdf (vector format)

    Raises:
        AnalysisError: If graph generation fails

    Example:
        >>> distances = {0: 0.4, 25: 0.3, 50: 0.35}
        >>> text_sims = {0: 0.6, 25: 0.7, 50: 0.65}
        >>> word_overlaps = {0: 0.5, 25: 0.6, 50: 0.55}
        >>> generate_graph(distances, text_sims, word_overlaps)
        # Saves graphs to results/ directory
    """
    logger.info("Generating visualization graphs")

    try:
        # Extract data
        noise_levels = sorted(distances.keys())
        distance_values = [distances[n] for n in noise_levels]
        text_sim_values = [text_similarities[n] for n in noise_levels]
        word_overlap_values = [word_overlaps[n] for n in noise_levels]

        logger.debug(f"Generating graphs for {len(noise_levels)} noise levels")

        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(
            'Semantic Drift Analysis - Multi-Agent Translation Pipeline\n'
            'English → French → Hebrew → English (Local Analysis - No API)',
            fontsize=16, fontweight='bold'
        )
    
        # Plot 1: Cosine Distance
        ax1 = axes[0, 0]
        ax1.plot(noise_levels, distance_values, 
             marker='o', linewidth=2, markersize=10,
             color='#2E86AB', markerfacecolor='#A23B72',
             markeredgewidth=2, markeredgecolor='#2E86AB')
        ax1.set_xlabel('Spelling Error Rate (%)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Cosine Distance (TF-IDF)', fontsize=12, fontweight='bold')
        ax1.set_title('Semantic Distance (Lower = Better)', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_xlim(-5, 55)
        ax1.set_xticks(noise_levels)

        for noise, distance in zip(noise_levels, distance_values):
            ax1.annotate(f'{distance:.4f}', xy=(noise, distance), xytext=(0, 10),
                        textcoords='offset points', ha='center', fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

        # Plot 2: Text Similarity
        ax2 = axes[0, 1]
        ax2.plot(noise_levels, text_sim_values,
                 marker='s', linewidth=2, markersize=10,
                 color='#27AE60', markerfacecolor='#F39C12',
                 markeredgewidth=2, markeredgecolor='#27AE60')
        ax2.set_xlabel('Spelling Error Rate (%)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Text Similarity', fontsize=12, fontweight='bold')
        ax2.set_title('Character-Level Similarity (Higher = Better)', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.set_xlim(-5, 55)
        ax2.set_xticks(noise_levels)

        for noise, sim in zip(noise_levels, text_sim_values):
            ax2.annotate(f'{sim:.4f}', xy=(noise, sim), xytext=(0, 10),
                        textcoords='offset points', ha='center', fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.3))

        # Plot 3: Word Overlap
        ax3 = axes[1, 0]
        ax3.plot(noise_levels, word_overlap_values,
                 marker='^', linewidth=2, markersize=10,
                 color='#E74C3C', markerfacecolor='#9B59B6',
                 markeredgewidth=2, markeredgecolor='#E74C3C')
        ax3.set_xlabel('Spelling Error Rate (%)', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Word Overlap (Jaccard)', fontsize=12, fontweight='bold')
        ax3.set_title('Word Preservation (Higher = Better)', fontsize=13, fontweight='bold')
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.set_xlim(-5, 55)
        ax3.set_xticks(noise_levels)

        for noise, overlap in zip(noise_levels, word_overlap_values):
            ax3.annotate(f'{overlap:.4f}', xy=(noise, overlap), xytext=(0, 10),
                        textcoords='offset points', ha='center', fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.3))

        # Plot 4: Combined view (all metrics normalized)
        ax4 = axes[1, 1]

        # Normalize all metrics to 0-1 scale for comparison
        norm_distances = [1 - d for d in distance_values]  # Invert so higher = better

        ax4.plot(noise_levels, norm_distances, marker='o', linewidth=2, markersize=8,
                 label='Semantic (TF-IDF)', color='#2E86AB')
        ax4.plot(noise_levels, text_sim_values, marker='s', linewidth=2, markersize=8,
                 label='Text Similarity', color='#27AE60')
        ax4.plot(noise_levels, word_overlap_values, marker='^', linewidth=2, markersize=8,
                 label='Word Overlap', color='#E74C3C')

        ax4.set_xlabel('Spelling Error Rate (%)', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Normalized Score (Higher = Better)', fontsize=12, fontweight='bold')
        ax4.set_title('All Metrics Combined', fontsize=13, fontweight='bold')
        ax4.legend(loc='best', fontsize=10)
        ax4.grid(True, alpha=0.3, linestyle='--')
        ax4.set_xlim(-5, 55)
        ax4.set_xticks(noise_levels)

        plt.tight_layout()

        # Save figure to output directory (default: results/)
        if output_dir is None:
            results_dir = Path(__file__).parent.parent / "results"
        else:
            results_dir = Path(output_dir)
        results_dir.mkdir(parents=True, exist_ok=True)
        
        png_path = results_dir / "semantic_drift_analysis_local.png"
        plt.savefig(png_path, dpi=300, bbox_inches='tight')
        print(f"Graph saved to: {png_path}")
        logger.info("Saved PNG visualization")

        pdf_path = results_dir / "semantic_drift_analysis_local.pdf"
        plt.savefig(pdf_path, bbox_inches='tight')
        print(f"Graph saved to: {pdf_path}")
        logger.info("Saved PDF visualization")

        plt.close()
        logger.info("Graph generation complete")

    except Exception as e:
        logger.error(f"Failed to generate graphs: {e}", exc_info=True)
        raise AnalysisError(
            "Graph generation failed",
            details={"error": str(e)}
        ) from e


def print_summary_statistics(
    distances: Dict[int, float],
    text_sims: Dict[int, float],
    word_overlaps: Dict[int, float]
) -> None:
    """
    Print comprehensive summary statistics for all metrics.

    Calculates and displays mean, median, standard deviation, minimum,
    and maximum values for each of the three similarity metrics.

    Args:
        distances: Dictionary mapping noise level to cosine distance
        text_sims: Dictionary mapping noise level to text similarity
        word_overlaps: Dictionary mapping noise level to word overlap

    Side Effects:
        Prints formatted statistics to console

    Example:
        >>> distances = {0: 0.4, 25: 0.3, 50: 0.35}
        >>> text_sims = {0: 0.6, 25: 0.7, 50: 0.65}
        >>> word_overlaps = {0: 0.5, 25: 0.6, 50: 0.55}
        >>> print_summary_statistics(distances, text_sims, word_overlaps)
        # Prints formatted table of statistics
    """
    logger.info("Calculating summary statistics")

    if not distances:
        logger.warning("No distance data to summarize")
        return

    dist_values = list(distances.values())
    text_values = list(text_sims.values())
    word_values = list(word_overlaps.values())

    print("SUMMARY STATISTICS")
    print("=" * 70)

    print("\nCosine Distance (Lower = Better):")
    print(f"  Mean:      {np.mean(dist_values):.6f}")
    print(f"  Median:    {np.median(dist_values):.6f}")
    print(f"  Std Dev:   {np.std(dist_values):.6f}")
    print(f"  Min:       {np.min(dist_values):.6f} (at {min(distances, key=distances.get)}%)")
    print(f"  Max:       {np.max(dist_values):.6f} (at {max(distances, key=distances.get)}%)")

    print("\nText Similarity (Higher = Better):")
    print(f"  Mean:      {np.mean(text_values):.6f}")
    print(f"  Median:    {np.median(text_values):.6f}")
    print(f"  Std Dev:   {np.std(text_values):.6f}")
    print(f"  Min:       {np.min(text_values):.6f} (at {min(text_sims, key=text_sims.get)}%)")
    print(f"  Max:       {np.max(text_values):.6f} (at {max(text_sims, key=text_sims.get)}%)")

    print("\nWord Overlap (Higher = Better):")
    print(f"  Mean:      {np.mean(word_values):.6f}")
    print(f"  Median:    {np.median(word_values):.6f}")
    print(f"  Std Dev:   {np.std(word_values):.6f}")
    print(f"  Min:       {np.min(word_values):.6f} (at {min(word_overlaps, key=word_overlaps.get)}%)")
    print(f"  Max:       {np.max(word_values):.6f} (at {max(word_overlaps, key=word_overlaps.get)}%)")

    print("=" * 70)
    logger.info("Summary statistics complete")


def main():
    """Main entry point for semantic drift analysis."""
    # No API key needed!
    logger.info("Starting local semantic drift analysis")
    print("✓ No API calls required - all computation is local!")
    print()

    try:
        # Run analysis
        analyze_semantic_drift()
        logger.info("Analysis completed successfully")
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        exit(1)





if __name__ == "__main__":
    main()

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
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

# Original clean sentence
ORIGINAL_CLEAN = "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."

# Noise levels to analyze
NOISE_LEVELS = [0, 10, 20, 25, 30, 40, 50]


def get_local_embedding(texts: list) -> np.ndarray:
    """
    Get vector embeddings using TF-IDF (completely local, no API needed).
    
    Args:
        texts: List of texts to embed
        
    Returns:
        numpy array of embeddings
    """
    # Use TF-IDF to create embeddings
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 3),  # Use unigrams, bigrams, and trigrams
        lowercase=True,
        stop_words=None  # Keep all words for semantic preservation
    )
    
    embeddings = vectorizer.fit_transform(texts).toarray()
    return embeddings


def calculate_cosine_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine distance between two vectors.
    Cosine distance = 1 - cosine similarity
    
    Args:
        vec1: First embedding vector
        vec2: Second embedding vector
        
    Returns:
        Float representing the cosine distance (0 = identical, 2 = opposite)
    """
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    similarity = cosine_similarity(vec1, vec2)[0][0]
    distance = 1 - similarity
    return distance


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate character-level similarity using difflib.
    
    Returns:
        Float between 0 and 1 (1 = identical, 0 = completely different)
    """
    return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def calculate_word_overlap(text1: str, text2: str) -> float:
    """
    Calculate word overlap ratio (Jaccard similarity).
    
    Returns:
        Float between 0 and 1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0.0


def load_final_outputs() -> dict:
    """
    Load the final English outputs from each noise level experiment.
    
    Returns:
        Dictionary mapping noise level to final output text
    """
    outputs = {}
    
    for noise in NOISE_LEVELS:
        output_file = f"outputs/noise_{noise}/agent3_english.txt"
        
        if not os.path.exists(output_file):
            print(f"Warning: Output file not found for noise level {noise}%")
            print(f"Expected: {output_file}")
            continue
            
        with open(output_file, 'r', encoding='utf-8') as f:
            outputs[noise] = f.read().strip()
    
    return outputs


def analyze_semantic_drift():
    """
    Main analysis function:
    1. Load all final outputs
    2. Calculate local embeddings (TF-IDF)
    3. Compute cosine distances
    4. Calculate additional similarity metrics
    5. Generate visualization
    """
    print("=" * 70)
    print("SEMANTIC DRIFT ANALYSIS (Local - No API Calls Required!)")
    print("=" * 70)
    print()
    
    # Load outputs
    print("Loading final outputs from agent chain...")
    final_outputs = load_final_outputs()
    
    if not final_outputs:
        print("Error: No output files found!")
        print("Please run the agent chain first:")
        print("  ./run_full_experiment_gemini.sh  OR  ./run_full_experiment.sh")
        return
    
    print(f"Loaded {len(final_outputs)} outputs")
    print()
    
    # Prepare all texts for embedding
    print("Creating local embeddings using TF-IDF...")
    all_texts = [ORIGINAL_CLEAN] + [final_outputs[n] for n in sorted(final_outputs.keys())]
    embeddings = get_local_embedding(all_texts)
    
    original_embedding = embeddings[0]
    final_embeddings = {noise: embeddings[i+1] for i, noise in enumerate(sorted(final_outputs.keys()))}
    
    print(f"Embedding dimension: {len(original_embedding)}")
    print()
    
    # Calculate distances for each noise level
    print("Calculating semantic distances...")
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
    generate_graph(distances, text_similarities, word_overlaps)
    
    # Save results to JSON
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
    
    with open("analysis_results_local.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("Results saved to: analysis_results_local.json")
    print("=" * 70)
    print()


def generate_graph(distances: dict, text_similarities: dict, word_overlaps: dict):
    """
    Generate and save graphs showing semantic drift vs noise level.
    
    Args:
        distances: Dictionary mapping noise level to cosine distance
        text_similarities: Dictionary mapping noise level to text similarity
        word_overlaps: Dictionary mapping noise level to word overlap
    """
    # Extract data
    noise_levels = sorted(distances.keys())
    distance_values = [distances[n] for n in noise_levels]
    text_sim_values = [text_similarities[n] for n in noise_levels]
    word_overlap_values = [word_overlaps[n] for n in noise_levels]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Semantic Drift Analysis - Multi-Agent Translation Pipeline\nEnglish → French → Hebrew → English (Local Analysis - No API)',
                 fontsize=16, fontweight='bold')
    
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
    
    # Save figure
    plt.savefig('semantic_drift_analysis_local.png', dpi=300, bbox_inches='tight')
    print("Graph saved to: semantic_drift_analysis_local.png")
    
    plt.savefig('semantic_drift_analysis_local.pdf', bbox_inches='tight')
    print("Graph saved to: semantic_drift_analysis_local.pdf")
    
    plt.close()


def print_summary_statistics(distances: dict, text_sims: dict, word_overlaps: dict):
    """Print summary statistics of the experiment."""
    if not distances:
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


if __name__ == "__main__":
    # No API key needed!
    print("✓ No API calls required - all computation is local!")
    print()
    
    # Run analysis
    analyze_semantic_drift()


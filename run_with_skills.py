#!/usr/bin/env python3
"""
Agentic Turing Machine - Run with Claude Agent Skills
======================================================

This script runs the translation chain experiment using Claude's Agent Skills feature.
It demonstrates how to invoke specialized agent skills through the Anthropic API.

Usage:
    python3 run_with_skills.py --noise 25
    python3 run_with_skills.py --all  # Run all noise levels

Requirements:
    pip install anthropic
    export ANTHROPIC_API_KEY='your-key-here'
"""

import os
import sys
import argparse
from pathlib import Path
import anthropic

# Skills directory
SKILLS_DIR = Path(__file__).parent / "skills"

# Original clean sentence
ORIGINAL_CLEAN = "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."

# Noise levels mapping
NOISY_INPUTS = {
    0: "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data.",
    10: "The artifical intelligence systm can efficiently process natural language and understand complex semantic relationships within textual data.",
    20: "The artifical inteligence systm can efficiently proces natural language and understand complex semantic relationships within textual data.",
    25: "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data.",
    30: "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data.",
    40: "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships within textual data.",
    50: "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships withn textul data."
}


def load_skill(skill_name: str) -> dict:
    """Load a skill's SKILL.md content."""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill not found: {skill_path}")
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        "name": skill_name,
        "content": content
    }


def run_translation_with_skill(client: anthropic.Anthropic, skill_name: str, input_text: str, stage: int) -> str:
    """
    Run a single translation using a specific skill.
    
    Args:
        client: Anthropic API client
        skill_name: Name of the skill to use
        input_text: Text to translate
        stage: Stage number (1, 2, or 3)
        
    Returns:
        Translated text
    """
    skill = load_skill(skill_name)
    
    # Construct the prompt
    prompt = f"""You are using the "{skill_name}" skill.

{skill['content']}

---

Please translate the following text according to the skill instructions above.
Return ONLY the translation, with no explanations or additional text.

Input text:
{input_text}"""

    print(f"  Stage {stage}: Invoking {skill_name}...")
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0,  # Deterministic for consistency
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract the text content
        output = response.content[0].text.strip()
        print(f"  ✓ Stage {stage} complete: {len(output)} characters")
        return output
        
    except Exception as e:
        print(f"  ✗ Error in stage {stage}: {e}")
        raise


def run_translation_chain(noise_level: int):
    """
    Run the complete translation chain for a given noise level.
    
    Args:
        noise_level: Percentage of noise (0, 10, 20, 25, 30, 40, or 50)
    """
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Get noisy input
    if noise_level not in NOISY_INPUTS:
        print(f"Error: Invalid noise level {noise_level}. Must be one of: {list(NOISY_INPUTS.keys())}")
        sys.exit(1)
    
    input_text = NOISY_INPUTS[noise_level]
    
    print("=" * 70)
    print(f"RUNNING TRANSLATION CHAIN - Noise Level: {noise_level}%")
    print("=" * 70)
    print(f"Input: {input_text[:60]}...")
    print()
    
    # Create output directory
    output_dir = Path(f"outputs/noise_{noise_level}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Stage 1: English → French
    french_output = run_translation_with_skill(
        client,
        "english-to-french-translator",
        input_text,
        stage=1
    )
    
    # Save French output
    with open(output_dir / "agent1_french.txt", 'w', encoding='utf-8') as f:
        f.write(french_output + "\n")
    
    print(f"  Saved: {output_dir}/agent1_french.txt")
    print()
    
    # Stage 2: French → Hebrew
    hebrew_output = run_translation_with_skill(
        client,
        "french-to-hebrew-translator",
        french_output,
        stage=2
    )
    
    # Save Hebrew output
    with open(output_dir / "agent2_hebrew.txt", 'w', encoding='utf-8') as f:
        f.write(hebrew_output + "\n")
    
    print(f"  Saved: {output_dir}/agent2_hebrew.txt")
    print()
    
    # Stage 3: Hebrew → English
    english_output = run_translation_with_skill(
        client,
        "hebrew-to-english-translator",
        hebrew_output,
        stage=3
    )
    
    # Save English output
    with open(output_dir / "agent3_english.txt", 'w', encoding='utf-8') as f:
        f.write(english_output + "\n")
    
    print(f"  Saved: {output_dir}/agent3_english.txt")
    print()
    
    # Summary
    print("-" * 70)
    print("TRANSLATION CHAIN COMPLETE")
    print("-" * 70)
    print(f"Original: {ORIGINAL_CLEAN}")
    print(f"Final:    {english_output}")
    print()
    print(f"All outputs saved to: {output_dir}")
    print("=" * 70)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Run translation chain experiment using Claude Agent Skills"
    )
    parser.add_argument(
        "--noise",
        type=int,
        choices=[0, 10, 20, 25, 30, 40, 50],
        help="Noise level percentage (0, 10, 20, 25, 30, 40, or 50)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all noise levels"
    )
    
    args = parser.parse_args()
    
    if not args.noise and not args.all:
        parser.print_help()
        print("\nError: Specify --noise LEVEL or --all")
        sys.exit(1)
    
    # Check if skills exist
    if not SKILLS_DIR.exists():
        print(f"Error: Skills directory not found: {SKILLS_DIR}")
        print("Please ensure the skills/ directory exists with SKILL.md files")
        sys.exit(1)
    
    # Run experiment
    if args.all:
        print("Running full experiment with all noise levels...")
        print()
        for noise_level in [0, 10, 20, 25, 30, 40, 50]:
            try:
                run_translation_chain(noise_level)
            except Exception as e:
                print(f"Error at noise level {noise_level}: {e}")
                continue
    else:
        run_translation_chain(args.noise)
    
    print()
    print("✓ Experiment complete!")
    print("Run analysis: .venv/bin/python3 analyze_results_local.py")


if __name__ == "__main__":
    main()


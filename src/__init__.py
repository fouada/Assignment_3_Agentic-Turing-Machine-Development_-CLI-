"""
Agentic Turing Machine - Core Package
======================================

A multi-agent translation pipeline demonstrating LLM attention mechanism
robustness using Claude Agent Skills.

Modules:
    pipeline: Main translation pipeline execution
    analysis: Results analysis and visualization
    agent_tester: CLI tool for testing individual agents
"""

__version__ = "1.0.0"
__author__ = "Agentic Turing Machine Team"

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
CONFIG_DIR = PROJECT_ROOT / "config"

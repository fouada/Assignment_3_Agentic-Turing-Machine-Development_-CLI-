#!/usr/bin/env python3
"""
Backward compatibility wrapper for run_with_skills.py

This script maintains backward compatibility with existing documentation
and scripts by forwarding to the new modular structure in src/pipeline.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the main function from the refactored module
from pipeline import main

if __name__ == "__main__":
    main()

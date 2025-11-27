#!/usr/bin/env python3
"""
Backward compatibility wrapper for analyze_results_local.py

This script maintains backward compatibility with existing documentation
and scripts by forwarding to the new modular structure in src/analysis.py
"""

import sys
from pathlib import Path

# Add src to path (go up to project root, then into src)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import and run the main function from the refactored module
from analysis import main

if __name__ == "__main__":
    main()

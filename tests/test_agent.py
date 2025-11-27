#!/usr/bin/env python3
"""
Backward compatibility wrapper for test_agent.py

This script maintains backward compatibility with existing documentation
and scripts by forwarding to the new modular structure in src/agent_tester.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the main function from the refactored module
from agent_tester import main

if __name__ == "__main__":
    main()

# 🚀 UV Setup Guide

## What is UV?

UV is an extremely fast Python package installer and resolver, written in Rust. It's 10-100x faster than pip and provides better dependency resolution.

## Installation

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Via Homebrew (macOS)
```bash
brew install uv
```

### Via pip (if you already have Python)
```bash
pip install uv
```

## Project Setup

### 1. Create Virtual Environment
```bash
# UV will automatically create a virtual environment
uv venv
```

This creates a `.venv` directory in your project.

### 2. Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

**Install from pyproject.toml:**
```bash
uv pip install -e .
```

**Or install from requirements.txt (legacy):**
```bash
uv pip install -r requirements.txt
```

**Install dev dependencies:**
```bash
uv pip install -e ".[dev]"
```

### 4. Sync Dependencies (Recommended)
```bash
uv pip sync
```

## Quick Start Commands

### Installing Packages
```bash
# Install a single package
uv pip install openai

# Install multiple packages
uv pip install numpy matplotlib scikit-learn

# Install specific version
uv pip install "openai>=1.0.0"
```

### Managing Dependencies
```bash
# List installed packages
uv pip list

# Freeze dependencies
uv pip freeze > requirements.txt

# Compile dependencies (create lock file)
uv pip compile pyproject.toml -o requirements.lock
```

### Running Scripts
```bash
# Run Python script in the UV environment
uv run python analyze_results.py

# Or with activated venv
python analyze_results.py
```

## Advantages of UV

✅ **Speed**: 10-100x faster than pip  
✅ **Better Dependency Resolution**: Handles complex dependency trees  
✅ **Disk Space**: Efficient caching and smaller footprint  
✅ **Drop-in Replacement**: Compatible with pip commands  
✅ **Modern**: Built with Rust for performance  

## Common Workflows

### Starting Fresh
```bash
# Remove old virtual environment (if exists)
rm -rf .venv

# Create new environment with UV
uv venv

# Activate it
source .venv/bin/activate

# Install dependencies
uv pip install -e .

# Verify installation
python -c "import openai; print('✓ Dependencies installed!')"
```

### Adding New Dependencies
```bash
# Install and add to pyproject.toml manually, or:
uv pip install <package-name>

# Then update pyproject.toml manually
# This ensures your dependencies are tracked
```

### Running the Project
```bash
# With UV (no activation needed)
uv run python analyze_results.py

# Or activate venv first
source .venv/bin/activate
python analyze_results.py
./run_full_experiment.sh
```

## Migration from pip

If you're coming from pip, here's the mapping:

| pip Command | UV Equivalent |
|-------------|---------------|
| `pip install package` | `uv pip install package` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip freeze` | `uv pip freeze` |
| `pip list` | `uv pip list` |
| `pip uninstall package` | `uv pip uninstall package` |
| `python -m venv .venv` | `uv venv` |

## Troubleshooting

### UV Command Not Found
```bash
# Add UV to PATH (usually done automatically)
export PATH="$HOME/.cargo/bin:$PATH"

# Or reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Virtual Environment Not Activating
```bash
# Make sure you're in the project directory
cd /path/to/project

# Create venv if it doesn't exist
uv venv

# Activate
source .venv/bin/activate
```

### Dependencies Not Installing
```bash
# Clear UV cache
uv cache clean

# Try installing again
uv pip install -e .
```

## Resources

- **Official Website**: https://astral.sh/uv
- **GitHub**: https://github.com/astral-sh/uv
- **Documentation**: https://github.com/astral-sh/uv/blob/main/README.md

## Integration with This Project

Once UV is set up, you can run the full workflow:

```bash
# Setup (one time)
uv venv
source .venv/bin/activate
uv pip install -e .

# Set your OpenAI API key
export OPENAI_API_KEY='sk-your-key-here'

# Run the experiment
./run_full_experiment.sh

# Analyze results
python analyze_results.py
```

---

**Note**: UV is a drop-in replacement for pip. All your existing scripts and workflows will continue to work!


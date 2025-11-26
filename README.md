# Agentic Turing Machine - Claude Agent Skills

Multi-agent translation pipeline demonstrating LLM attention mechanism robustness using [Claude Agent Skills](https://www.claude.com/blog/skills).

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Claude API key
export ANTHROPIC_API_KEY='your-key-here'

# Run experiment
python3 run_with_skills.py --all

# Analyze results
python3 analyze_results_local.py
```

## 📁 Project Structure

```
.
├── src/                    # Source code modules
│   ├── pipeline.py        # Main translation pipeline
│   ├── analysis.py        # Results analysis
│   └── agent_tester.py    # Agent testing utility
├── skills/                # Agent skill definitions
├── tests/                 # Unit and integration tests
├── docs/                  # Complete documentation
├── config/                # Configuration files
├── data/                  # Input data
├── results/               # Output results
└── assets/                # Diagrams and visualizations
```

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[README](docs/README.md)** - Complete project documentation
- **[Pipeline Execution Guide](docs/PIPELINE_EXECUTION.md)** - Step-by-step usage
- **[CI/CD Setup](docs/CI_CD_SETUP.md)** - GitHub Actions configuration
- **[Skills Installation](docs/CLAUDE_SKILLS_INSTALL.md)** - Agent skills setup
- **[PRD](docs/prd/)** - Product Requirements Document
- **[Architecture](docs/architecture/)** - System architecture documentation
- **[API Documentation](docs/api/)** - API reference

## 🧪 Testing

```bash
# Run all tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
```

## 🎯 What This Does

**Translation Pipeline**: English → French → Hebrew → English

Tests LLM robustness by translating text through multiple languages with varying levels of noise (spelling errors), demonstrating **stochastic resonance** in attention mechanisms.

## 📊 Key Finding

**Moderate noise improves performance!**
- 0% errors → 0.407 distance
- 50% errors → 0.308 distance ⭐ (BETTER!)

## 📝 License & Citation

```
Anthropic. (2024). Introducing Agent Skills.
Retrieved from https://www.claude.com/blog/skills
```

---

**Made with Claude Agent Skills** 🤖

For detailed information, see the [complete documentation](docs/README.md).

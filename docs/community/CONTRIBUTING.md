# Contributing to Agentic Turing Machine

Thank you for your interest in contributing to the Agentic Turing Machine! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- [UV](https://docs.astral.sh/uv/) (recommended) or pip
- Claude API key (for running experiments)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-.git
cd Assignment_3_Agentic-Turing-Machine-Development_-CLI-

# Install with UV (recommended - 18x faster)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"

# Or with pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests to verify setup
pytest tests/ -v
```

---

## How to Contribute

### Types of Contributions

We welcome many types of contributions:

| Type | Description | How to Start |
|------|-------------|--------------|
| 🐛 **Bug Reports** | Found a bug? Let us know! | [Open an issue](../../issues/new?template=bug_report.md) |
| ✨ **Feature Requests** | Have an idea? We'd love to hear it! | [Open an issue](../../issues/new?template=feature_request.md) |
| 📝 **Documentation** | Improve docs, fix typos, add examples | Fork and submit PR |
| 🔧 **Code** | Fix bugs, add features, improve performance | Fork and submit PR |
| 🧪 **Tests** | Add test coverage, improve test quality | Fork and submit PR |
| 🌍 **Translations** | Add new languages to the translation chain | See [Adding Languages](#adding-new-languages) |
| 📊 **Research** | Add new analysis methods or metrics | See [Research Contributions](#research-contributions) |

### First-Time Contributors

New to open source? Here's how to make your first contribution:

1. **Find a good first issue**: Look for issues labeled [`good first issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
2. **Fork the repository**: Click "Fork" at the top right
3. **Clone your fork**: `git clone https://github.com/YOUR-USERNAME/repo-name.git`
4. **Create a branch**: `git checkout -b my-feature`
5. **Make changes**: Edit files, add tests
6. **Push changes**: `git push origin my-feature`
7. **Open a PR**: Go to GitHub and click "New Pull Request"

---

## Development Setup

### Project Structure

```
├── src/                    # Source code
│   ├── pipeline.py         # Main translation pipeline
│   ├── analysis.py         # Semantic analysis
│   ├── information_theory.py   # Information-theoretic metrics
│   ├── stochastic_resonance.py # SR detection
│   ├── self_healing_agent.py   # Self-healing translation
│   └── adversarial_robustness.py # Adversarial testing
├── skills/                 # Claude Agent Skills
│   └── */SKILL.md          # Individual skill definitions
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test fixtures
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

### Running the Project

```bash
# Run a single experiment
python scripts/experiment/run_with_skills.py --noise 25

# Run all noise levels
python scripts/experiment/run_with_skills.py --all

# Analyze results (no API needed)
python scripts/experiment/analyze_results.py

# Run the innovation modules
python scripts/experiment/run_mit_innovations.py
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://peps.python.org/pep-0008/) with these additions:

```python
# ✅ Good: Type hints on all public functions
def calculate_entropy(text: str, level: str = "word") -> EntropyResult:
    """Calculate Shannon entropy of text.
    
    Args:
        text: Input text to analyze
        level: Granularity level ("char" or "word")
    
    Returns:
        EntropyResult with entropy metrics
    
    Raises:
        ValueError: If level is not "char" or "word"
    """
    if level not in ("char", "word"):
        raise ValueError(f"Invalid level: {level}")
    ...

# ✅ Good: Dataclasses for structured returns
@dataclass
class EntropyResult:
    """Result of entropy calculation."""
    shannon_entropy: float
    normalized_entropy: float
    vocabulary_size: int
```

### Code Quality Tools

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Type check with mypy
mypy src/

# Lint with ruff
ruff check src/
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new translation language support
fix: resolve entropy calculation edge case
docs: update API documentation
test: add tests for self-healing module
refactor: simplify pipeline configuration
perf: optimize TF-IDF vectorization
```

---

## Testing Guidelines

### Test Coverage Requirements

| Component | Minimum Coverage | Target Coverage |
|-----------|-----------------|-----------------|
| Core modules (`src/`) | 85% | 90%+ |
| Innovation modules | 85% | 90%+ |
| Overall project | 85% | 87%+ |

### Writing Tests

```python
# tests/unit/test_example.py
import pytest
from src.information_theory import InformationTheoreticAnalyzer

class TestEntropyCalculation:
    """Tests for entropy calculation."""
    
    def test_entropy_positive_for_non_empty_text(self):
        """Entropy should be positive for non-empty text."""
        analyzer = InformationTheoreticAnalyzer(data_path="tests/fixtures")
        result = analyzer.calculate_entropy("hello world")
        assert result.shannon_entropy > 0
    
    def test_entropy_zero_for_single_char(self):
        """Entropy should be zero for single repeated character."""
        analyzer = InformationTheoreticAnalyzer(data_path="tests/fixtures")
        result = analyzer.calculate_entropy("aaaa")
        assert result.shannon_entropy == 0
    
    @pytest.mark.parametrize("level", ["char", "word"])
    def test_entropy_levels(self, level):
        """Both char and word levels should work."""
        analyzer = InformationTheoreticAnalyzer(data_path="tests/fixtures")
        result = analyzer.calculate_entropy("hello world", level=level)
        assert result.normalized_entropy >= 0
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_analysis.py -v

# Run tests matching pattern
pytest tests/ -k "entropy" -v

# Run with coverage threshold (fails if < 85%)
pytest --cov=src --cov-fail-under=85
```

---

## Documentation Standards

### Docstring Format

We use Google-style docstrings:

```python
def translate_with_healing(
    source_text: str,
    target_language: str,
    max_iterations: int = 3
) -> HealingReport:
    """Translate text with self-healing capabilities.
    
    Performs translation and automatically detects and corrects
    errors using confidence-based self-healing.
    
    Args:
        source_text: The text to translate
        target_language: Target language code (e.g., "fr", "he")
        max_iterations: Maximum healing iterations (default: 3)
    
    Returns:
        HealingReport containing:
            - initial_translation: First attempt
            - final_translation: After healing
            - confidence_improvement: Delta in confidence
            - corrections_applied: List of corrections
    
    Raises:
        TranslationError: If translation fails after max iterations
        ValueError: If target_language is not supported
    
    Example:
        >>> healer = SelfHealingTranslator()
        >>> report = healer.translate_with_healing("Hello", "fr")
        >>> print(report.final_translation)
        "Bonjour"
    """
```

### README in Each Directory

Every major directory should have a README:

```markdown
# Directory Name

Brief description of what this directory contains.

## Contents

- `file1.py` - Description of file1
- `file2.py` - Description of file2

## Usage

```python
from this_directory import something
```

## See Also

- [Related Document](../docs/related.md)
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation**: If you changed functionality, update docs
2. **Add tests**: All new code should have tests
3. **Run the test suite**: `pytest tests/ --cov=src`
4. **Check coverage**: Ensure coverage doesn't drop below 85%
5. **Format code**: `black src/ tests/ && isort src/ tests/`

### PR Checklist

Use this checklist in your PR description:

```markdown
## Checklist

- [ ] I have read the [CONTRIBUTING](CONTRIBUTING.md) guide
- [ ] My code follows the project's coding standards
- [ ] I have added tests covering my changes
- [ ] All tests pass locally (`pytest tests/ -v`)
- [ ] Coverage is maintained (≥85%)
- [ ] I have updated documentation as needed
- [ ] My commits follow Conventional Commits format
```

### Review Process

1. **Automated checks**: CI runs tests, linting, coverage
2. **Code review**: A maintainer will review your code
3. **Feedback**: Address any comments or suggestions
4. **Merge**: Once approved, a maintainer will merge

---

## Adding New Languages

Want to add a new translation language? Here's how:

### 1. Create the Skill

Create a new directory under `skills/`:

```
skills/
└── english-to-spanish-translator/
    └── SKILL.md
```

### 2. Write the SKILL.md

Use this template:

```markdown
# English to Spanish Translator

## Description
Translates English text to Spanish with high accuracy.

## Instructions
1. Translate the given English text to Spanish
2. Preserve the original meaning and tone
3. Handle spelling errors gracefully
4. Return ONLY the Spanish translation

## Examples

### Input
The artificial intelligence system processes data efficiently.

### Output
El sistema de inteligencia artificial procesa datos de manera eficiente.

## Notes
- Handle noisy input with spelling errors
- Preserve technical terminology where appropriate
- Maintain sentence structure when possible
```

### 3. Update Pipeline

Add your language to `src/pipeline.py`:

```python
SUPPORTED_LANGUAGES = {
    "en": "english",
    "fr": "french",
    "he": "hebrew",
    "es": "spanish",  # Add your language
}
```

### 4. Add Tests

Create tests in `tests/unit/test_your_language.py`.

---

## Research Contributions

### Adding New Analysis Methods

1. Create a new module in `src/`
2. Follow the pattern of existing modules (dataclasses, type hints, docstrings)
3. Add tests with 85%+ coverage
4. Document in `docs/`

### Academic Contributions

If using this project for research:

1. **Cite the project** (see LICENSE for citation format)
2. **Share your findings** - Open an issue or PR with your results
3. **Contribute improvements** - If you improved the methodology, share it!

---

## Community

### Getting Help

- **Issues**: [GitHub Issues](../../issues) for bugs and features
- **Discussions**: [GitHub Discussions](../../discussions) for questions
- **Email**: Contact maintainers (see README)

### Recognition

Contributors are recognized in:
- The [CONTRIBUTORS.md](./CONTRIBUTORS.md) file
- Release notes for significant contributions
- Academic acknowledgments for research contributions

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](../../LICENSE).

---

**Thank you for contributing to the Agentic Turing Machine! 🤖✨**


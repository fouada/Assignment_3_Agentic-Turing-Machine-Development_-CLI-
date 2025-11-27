# Reusable Templates & Patterns

This document provides reusable templates from the Agentic Turing Machine project that you can adapt for your own projects.

## Table of Contents

1. [Claude Agent Skill Template](#claude-agent-skill-template)
2. [Analysis Module Template](#analysis-module-template)
3. [Test Module Template](#test-module-template)
4. [Documentation Templates](#documentation-templates)
5. [CI/CD Workflow Templates](#cicd-workflow-templates)
6. [ADR Template](#adr-template)
7. [Research Paper Structure](#research-paper-structure)

---

## Claude Agent Skill Template

Use this template to create new Claude Agent Skills:

### `skills/your-skill-name/SKILL.md`

```markdown
# Skill Name

## Description

One-sentence description of what this skill does.

## Detailed Purpose

A paragraph explaining the skill's role in the larger system.

## Instructions

You are a specialized agent that [description of role].

### Core Responsibilities

1. [Primary responsibility]
2. [Secondary responsibility]
3. [Tertiary responsibility]

### Input Format

You will receive input in the following format:
- [Description of expected input]

### Output Format

You must respond with ONLY:
- [Description of expected output]
- No additional commentary or explanation

### Edge Cases

Handle these situations:
- **Empty input**: [How to handle]
- **Malformed input**: [How to handle]
- **Edge case 3**: [How to handle]

## Examples

### Example 1: Basic Usage

**Input:**
[Example input]

**Output:**
[Example output]

### Example 2: Edge Case

**Input:**
[Edge case input]

**Output:**
[Edge case output]

## Quality Criteria

Your output will be evaluated on:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Notes

- [Important note 1]
- [Important note 2]
```

---

## Analysis Module Template

Use this template for new analysis modules in `src/`:

### `src/your_analysis.py`

```python
"""
Your Analysis Module

Brief description of what this module analyzes.

Example:
    >>> from src.your_analysis import YourAnalyzer
    >>> analyzer = YourAnalyzer(data_path="results")
    >>> result = analyzer.analyze()
    >>> print(result.summary)

Author: Your Name
Date: YYYY-MM-DD
"""

from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import logging

from src.errors import AnalysisError

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Result of analysis operation.
    
    Attributes:
        metric_1: Description of metric 1
        metric_2: Description of metric 2
        summary: Human-readable summary
        metadata: Additional metadata
    """
    metric_1: float
    metric_2: float
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return asdict(self)


class YourAnalyzer:
    """Analyzer for [type of analysis].
    
    This class provides methods for analyzing [what you're analyzing]
    using [methodology].
    
    Attributes:
        data_path: Path to data directory
        config: Configuration options
    
    Example:
        >>> analyzer = YourAnalyzer("results")
        >>> result = analyzer.analyze()
    """
    
    def __init__(
        self,
        data_path: str = "results",
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize the analyzer.
        
        Args:
            data_path: Path to the data directory
            config: Optional configuration dictionary
            
        Raises:
            AnalysisError: If data path doesn't exist
        """
        self.data_path = Path(data_path)
        self.config = config or {}
        
        if not self.data_path.exists():
            raise AnalysisError(f"Data path not found: {data_path}")
        
        self._load_data()
    
    def _load_data(self) -> None:
        """Load required data files."""
        try:
            # Load your data here
            pass
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise AnalysisError(f"Failed to load data: {e}")
    
    def analyze(self) -> AnalysisResult:
        """Perform the main analysis.
        
        Returns:
            AnalysisResult with computed metrics
            
        Raises:
            AnalysisError: If analysis fails
        """
        logger.info("Starting analysis...")
        
        try:
            # Compute your metrics here
            metric_1 = self._compute_metric_1()
            metric_2 = self._compute_metric_2()
            
            result = AnalysisResult(
                metric_1=metric_1,
                metric_2=metric_2,
                summary=f"Analysis complete: m1={metric_1:.3f}, m2={metric_2:.3f}",
                metadata={"analyzer": "YourAnalyzer", "version": "1.0"}
            )
            
            logger.info(f"Analysis complete: {result.summary}")
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise AnalysisError(f"Analysis failed: {e}")
    
    def _compute_metric_1(self) -> float:
        """Compute metric 1.
        
        Returns:
            The computed metric value
        """
        # Your computation here
        return 0.0
    
    def _compute_metric_2(self) -> float:
        """Compute metric 2.
        
        Returns:
            The computed metric value
        """
        # Your computation here
        return 0.0
    
    def save_results(
        self,
        result: AnalysisResult,
        output_path: Optional[str] = None
    ) -> str:
        """Save analysis results to JSON.
        
        Args:
            result: The analysis result to save
            output_path: Optional custom output path
            
        Returns:
            Path to the saved file
        """
        if output_path is None:
            output_path = self.data_path / "your_analysis.json"
        else:
            output_path = Path(output_path)
        
        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        
        logger.info(f"Results saved to {output_path}")
        return str(output_path)


def main() -> None:
    """Command-line entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run analysis")
    parser.add_argument("--data-path", default="results", help="Path to data")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()
    
    analyzer = YourAnalyzer(data_path=args.data_path)
    result = analyzer.analyze()
    
    if args.output:
        analyzer.save_results(result, args.output)
    else:
        print(result.summary)


if __name__ == "__main__":
    main()
```

---

## Test Module Template

Use this template for new test modules:

### `tests/unit/test_your_module.py`

```python
"""
Unit tests for your_module.

Tests cover:
- Basic functionality
- Edge cases
- Error handling
- Integration scenarios
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.your_analysis import YourAnalyzer, AnalysisResult
from src.errors import AnalysisError


class TestAnalysisResult:
    """Tests for AnalysisResult dataclass."""
    
    def test_creation_with_required_fields(self):
        """Result should be created with required fields."""
        result = AnalysisResult(
            metric_1=0.5,
            metric_2=0.8,
            summary="Test summary"
        )
        assert result.metric_1 == 0.5
        assert result.metric_2 == 0.8
        assert result.summary == "Test summary"
    
    def test_to_dict_returns_dictionary(self):
        """to_dict should return a dictionary."""
        result = AnalysisResult(
            metric_1=0.5,
            metric_2=0.8,
            summary="Test"
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["metric_1"] == 0.5


class TestYourAnalyzer:
    """Tests for YourAnalyzer class."""
    
    @pytest.fixture
    def mock_data_path(self, tmp_path):
        """Create a temporary data directory."""
        data_dir = tmp_path / "results"
        data_dir.mkdir()
        return data_dir
    
    @pytest.fixture
    def analyzer(self, mock_data_path):
        """Create an analyzer instance."""
        return YourAnalyzer(data_path=str(mock_data_path))
    
    def test_init_with_valid_path(self, mock_data_path):
        """Analyzer should initialize with valid path."""
        analyzer = YourAnalyzer(data_path=str(mock_data_path))
        assert analyzer.data_path == mock_data_path
    
    def test_init_with_invalid_path_raises_error(self):
        """Analyzer should raise AnalysisError for invalid path."""
        with pytest.raises(AnalysisError) as exc_info:
            YourAnalyzer(data_path="/nonexistent/path")
        assert "not found" in str(exc_info.value).lower()
    
    def test_analyze_returns_result(self, analyzer):
        """analyze() should return AnalysisResult."""
        result = analyzer.analyze()
        assert isinstance(result, AnalysisResult)
    
    def test_analyze_computes_metrics(self, analyzer):
        """analyze() should compute valid metrics."""
        result = analyzer.analyze()
        assert isinstance(result.metric_1, float)
        assert isinstance(result.metric_2, float)
    
    @pytest.mark.parametrize("config_value", [None, {}, {"key": "value"}])
    def test_init_with_various_configs(self, mock_data_path, config_value):
        """Analyzer should accept various config values."""
        analyzer = YourAnalyzer(
            data_path=str(mock_data_path),
            config=config_value
        )
        assert analyzer.config == (config_value or {})
    
    def test_save_results_creates_file(self, analyzer, tmp_path):
        """save_results should create output file."""
        result = AnalysisResult(
            metric_1=0.5,
            metric_2=0.8,
            summary="Test"
        )
        output_path = tmp_path / "output.json"
        analyzer.save_results(result, str(output_path))
        assert output_path.exists()


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_data_handling(self):
        """Should handle empty data gracefully."""
        # Test your edge case
        pass
    
    def test_malformed_data_handling(self):
        """Should handle malformed data gracefully."""
        # Test your edge case
        pass


class TestIntegration:
    """Integration tests."""
    
    @pytest.mark.integration
    def test_full_analysis_pipeline(self, tmp_path):
        """Full pipeline should work end-to-end."""
        # Setup
        data_dir = tmp_path / "results"
        data_dir.mkdir()
        
        # Execute
        analyzer = YourAnalyzer(data_path=str(data_dir))
        result = analyzer.analyze()
        output = analyzer.save_results(result)
        
        # Verify
        assert Path(output).exists()
        assert result.metric_1 is not None
```

---

## Documentation Templates

### README Template for Subdirectories

```markdown
# Directory Name

Brief description of this directory's contents and purpose.

## Contents

| File/Directory | Description |
|----------------|-------------|
| `file1.py` | Description |
| `subdir/` | Description |

## Quick Start

\`\`\`bash
# How to use the contents of this directory
\`\`\`

## Dependencies

- Dependency 1
- Dependency 2

## Related Documentation

- [Related Doc 1](../docs/related1.md)
- [Related Doc 2](../docs/related2.md)

## Maintainers

- @maintainer1
- @maintainer2
```

### API Documentation Template

```markdown
# Module Name API

## Overview

Brief description of the module's purpose.

## Installation

\`\`\`bash
pip install package-name
\`\`\`

## Classes

### `ClassName`

Description of the class.

**Constructor:**

\`\`\`python
ClassName(param1: type, param2: type = default)
\`\`\`

**Parameters:**
- `param1` (type): Description
- `param2` (type, optional): Description. Defaults to `default`.

**Methods:**

#### `method_name(args) -> ReturnType`

Description of what the method does.

**Example:**

\`\`\`python
instance = ClassName(param1)
result = instance.method_name(args)
\`\`\`

## Functions

### `function_name(args) -> ReturnType`

Description of the function.

## Exceptions

### `CustomError`

Raised when [condition].

## Examples

### Basic Usage

\`\`\`python
# Complete working example
\`\`\`

### Advanced Usage

\`\`\`python
# More complex example
\`\`\`
```

---

## CI/CD Workflow Templates

### Basic Test Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Install dependencies
        run: |
          uv venv
          source .venv/bin/activate
          uv pip install -e ".[dev]"
      
      - name: Run tests with coverage
        run: |
          source .venv/bin/activate
          pytest tests/ --cov=src --cov-report=xml --cov-fail-under=85
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: coverage.xml
```

---

## ADR Template

### Architecture Decision Record

```markdown
# ADR-XXX: Title

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Context

What is the issue that we're seeing that is motivating this decision?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

### Positive

- Consequence 1
- Consequence 2

### Negative

- Consequence 1
- Consequence 2

### Neutral

- Consequence 1

## Alternatives Considered

### Alternative 1

Description. Why rejected?

### Alternative 2

Description. Why rejected?

## References

- [Reference 1](url)
- [Reference 2](url)

## Revision History

| Date | Author | Description |
|------|--------|-------------|
| YYYY-MM-DD | Name | Initial proposal |
```

---

## Research Paper Structure

### Academic Paper Template

```markdown
# Title: Descriptive Title of Research

## Abstract

~250 words summarizing:
- Problem statement
- Methodology
- Key findings
- Implications

## 1. Introduction

### 1.1 Motivation
### 1.2 Problem Statement
### 1.3 Research Questions
### 1.4 Contributions
### 1.5 Paper Organization

## 2. Background

### 2.1 Related Work
### 2.2 Theoretical Framework
### 2.3 Definitions

## 3. Methodology

### 3.1 Research Design
### 3.2 Data Collection
### 3.3 Analysis Methods
### 3.4 Validity & Limitations

## 4. Implementation

### 4.1 System Architecture
### 4.2 Technical Details
### 4.3 Reproducibility

## 5. Results

### 5.1 Experimental Setup
### 5.2 Quantitative Results
### 5.3 Qualitative Analysis
### 5.4 Statistical Significance

## 6. Discussion

### 6.1 Interpretation of Results
### 6.2 Implications
### 6.3 Limitations
### 6.4 Future Work

## 7. Conclusion

## References

## Appendices
```

---

## How to Use These Templates

1. **Copy the template** you need
2. **Modify placeholders** (marked with `[brackets]` or `your_name`)
3. **Add your specific content**
4. **Review for consistency** with existing project style
5. **Test thoroughly** before committing

## Contributing New Templates

If you create a useful template, please contribute it back:

1. Add the template to this document
2. Include a clear description
3. Provide at least one usage example
4. Submit a PR with the `documentation` label

---

*Last Updated: November 2025*


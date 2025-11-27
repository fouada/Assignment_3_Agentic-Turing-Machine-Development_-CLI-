# 🚀 Testing Quick Reference Guide

**Last Updated:** November 27, 2025

---

## ⚡ Quick Commands

### Run All Tests
```bash
pytest tests/ --cov=src -v
```

### Run With Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Run Specific Test Types
```bash
# Unit tests only
pytest tests/unit/ -v

# Performance tests only
pytest tests/unit/test_performance.py -v

# Specific module
pytest tests/unit/test_analysis.py -v

# Specific test
pytest tests/unit/test_analysis.py::TestGetLocalEmbedding::test_embedding_basic -v
```

### Check Coverage Threshold
```bash
pytest tests/ --cov=src --cov-fail-under=85
```

---

## 📊 Current Test Status

| Metric | Value | Status |
|--------|-------|--------|
| **Total Tests** | 103 | ✅ |
| **Pass Rate** | 100% | ✅ |
| **Coverage** | 86.33% | ✅ (>85%) |
| **Execution Time** | 6.82s | ✅ (<10s) |
| **Performance Tests** | 20 | ✅ |
| **Functional Tests** | 83 | ✅ |

---

## 🧪 Test Categories

### 1. **Unit Tests** (83 tests)
Tests individual functions in isolation.

```bash
# Run all unit tests
pytest tests/unit/ -v

# By module
pytest tests/unit/test_agent_tester.py -v    # 15 tests
pytest tests/unit/test_analysis.py -v        # 42 tests
pytest tests/unit/test_config.py -v          # 20 tests
pytest tests/unit/test_pipeline.py -v        # 16 tests
```

### 2. **Performance Tests** (20 tests)
Verifies system meets performance SLAs.

```bash
# Run performance suite
pytest tests/unit/test_performance.py -v

# Categories tested:
# - Skill loading (<10ms)
# - Embeddings (<100ms)
# - Distance calc (<5ms)
# - Text ops (<10ms)
# - Graphs (<3s)
# - Cost tracking (<1ms)
# - End-to-end (<5s)
```

### 3. **Integration Tests** (Placeholder)
Tests component interactions.

```bash
pytest tests/integration/ -v
```

---

## 📈 Coverage by Module

| Module | Coverage | Missing Lines | Status |
|--------|----------|--------------|--------|
| `errors.py` | 100% | 0 | ✅ Perfect |
| `config.py` | 90% | 8 | ✅ Excellent |
| `analysis.py` | 88% | 35 | ✅ Good |
| `agent_tester.py` | 88% | 19 | ✅ Good |
| `cost_tracker.py` | 88% | 7 | ✅ Good |
| `pipeline.py` | 82% | 30 | ✅ Good |
| `logger.py` | 80% | 4 | ✅ Good |

---

## 🎯 Performance Benchmarks

All tests must meet these SLA targets:

| Operation | Target | Actual | Status |
|-----------|--------|--------|--------|
| Skill Loading | <10ms | ~8ms | ✅ |
| TF-IDF Embedding | <100ms | ~35ms | ✅ |
| Cosine Distance | <5ms | ~2ms | ✅ |
| Text Similarity | <10ms | ~5ms | ✅ |
| Graph Generation | <3s | ~2.1s | ✅ |
| Cost Tracking | <1ms | ~0.3ms | ✅ |
| Full Analysis | <5s | ~1.8s | ✅ |

---

## 🔄 CI/CD Integration

### GitHub Actions Workflows

**1. Test & Coverage** (`.github/workflows/test-and-coverage.yml`)
- ✅ Runs on every push to main/develop/tests_to_get_100
- ✅ Tests on Python 3.11 and 3.12
- ✅ Enforces 85% coverage threshold
- ✅ Uploads coverage reports to Codecov
- ✅ Creates HTML/XML coverage artifacts

**2. PR Validation** (`.github/workflows/validate-pr.yml`)
- ✅ Quick validation for pull requests
- ✅ Syntax checking
- ✅ Skills structure validation
- ✅ Coverage impact analysis

### Triggering CI/CD

```bash
# Push to trigger CI/CD
git add .
git commit -m "Your changes"
git push origin tests_to_get_100

# CI/CD will automatically:
# 1. Run all 103 tests
# 2. Check coverage >= 85%
# 3. Generate reports
# 4. Upload artifacts
```

---

## 📝 Writing New Tests

### Test File Template

```python
"""
Tests for [module_name]
"""

import pytest
from unittest.mock import Mock, patch
from src.[module] import [function]


class Test[FunctionName]:
    """Test suite for [function_name]"""
    
    def test_[function]_success(self):
        """Test: [function] works with valid input"""
        # Arrange
        input_data = "test"
        
        # Act
        result = function(input_data)
        
        # Assert
        assert result is not None
    
    def test_[function]_error_handling(self):
        """Test: [function] handles errors correctly"""
        with pytest.raises(ValueError):
            function(None)
```

### Running New Tests

```bash
# Run your new test file
pytest tests/unit/test_new_module.py -v

# Check coverage impact
pytest tests/unit/test_new_module.py --cov=src/new_module --cov-report=term-missing
```

---

## 🐛 Debugging Failed Tests

### View Detailed Output

```bash
# Verbose output with full tracebacks
pytest tests/ -vv --tb=long

# Show local variables in tracebacks
pytest tests/ -vv --tb=long --showlocals

# Stop at first failure
pytest tests/ -x

# Drop into debugger on failure
pytest tests/ --pdb
```

### Check Specific Module Coverage

```bash
# Focus on one module
pytest tests/unit/test_analysis.py --cov=src/analysis --cov-report=term-missing

# See which lines aren't covered
coverage report -m src/analysis.py
```

---

## 📊 Generating Reports

### HTML Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### XML Coverage Report (for CI)
```bash
pytest tests/ --cov=src --cov-report=xml
cat coverage.xml
```

### Terminal Report
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### JSON Report
```bash
pytest tests/ --json-report --json-report-file=test_report.json
```

---

## 🎯 Coverage Goals

### Target Coverage by Module Type

| Type | Target | Why |
|------|--------|-----|
| **Critical** (errors) | 100% | Zero tolerance for bugs |
| **Core** (analysis, pipeline) | 85-90% | Comprehensive coverage |
| **Utilities** (logger, config) | 80-85% | Adequate coverage |
| **Boilerplate** (\_\_init\_\_) | 0-50% | Not critical |

### Acceptable Uncovered Lines

✅ **Allowed:**
- Debug print statements
- Rare error paths (filesystem failures)
- Platform-specific code
- Visualization backend edge cases

❌ **Not Allowed:**
- Main business logic
- Core algorithms
- User-facing functions
- Error handling for common cases

---

## 🔍 Test Fixtures

### Using Existing Fixtures

```python
# From conftest.py
def test_with_temp_dir(temp_dir):
    """Uses temporary directory fixture"""
    file_path = temp_dir / "test.txt"
    file_path.write_text("test")
    assert file_path.exists()

def test_with_mock_skills(mock_skills_dir, monkeypatch):
    """Uses mock skills directory"""
    from pipeline import load_skill
    monkeypatch.setattr("pipeline.SKILLS_DIR", mock_skills_dir)
    skill = load_skill("english-to-french-translator")
    assert skill is not None
```

### Available Fixtures

- `temp_dir` - Temporary directory
- `mock_skills_dir` - Mock skills directory
- `mock_anthropic_client` - Mock API client
- `mock_analysis_outputs` - Mock output files

---

## ⚡ Performance Testing

### Running Performance Tests

```bash
# All performance tests
pytest tests/unit/test_performance.py -v

# Specific performance test
pytest tests/unit/test_performance.py::TestSkillLoadingPerformance -v
```

### Adding Performance Tests

```python
import time

def test_operation_performance():
    """Test: Operation completes within SLA"""
    start_time = time.perf_counter()
    
    # Your operation
    result = expensive_operation()
    
    elapsed = time.perf_counter() - start_time
    
    # Assert SLA met
    assert elapsed < 0.1, f"Too slow: {elapsed:.3f}s > 0.1s"
    assert result is not None
```

---

## 📚 Documentation

### Test Documentation Locations

| Document | Location | Purpose |
|----------|----------|---------|
| **Comprehensive Report** | `docs/COMPREHENSIVE_TESTING_REPORT.md` | Complete analysis |
| **This Guide** | `docs/TESTING_QUICK_REFERENCE.md` | Quick commands |
| **Strategy** | `docs/adrs/ADR-005-testing-strategy.md` | Approach & rationale |
| **Coverage HTML** | `htmlcov/index.html` | Visual coverage |
| **CI/CD Setup** | `docs/CI_CD_SETUP.md` | Automation |

---

## 🎓 Best Practices

### ✅ DO

- ✅ Write tests for new features
- ✅ Test error paths
- ✅ Use descriptive test names
- ✅ Mock external dependencies
- ✅ Run tests before committing
- ✅ Keep tests fast (<10s total)
- ✅ Maintain 85%+ coverage

### ❌ DON'T

- ❌ Test implementation details
- ❌ Make tests dependent on each other
- ❌ Use hardcoded paths
- ❌ Skip error case testing
- ❌ Commit without running tests
- ❌ Let coverage drop below 85%
- ❌ Write slow tests without marking them

---

## 🆘 Common Issues

### Issue: Tests fail locally but pass in CI

**Solution:**
```bash
# Clean pytest cache
rm -rf .pytest_cache
rm -rf __pycache__

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run tests fresh
pytest tests/ --cache-clear
```

### Issue: Coverage report not generating

**Solution:**
```bash
# Ensure coverage installed
pip install pytest-cov coverage

# Generate with explicit options
pytest tests/ --cov=src --cov-report=html:htmlcov

# Check if file created
ls -la htmlcov/index.html
```

### Issue: Performance tests failing

**Solution:**
```bash
# Run with longer timeout
pytest tests/unit/test_performance.py -v --timeout=60

# Check system load
top

# Run individually
pytest tests/unit/test_performance.py::TestSkillLoadingPerformance::test_skill_loading_time -v
```

---

## 📞 Getting Help

**For Testing Issues:**
1. Check this guide first
2. Review `docs/COMPREHENSIVE_TESTING_REPORT.md`
3. Look at test examples in `tests/unit/`
4. Check pytest documentation: https://docs.pytest.org/

**For Coverage Issues:**
1. Generate HTML report: `pytest tests/ --cov=src --cov-report=html`
2. Review `htmlcov/index.html` for detailed analysis
3. Check `docs/adrs/ADR-005-testing-strategy.md` for targets

**For CI/CD Issues:**
1. Check workflow logs in GitHub Actions
2. Review `.github/workflows/` configuration
3. See `docs/CI_CD_SETUP.md`

---

## ✅ Checklist Before Commit

```bash
# 1. Run all tests
pytest tests/ -v
# ✅ All 103 tests pass

# 2. Check coverage
pytest tests/ --cov=src --cov-fail-under=85
# ✅ Coverage >= 85%

# 3. Check for errors
pytest tests/ --tb=short
# ✅ No errors or warnings

# 4. Generate fresh report
pytest tests/ --cov=src --cov-report=html
# ✅ Report generated

# 5. Commit!
git add .
git commit -m "Your message"
git push
```

---

**Last Updated:** November 27, 2025  
**Status:** ✅ All Systems Operational  
**Test Count:** 103 tests  
**Coverage:** 86.33%


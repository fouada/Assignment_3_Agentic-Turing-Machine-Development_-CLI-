# ADR-005: Comprehensive Testing Strategy

**Status:** Accepted  
**Date:** 2025-11-26

---

## Context

The system requires:
- High reliability (95%+ error coverage)
- Maintainability (easy to refactor)
- Confidence in changes
- Grade requirement: 85%+ test coverage

---

## Decision

Implement **comprehensive testing strategy** with:

1. **Unit Tests** - Test individual functions in isolation
2. **Integration Tests** - Test component interactions
3. **Fixtures** - Reusable test data and mocks
4. **Coverage Tracking** - pytest-cov with 85%+ target
5. **Mocking** - Mock external dependencies (API, file system)

### Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── fixtures/
│   ├── mock_data.py     # Test data
│   └── __init__.py
├── unit/
│   ├── test_pipeline.py
│   ├── test_analysis.py
│   ├── test_config.py
│   └── test_agent_tester.py
└── integration/
    └── test_full_pipeline.py
```

### Key Testing Principles

1. **Mock External Dependencies**
   ```python
   @pytest.fixture
   def mock_anthropic_client():
       client = Mock()
       response = Mock()
       response.content = [Mock(text="Bonjour")]
       response.usage = Mock(input_tokens=10, output_tokens=5)
       client.messages.create.return_value = response
       return client
   ```

2. **Test Error Paths**
   ```python
   def test_skill_not_found():
       with pytest.raises(SkillNotFoundError):
           load_skill("nonexistent-skill")
   ```

3. **Use Fixtures for Repeated Setup**
   ```python
   @pytest.fixture
   def temp_skills_dir(tmp_path):
       skills_dir = tmp_path / "skills"
       skills_dir.mkdir()
       # Create mock skills
       return skills_dir
   ```

---

## Rationale

**✅ Advantages:**
1. **High confidence** - Changes don't break things
2. **Fast feedback** - Catch bugs immediately
3. **Documentation** - Tests show how code works
4. **Refactoring safety** - Confident changes
5. **Grade requirement** - Meets 85%+ coverage

**Alternatives Rejected:**
- ❌ No tests - Unprofessional, risky
- ❌ Manual testing - Not scalable, error-prone
- ❌ Integration tests only - Too slow, less precise

---

## Test Coverage Requirements

| Module | Target Coverage | Actual |
|--------|----------------|---------|
| src/errors.py | 100% | 100% ✅ |
| src/config.py | 90%+ | 90% ✅ |
| src/cost_tracker.py | 88%+ | 88% ✅ |
| src/analysis.py | 84%+ | 88% ✅ |
| src/pipeline.py | 82%+ | 82% ✅ |
| src/logger.py | 80%+ | 80% ✅ |
| src/agent_tester.py | 71%+ | 88% ✅ |
| **Overall** | **85%+** | **86%** ✅ |

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_pipeline.py -v

# Run specific test
pytest tests/unit/test_pipeline.py::TestLoadSkill::test_load_skill_success -v
```

---

## Consequences

**Positive:**
- ✅ 86% test coverage achieved
- ✅ 83 tests passing
- ✅ Fast test execution (~7 seconds)
- ✅ Confidence in code quality
- ✅ Easy to add new tests

**Negative:**
- ⚠️ Test maintenance overhead
- ⚠️ Need to update tests when changing code

---

## Related Decisions

- [ADR-001: Claude Agent Skills](ADR-001-claude-agent-skills.md)
- [ADR-004: Error Handling](ADR-004-error-handling.md)

---

**Status:** Implemented and Accepted

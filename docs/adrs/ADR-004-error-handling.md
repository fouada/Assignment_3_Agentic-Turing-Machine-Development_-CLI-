# ADR-004: Custom Exception Hierarchy for Error Handling

**Status:** Accepted  
**Date:** 2025-11-26

---

## Context

The system needs robust error handling for:
- Skill loading failures
- API errors (rate limits, network issues)
- Configuration problems
- File I/O errors
- Analysis failures

Generic Python exceptions (`Exception`, `ValueError`) don't provide enough context for precise error handling and user-friendly messages.

---

## Decision

Implement a **custom exception hierarchy** with specific exception types for each error category:

```python
class ATMError(Exception):
    """Base exception for all ATM errors."""
    pass

class SkillNotFoundError(ATMError):
    """Skill file not found."""
    pass

class SkillLoadError(ATMError):
    """Error loading skill file."""
    pass

class TranslationError(ATMError):
    """Translation failed."""
    pass

class APIError(ATMError):
    """API call failed."""
    pass

class ValidationError(ATMError):
    """Input validation failed."""
    pass

class ConfigurationError(ATMError):
    """Configuration invalid."""
    pass

class AnalysisError(ATMError):
    """Analysis failed."""
    pass

class FileOperationError(ATMError):
    """File operation failed."""
    pass
```

---

## Rationale

**✅ Advantages:**
1. **Precise error handling** - Catch specific exceptions
2. **Better error messages** - Custom messages per error type
3. **Easier debugging** - Know exactly what failed
4. **Type safety** - Type hints work better
5. **Professional quality** - Production-ready error handling

**Alternatives Rejected:**
- ❌ Generic `Exception` - Too vague, hard to handle
- ❌ Built-in exceptions only - Not specific enough
- ❌ String error codes - Less Pythonic, error-prone

---

## Usage Pattern

```python
try:
    skill = load_skill("english-to-french-translator")
except SkillNotFoundError as e:
    logger.error(f"Skill not found: {e}")
    print("Please check skill name and try again.")
    sys.exit(1)
except SkillLoadError as e:
    logger.error(f"Failed to load skill: {e}")
    print("Skill file may be corrupted.")
    sys.exit(1)
```

---

## Consequences

**Positive:**
- ✅ Clear error types throughout codebase
- ✅ Easy to add new exception types
- ✅ Better user experience with specific messages
- ✅ Easier testing with pytest.raises()

**Negative:**
- ⚠️ More code (minimal - 28 lines)
- ⚠️ Need to document exceptions

---

## Related Decisions

- [ADR-001: Claude Agent Skills](ADR-001-claude-agent-skills.md)
- [ADR-005: Testing Strategy](ADR-005-testing-strategy.md)

---

**Status:** Implemented and Accepted

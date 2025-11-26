# ADR-001: Claude Agent Skills Architecture

**Status:** Accepted  
**Date:** 2025-11-26  
**Decision Makers:** Development Team  
**Technical Story:** Multi-agent translation system design

---

## Context

We need to design a system that performs sequential translations through multiple languages (English → French → Hebrew → English) using AI agents. The system must be:
- Flexible and extensible for new languages
- Easy to configure and modify agent behavior
- Maintainable without requiring code changes for prompt updates
- Testable in isolation (individual agents)

### Constraints
- Using Anthropic Claude API for AI capabilities
- Need to support multiple translation skills
- Must track costs per API call
- Need comprehensive logging

---

## Decision

We will implement a **skill-based agent architecture** where:

1. **Skills are defined in separate markdown files** stored in a `skills/` directory
2. **Each skill is self-contained** with its own directory and SKILL.md file
3. **Skills contain:**
   - Agent description
   - Detailed instructions/prompts
   - Examples (optional)
   - Metadata (optional)

4. **Skills are loaded dynamically** at runtime
5. **No hardcoded prompts** in the codebase

### Directory Structure
```
skills/
├── english-to-french-translator/
│   └── SKILL.md
├── french-to-hebrew-translator/
│   └── SKILL.md
└── hebrew-to-english-translator/
    └── SKILL.md
```

### Example Skill File
```markdown
# English to French Translator

## Description
Translates English text to French with high accuracy.

## Instructions
You are an expert English to French translator...
[Detailed prompt instructions]

## Examples
Input: Hello, how are you?
Output: Bonjour, comment allez-vous ?
```

---

## Rationale

### Why Skill-Based Architecture?

**✅ Advantages:**

1. **Separation of Concerns**
   - Prompts separated from code logic
   - Easy to update without code changes
   - Non-developers can modify prompts

2. **Flexibility**
   - Add new translation pairs by creating new skill files
   - Modify agent behavior without redeployment
   - Version control for prompts

3. **Testability**
   - Test skills individually (`test_agent.py`)
   - Isolate prompt issues from code issues
   - A/B test different prompts

4. **Maintainability**
   - Prompts in human-readable markdown
   - Easy to review and diff changes
   - Self-documenting (description in file)

5. **Extensibility**
   - Support for future languages
   - Plugin-like architecture
   - Skill metadata for advanced features

**❌ Alternatives Considered:**

1. **Hardcoded Prompts in Code**
   - ❌ Requires code changes for prompt updates
   - ❌ Difficult for non-developers to modify
   - ❌ Harder to version control prompts separately

2. **Database Storage**
   - ❌ Overkill for this use case
   - ❌ Requires database setup
   - ❌ Less transparent than files

3. **JSON Configuration**
   - ❌ Less human-readable than markdown
   - ❌ Escaping issues with multi-line prompts
   - ✅ Could be viable alternative

---

## Consequences

### Positive
- ✅ Rapid iteration on prompts
- ✅ Clear separation of concerns
- ✅ Easy to add new languages
- ✅ Prompt engineering can be done independently
- ✅ Version control for prompts
- ✅ Self-documenting skills

### Negative
- ⚠️ File I/O overhead (minimal, ~1-5ms)
- ⚠️ No validation of skill format (could add)
- ⚠️ Skills must exist before runtime

### Mitigation Strategies
- **Performance:** Cache loaded skills in memory (future optimization)
- **Validation:** Add skill schema validation (future feature)
- **Error Handling:** Comprehensive error messages for missing/invalid skills

---

## Implementation Details

### Skill Loading
```python
def load_skill(skill_name: str) -> Dict[str, str]:
    """Load a skill from the skills directory."""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    
    if not skill_path.exists():
        raise SkillNotFoundError(f"Skill not found: {skill_name}")
    
    try:
        content = skill_path.read_text(encoding='utf-8')
        return {"name": skill_name, "content": content}
    except Exception as e:
        raise SkillLoadError(f"Failed to load skill: {e}")
```

### Skill Usage
```python
skill = load_skill("english-to-french-translator")
response = client.messages.create(
    model=config.model_name,
    messages=[{
        "role": "user",
        "content": f"{skill['content']}\n\nTranslate: {input_text}"
    }]
)
```

---

## Validation

### How We Verify This Decision
1. **Functional Testing:**
   - Load all skills successfully
   - Execute translations with each skill
   - Verify skill not found errors

2. **Performance Testing:**
   - Measure skill loading time (<5ms)
   - Ensure no bottleneck

3. **Usability Testing:**
   - Non-developer can add new skill
   - Prompt updates don't require code changes

### Success Metrics
- ✅ Skill loading time: <5ms
- ✅ 100% skill availability
- ✅ Zero hardcoded prompts in code
- ✅ New skill can be added in <5 minutes

---

## Alternatives in Detail

### Alternative 1: Hardcoded Prompts
```python
# ❌ NOT CHOSEN
EN_TO_FR_PROMPT = """
You are an expert translator from English to French...
"""

FR_TO_HE_PROMPT = """
You are an expert translator from French to Hebrew...
"""
```

**Rejected Because:**
- Requires code changes for prompt updates
- Harder to collaborate on prompts
- No clear separation

---

### Alternative 2: Configuration File
```yaml
# ❌ NOT CHOSEN
skills:
  english-to-french:
    prompt: |
      You are an expert translator...
  french-to-hebrew:
    prompt: |
      You are an expert translator...
```

**Rejected Because:**
- YAML multiline strings are harder to edit
- Less self-documenting than markdown
- Mixing config and content

---

### Alternative 3: Database Storage
```sql
-- ❌ NOT CHOSEN
CREATE TABLE skills (
    name VARCHAR(255),
    content TEXT,
    metadata JSON
);
```

**Rejected Because:**
- Overkill for 3 skills
- Adds dependency (database)
- Less transparent
- Harder to version control

---

## Related Decisions
- [ADR-002: Local Embeddings](ADR-002-local-embeddings.md)
- [ADR-003: Cost Tracking](ADR-003-cost-tracking.md)
- [ADR-005: Testing Strategy](ADR-005-testing-strategy.md)

---

## References
- [Anthropic Claude API Documentation](https://docs.anthropic.com)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Architecture Decision Records (ADRs)](https://adr.github.io/)

---

## Notes
- Skills can be extended with metadata in future (version, author, etc.)
- Consider skill validation schema (JSON Schema) for future
- Plugin system could build on this foundation

---

**Last Updated:** 2025-11-26  
**Status:** Implemented and Accepted

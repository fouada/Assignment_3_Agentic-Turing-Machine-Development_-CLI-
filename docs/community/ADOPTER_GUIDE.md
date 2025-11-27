# Adopter's Guide: Building Your Own Multi-Agent System

This guide helps you adapt the Agentic Turing Machine project for your own use cases. Whether you're building a different translation pipeline, a non-translation agent system, or using this as a learning resource, this guide will help you get started.

## Table of Contents

1. [Before You Start](#before-you-start)
2. [Fork & Setup](#fork--setup)
3. [Customization Scenarios](#customization-scenarios)
4. [Step-by-Step Adaptation](#step-by-step-adaptation)
5. [Best Practices](#best-practices)
6. [Common Pitfalls](#common-pitfalls)
7. [Getting Help](#getting-help)

---

## Before You Start

### Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.11 | 3.12 |
| Memory | 2GB | 4GB |
| Claude API access | Required | Required |
| Git experience | Basic | Intermediate |

### What You'll Learn

By following this guide, you'll learn how to:

- ✅ Create custom Claude Agent Skills
- ✅ Build multi-agent pipelines
- ✅ Implement semantic analysis
- ✅ Add noise/perturbation testing
- ✅ Set up proper testing and CI/CD
- ✅ Document your project professionally

---

## Fork & Setup

### Step 1: Fork the Repository

```bash
# Option A: GitHub CLI
gh repo fork talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI- --clone

# Option B: Manual
# 1. Click "Fork" on GitHub
# 2. Clone your fork:
git clone https://github.com/YOUR-USERNAME/Assignment_3_Agentic-Turing-Machine-Development_-CLI-.git
cd Assignment_3_Agentic-Turing-Machine-Development_-CLI-
```

### Step 2: Rename the Project

```bash
# Rename the directory
mv Assignment_3_Agentic-Turing-Machine-Development_-CLI- your-project-name
cd your-project-name

# Update pyproject.toml
sed -i 's/agentic-turing-machine/your-project-name/g' pyproject.toml
```

### Step 3: Setup Development Environment

```bash
# Install UV (fast package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Verify setup
pytest tests/ -v
```

### Step 4: Configure Your API Key

```bash
# Create .env file (not committed to git)
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Or export directly
export ANTHROPIC_API_KEY='your-key-here'
```

---

## Customization Scenarios

### Scenario 1: Different Translation Languages

**Goal:** Replace EN→FR→HE→EN with your language chain (e.g., EN→ES→DE→EN)

**Steps:**

1. Create new skill directories:
```bash
mkdir -p skills/english-to-spanish-translator
mkdir -p skills/spanish-to-german-translator
mkdir -p skills/german-to-english-translator
```

2. Create SKILL.md files (use template from [REUSABLE_TEMPLATES.md](REUSABLE_TEMPLATES.md))

3. Update `src/pipeline.py`:
```python
TRANSLATION_CHAIN = [
    "english-to-spanish-translator",
    "spanish-to-german-translator",
    "german-to-english-translator",
]
```

4. Update tests to match new languages

---

### Scenario 2: Non-Translation Agent System

**Goal:** Build a different multi-agent system (e.g., summarization → analysis → report)

**Steps:**

1. **Define your agent chain:**
```
Document → Summarizer → Analyzer → Report Generator
```

2. **Create skills:**
```bash
mkdir -p skills/document-summarizer
mkdir -p skills/content-analyzer
mkdir -p skills/report-generator
```

3. **Modify the pipeline:**
```python
# src/pipeline.py
class AgentPipeline:
    AGENT_CHAIN = [
        "document-summarizer",
        "content-analyzer", 
        "report-generator",
    ]
    
    async def run(self, document: str) -> Report:
        result = document
        for agent_name in self.AGENT_CHAIN:
            result = await self.invoke_agent(agent_name, result)
        return result
```

4. **Create appropriate analysis:**
```python
# src/analysis.py - customize for your metrics
def analyze_summarization_quality(original: str, summary: str) -> float:
    """Analyze how well the summary captures key points."""
    ...
```

---

### Scenario 3: Research Extension

**Goal:** Use this as a base for your own research

**Key files to customize:**

| File | Purpose | Customization |
|------|---------|---------------|
| `src/analysis.py` | Metrics | Add your metrics |
| `src/sensitivity_analysis.py` | Parameter study | Add your parameters |
| `docs/ACADEMIC_PAPER.md` | Paper template | Write your paper |
| `docs/RESEARCH_METHODOLOGY.md` | Methods | Document your methods |

**Adding a new analysis module:**

1. Copy template from [REUSABLE_TEMPLATES.md](REUSABLE_TEMPLATES.md#analysis-module-template)
2. Implement your analysis logic
3. Add tests (85%+ coverage)
4. Document in `docs/`

---

### Scenario 4: Learning & Teaching

**Goal:** Use this as a teaching resource

**Learning path:**

```
1. README.md (overview)
   ↓
2. docs/START_HERE_MIT_PRD.md (quick start)
   ↓
3. skills/*/SKILL.md (understand agents)
   ↓
4. src/pipeline.py (understand orchestration)
   ↓
5. src/analysis.py (understand analysis)
   ↓
6. tests/ (understand testing)
```

**For classroom use:**

- Assign students to add new languages
- Have students implement new metrics
- Use the research methodology for projects
- Discuss architectural decisions (ADRs)

---

## Step-by-Step Adaptation

### Phase 1: Core Customization (Day 1)

```bash
# 1. Fork and clone (see above)

# 2. Create your first custom agent
cat > skills/my-first-agent/SKILL.md << 'EOF'
# My First Agent

## Description
A simple agent that [does something].

## Instructions
You are an agent that [detailed instructions].

## Examples
Input: [example]
Output: [example]
EOF

# 3. Test your agent
python src/agent_tester.py my-first-agent "test input"
```

### Phase 2: Pipeline Integration (Day 2)

```python
# 1. Update pipeline configuration
# src/pipeline.py

AGENT_CHAIN = [
    "my-first-agent",
    "my-second-agent",
    # ...
]

# 2. Run the pipeline
python scripts/experiment/run_with_skills.py --noise 25
```

### Phase 3: Analysis Customization (Day 3)

```python
# 1. Add your custom metrics
# src/analysis.py

def your_custom_metric(original: str, result: str) -> float:
    """Calculate your custom metric."""
    # Your implementation
    return score

# 2. Integrate into analysis
results = {
    "cosine_distance": calculate_cosine_distance(original, result),
    "your_metric": your_custom_metric(original, result),
}
```

### Phase 4: Testing & CI/CD (Day 4)

```python
# 1. Add tests for your customizations
# tests/unit/test_your_module.py

def test_your_custom_metric():
    assert your_custom_metric("test", "test") == expected_value

# 2. Run tests
pytest tests/ --cov=src --cov-report=term

# 3. Verify CI/CD
git push origin your-branch
# Check GitHub Actions
```

### Phase 5: Documentation (Day 5)

```bash
# 1. Update README.md with your project description

# 2. Create your own docs
# - docs/YOUR_PROJECT.md
# - docs/YOUR_METHODOLOGY.md

# 3. Update CHANGELOG.md

# 4. Prepare for release
git tag v1.0.0
git push origin v1.0.0
```

---

## Best Practices

### 1. Keep the Core Architecture

The skill-based architecture is well-tested. Keep:
- `skills/*/SKILL.md` structure
- Pipeline orchestration pattern
- Error handling mechanisms
- Testing patterns

### 2. Maintain Code Quality

```bash
# Run before every commit
black src/ tests/
isort src/ tests/
mypy src/
pytest tests/ --cov=src --cov-fail-under=85
```

### 3. Document Your Changes

Every major change should update:
- [ ] README.md (if user-facing)
- [ ] Relevant docs in `docs/`
- [ ] CHANGELOG.md
- [ ] Docstrings in code

### 4. Test Thoroughly

```python
# For every new feature:
# 1. Unit tests
# 2. Integration tests (if applicable)
# 3. Edge case tests

# Target: 85%+ coverage
```

### 5. Keep Dependencies Minimal

```toml
# pyproject.toml - only add what you need
[project.optional-dependencies]
# Group dependencies by purpose
analysis = ["numpy", "scikit-learn"]
viz = ["matplotlib", "plotly"]
```

---

## Common Pitfalls

### Pitfall 1: Overcomplicating Skills

❌ **Don't:**
```markdown
# Bad SKILL.md
You are a super advanced AI that must analyze everything
and provide comprehensive detailed output with explanations
and reasoning and multiple perspectives...
```

✅ **Do:**
```markdown
# Good SKILL.md
You translate English to French.
Return ONLY the French translation.
No explanations. No commentary.
```

### Pitfall 2: Not Testing Edge Cases

❌ **Don't:**
```python
def test_analysis():
    assert analyze("normal input") == expected  # Only happy path
```

✅ **Do:**
```python
def test_analysis_normal():
    assert analyze("normal input") == expected

def test_analysis_empty():
    with pytest.raises(ValueError):
        analyze("")

def test_analysis_unicode():
    assert analyze("日本語テスト") == expected_unicode
```

### Pitfall 3: Hardcoding Paths

❌ **Don't:**
```python
data = open("/home/user/project/data/input.txt")
```

✅ **Do:**
```python
from pathlib import Path
data_path = Path(__file__).parent.parent / "data" / "input.txt"
```

### Pitfall 4: Ignoring API Costs

❌ **Don't:**
```python
# Running experiments in a loop without cost tracking
for noise in range(0, 100):
    run_experiment(noise)  # 💸 Expensive!
```

✅ **Do:**
```python
from src.cost_tracker import CostTracker

tracker = CostTracker()
for noise in [0, 25, 50]:  # Strategic noise levels
    with tracker.track("experiment"):
        run_experiment(noise)
print(f"Total cost: ${tracker.total_cost:.2f}")
```

---

## Getting Help

### Self-Help Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| Documentation Index | `docs/DOCUMENTATION_INDEX.md` | Find any document |
| API Reference | `docs/api/API.md` | Code documentation |
| ADRs | `docs/adrs/` | Understand design decisions |
| Prompt Library | `docs/PROMPTS.md` | Learn prompt engineering |

### Community Support

1. **GitHub Issues**: For bugs and feature requests
2. **GitHub Discussions**: For questions and ideas
3. **Email**: Contact maintainers (see README)

### Contributing Back

If you build something useful:

1. Consider contributing it back
2. Open a PR with your enhancement
3. Share in Discussions

---

## Checklist: Ready to Launch?

Before going live with your adaptation:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Coverage ≥ 85% (`pytest --cov=src --cov-fail-under=85`)
- [ ] README updated for your project
- [ ] LICENSE file present (update names if needed)
- [ ] CHANGELOG documents your changes
- [ ] API key not committed to repo
- [ ] CI/CD workflows updated if needed
- [ ] Documentation reviewed and accurate

---

## Success Stories

*Have you built something with this project? Let us know! We'd love to feature your work here.*

---

## License

This guide and the associated project are MIT licensed. You are free to use, modify, and distribute your adaptations.

---

*Last Updated: November 2025*

**Happy building! 🚀**


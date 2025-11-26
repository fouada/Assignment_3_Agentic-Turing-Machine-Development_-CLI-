# API Documentation
## Agentic Turing Machine - Public API Reference

**Version:** 1.0  
**Last Updated:** 2025-11-26

---

## Table of Contents
1. [Pipeline Module](#pipeline-module)
2. [Analysis Module](#analysis-module)
3. [Configuration Module](#configuration-module)
4. [Cost Tracker Module](#cost-tracker-module)
5. [Error Module](#error-module)
6. [Agent Tester Module](#agent-tester-module)

---

## Pipeline Module (`src/pipeline.py`)

### `load_skill(skill_name: str) -> Dict[str, str]`

Load a translation skill from the skills directory.

**Parameters:**
- `skill_name` (str): Name of the skill directory (e.g., "english-to-french-translator")

**Returns:**
- `Dict[str, str]`: Dictionary with keys "name" and "content"

**Raises:**
- `SkillNotFoundError`: If skill file doesn't exist
- `SkillLoadError`: If skill file cannot be read

**Example:**
```python
skill = load_skill("english-to-french-translator")
print(skill["name"])    # "english-to-french-translator"
print(skill["content"]) # Skill markdown content
```

---

### `create_noisy_input(text: str, noise_level: int) -> str`

Apply controlled character-level noise to input text.

**Parameters:**
- `text` (str): Original text
- `noise_level` (int): Percentage of characters to modify (0-100)

**Returns:**
- `str`: Text with applied noise

**Example:**
```python
original = "Hello, world!"
noisy = create_noisy_input(original, 25)
# Result: "Helko, wosld!" (approximately 25% changed)
```

---

### `run_translation_with_skill(client, skill_name: str, input_text: str, stage: int) -> str`

Execute a translation using Claude API with specified skill.

**Parameters:**
- `client`: Anthropic client instance
- `skill_name` (str): Skill to use
- `input_text` (str): Text to translate
- `stage` (int): Pipeline stage number (1-3)

**Returns:**
- `str`: Translated text

**Raises:**
- `APIError`: If API call fails
- `TranslationError`: If translation cannot be extracted

**Example:**
```python
import anthropic
client = anthropic.Anthropic(api_key=API_KEY)
french = run_translation_with_skill(
    client, "english-to-french-translator", "Hello", 1
)
```

---

### `run_translation_chain(input_text: str, noise_level: int) -> None`

Run complete 3-stage translation chain and save outputs.

**Parameters:**
- `input_text` (str): Original English text
- `noise_level` (int): Noise percentage (0-100)

**Side Effects:**
- Creates output directory
- Writes translation files
- Logs execution
- Records costs

**Example:**
```python
run_translation_chain("Good morning. How are you?", noise_level=25)
# Creates outputs/noise_25/agent1_french.txt, etc.
```

---

## Analysis Module (`src/analysis.py`)

### `get_local_embedding(texts: List[str]) -> np.ndarray`

Generate TF-IDF embeddings for texts.

**Parameters:**
- `texts` (List[str]): List of text strings

**Returns:**
- `np.ndarray`: TF-IDF vectors (shape: [n_texts, n_features])

**Raises:**
- `ValueError`: If texts list is empty
- `AnalysisError`: If embedding generation fails

**Example:**
```python
texts = ["Hello world", "Bonjour monde"]
embeddings = get_local_embedding(texts)
# Shape: (2, n_features)
```

---

### `calculate_cosine_distance(vec1: np.ndarray, vec2: np.ndarray) -> float`

Calculate cosine distance between two vectors.

**Parameters:**
- `vec1` (np.ndarray): First vector
- `vec2` (np.ndarray): Second vector

**Returns:**
- `float`: Cosine distance in range [0, 2]

**Raises:**
- `AnalysisError`: If vector dimensions don't match

**Formula:**
$$d(x,y) = 1 - \frac{x \cdot y}{||x|| \cdot ||y||}$$

**Example:**
```python
dist = calculate_cosine_distance(vec1, vec2)
# 0.0 = identical, 1.0 = orthogonal, 2.0 = opposite
```

---

### `calculate_word_overlap(text1: str, text2: str) -> float`

Calculate word-level overlap between texts.

**Parameters:**
- `text1` (str): First text
- `text2` (str): Second text

**Returns:**
- `float`: Overlap ratio in range [0, 1]

**Example:**
```python
overlap = calculate_word_overlap("hello world", "hello there")
# Result: 0.333 (1 common word / 3 total unique words)
```

---

### `analyze_semantic_drift() -> Dict[str, Any]`

Analyze semantic drift across all noise levels.

**Returns:**
- `Dict[str, Any]`: Results dictionary with metrics per noise level

**Side Effects:**
- Reads from outputs/ and data/ directories
- Writes to results/analysis_results_local.json
- Generates visualization graphs

**Example:**
```python
results = analyze_semantic_drift()
print(results["noise_0"]["cosine_distance"])
```

---

## Configuration Module (`src/config.py`)

### `class Config`

Singleton configuration manager.

**Properties:**
- `model_name: str` - Claude model name
- `temperature: float` - Model temperature (0.0-1.0)
- `max_tokens: int` - Maximum output tokens
- `noise_levels: List[int]` - Noise levels to test
- `output_dir: Path` - Output directory path
- `results_dir: Path` - Results directory path
- `cost_tracking_enabled: bool` - Enable cost tracking
- `plugins_enabled: bool` - Enable plugins

**Methods:**
- `get(key: str, default: Any) -> Any` - Get config value
- `validate() -> None` - Validate configuration

**Example:**
```python
from config import Config

config = Config()
print(config.model_name)        # "claude-3-5-sonnet-20241022"
print(config.temperature)       # 0.7
print(config.noise_levels)      # [0, 25, 50, 75, 100]
```

---

## Cost Tracker Module (`src/cost_tracker.py`)

### `class CostTracker`

Track API usage and costs.

**Constructor:**
```python
CostTracker(model_name: str)
```

**Methods:**

#### `record_request(usage) -> None`

Record an API request's token usage.

**Parameters:**
- `usage`: Response usage object with `input_tokens` and `output_tokens`

**Example:**
```python
tracker = CostTracker("claude-3-5-sonnet-20241022")
response = client.messages.create(...)
tracker.record_request(response.usage)
```

#### `get_total_cost() -> float`

Get total cost of all recorded requests.

**Returns:**
- `float`: Total cost in USD

#### `export_report(output_path: Path) -> None`

Export cost report to JSON file.

**Parameters:**
- `output_path` (Path): Output file path

**Example:**
```python
tracker.export_report(Path("results/cost_analysis.json"))
```

---

## Error Module (`src/errors.py`)

### Exception Hierarchy

```python
ATMError (base)
├── SkillNotFoundError
├── SkillLoadError
├── TranslationError
├── APIError
├── ValidationError
├── ConfigurationError
├── AnalysisError
└── FileOperationError
```

**Usage:**
```python
from errors import SkillNotFoundError, APIError

try:
    skill = load_skill("nonexistent")
except SkillNotFoundError as e:
    logger.error(f"Skill error: {e}")
except APIError as e:
    logger.error(f"API error: {e}")
```

---

## Agent Tester Module (`src/agent_tester.py`)

### `invoke_agent(skill_name: str, input_text: str) -> str`

Test individual agent with input.

**Parameters:**
- `skill_name` (str): Skill name
- `input_text` (str): Text to translate

**Returns:**
- `str`: Translation result

**Example:**
```python
result = invoke_agent("english-to-french-translator", "Hello")
print(result)  # "Bonjour"
```

### `list_agents() -> List[str]`

List all available agent skills.

**Returns:**
- `List[str]`: List of skill names

**Example:**
```python
agents = list_agents()
# ["english-to-french-translator", "french-to-hebrew-translator", ...]
```

---

## Complete Example

```python
import os
from pathlib import Path
import anthropic
from config import Config
from pipeline import load_skill, run_translation_chain
from analysis import analyze_semantic_drift
from cost_tracker import CostTracker

# 1. Setup
os.environ["ANTHROPIC_API_KEY"] = "your-key-here"
config = Config()

# 2. Run translation pipeline
run_translation_chain("Good morning. How are you?", noise_level=25)

# 3. Analyze results
results = analyze_semantic_drift()
print(f"Cosine distance: {results['noise_25']['cosine_distance']}")

# 4. Check costs
# Cost report automatically exported to results/cost_analysis.json
```

---

## Error Handling Best Practices

```python
from errors import *
import logging

logger = logging.getLogger(__name__)

try:
    run_translation_chain(text, noise_level)
except SkillNotFoundError as e:
    logger.error(f"Skill not found: {e}")
    sys.exit(1)
except APIError as e:
    logger.error(f"API call failed: {e}")
    sys.exit(1)
except Exception as e:
    logger.exception("Unexpected error")
    sys.exit(1)
```

---

## Type Hints Reference

```python
from typing import Dict, List, Any, Optional
from pathlib import Path
import numpy as np

# Common types used
SkillDict = Dict[str, str]
MetricsDict = Dict[str, float]
ResultsDict = Dict[str, MetricsDict]
```

---

**For more details, see the source code docstrings.**

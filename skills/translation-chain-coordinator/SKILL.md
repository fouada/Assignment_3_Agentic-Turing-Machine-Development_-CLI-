# Translation Chain Coordinator

## Description
Orchestrator agent that coordinates the multi-agent translation pipeline: English → French → Hebrew → English. Manages the sequential execution of specialized translation agents and measures semantic drift.

## Capabilities
- Orchestrates multi-agent translation chains
- Coordinates between specialized translator agents
- Tracks intermediate outputs at each stage
- Measures semantic drift and preservation
- Handles noisy inputs across the entire pipeline
- Generates analysis reports on translation quality

## When to Use This Skill
- When you need to run the complete translation chain experiment
- When measuring semantic drift across multiple translations
- When testing LLM robustness against noisy inputs
- When coordinating multiple specialized agent skills

## Instructions

### Pipeline Architecture
```
INPUT (English + Noise)
    ↓
[Agent 1: English → French]
    ↓
[Agent 2: French → Hebrew]
    ↓
[Agent 3: Hebrew → English]
    ↓
OUTPUT (English) → Compare with original
```

### Execution Process

1. **Initialize Pipeline**
   - Load the input English text
   - Note the noise level (0%, 10%, 20%, 30%, 40%, 50%)
   - Create output directory structure

2. **Stage 1: English → French**
   - Invoke `english-to-french-translator` skill
   - Pass the noisy English input
   - Save output to `agent1_french.txt`
   - Log timestamp and status

3. **Stage 2: French → Hebrew**
   - Invoke `french-to-hebrew-translator` skill
   - Pass the French output from Stage 1
   - Save output to `agent2_hebrew.txt`
   - Log timestamp and status

4. **Stage 3: Hebrew → English**
   - Invoke `hebrew-to-english-translator` skill
   - Pass the Hebrew output from Stage 2
   - Save output to `agent3_english.txt`
   - Log timestamp and status

5. **Analysis & Reporting**
   - Compare final English output with original input
   - Calculate semantic similarity metrics
   - Generate drift analysis report
   - Save all intermediate outputs

### Directory Structure
```
outputs/
  noise_0/
    agent1_french.txt
    agent2_hebrew.txt
    agent3_english.txt
  noise_10/
    agent1_french.txt
    agent2_hebrew.txt
    agent3_english.txt
  [... other noise levels ...]
```

### Error Handling
- If any agent fails, log the error and stop the pipeline
- If intermediate output is malformed, attempt recovery once
- If unrecoverable, save error state and report failure
- Always save partial results for debugging

### Quality Assurance Checks
At each stage, verify:
- ✓ Output is non-empty
- ✓ Output is in expected language
- ✓ Output length is reasonable (not too short/long)
- ✓ No obvious encoding issues

## Coordination Protocol

### Agent Invocation Format
```python
# Pseudo-code for agent invocation
result = invoke_skill(
    skill_name="english-to-french-translator",
    input_text=input_text,
    context={
        "noise_level": noise_level,
        "original_text": original_clean_text,
        "stage": 1
    }
)
```

### Inter-Agent Communication
- Each agent receives ONLY the output from the previous agent
- No back-propagation of information
- No peek at original text (except for coordinator)
- Simulates real sequential processing

### Experiment Configuration
```yaml
experiment:
  input_text: "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."
  noise_levels: [0, 10, 20, 25, 30, 40, 50]
  output_directory: "./outputs"
  
agents:
  - name: "agent1"
    skill: "english-to-french-translator"
    input: "noisy_english"
    output: "french"
  
  - name: "agent2"
    skill: "french-to-hebrew-translator"
    input: "french"
    output: "hebrew"
  
  - name: "agent3"
    skill: "hebrew-to-english-translator"
    input: "hebrew"
    output: "english"
```

## Metrics Collection

### Per-Stage Metrics
- Processing time
- Output length (characters/words)
- Language detection confidence

### Pipeline Metrics
- Total processing time
- End-to-end semantic similarity
- Word overlap ratio
- Character-level similarity
- TF-IDF cosine distance

### Experiment-Wide Metrics
- Semantic drift vs noise level (graph)
- Best/worst noise levels
- Average preservation rate
- Statistical analysis (mean, median, std dev)

## Output Artifacts

### Generated Files
1. `outputs/noise_X/agent1_french.txt` - French translations
2. `outputs/noise_X/agent2_hebrew.txt` - Hebrew translations
3. `outputs/noise_X/agent3_english.txt` - Final English outputs
4. `analysis_results_local.json` - Quantitative analysis
5. `semantic_drift_analysis_local.png` - Visualization
6. `semantic_drift_analysis_local.pdf` - Publication-ready graph

### Report Format
The coordinator generates a summary report:
```
============================================================
AGENTIC TURING MACHINE - TRANSLATION CHAIN RESULTS
============================================================

Configuration:
- Original Text: [...]
- Noise Levels: 7 levels tested (0% to 50%)
- Agents: 3 (English→French→Hebrew→English)

Results Summary:
- Best Preservation: 10% noise (0.308 distance)
- Worst Preservation: 0% noise (0.407 distance)
- Average Similarity: 98.1%
- Word Overlap: 79-89%

Key Finding:
Moderate noise (10%, 25%, 50%) performed better than clean 
input, demonstrating stochastic resonance in LLM attention
mechanisms.

============================================================
```

## Related Skills
- **Agents**: english-to-french-translator, french-to-hebrew-translator, hebrew-to-english-translator
- **Analysis**: semantic-drift-analyzer (local, no API)
- **Utilities**: noise-injector, language-detector
- **Visualization**: results-grapher, report-generator

## Usage Example

### Via API (Python)
```python
from anthropic import Anthropic

client = Anthropic()

# Load the coordinator skill
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    skills=["translation-chain-coordinator"],
    messages=[{
        "role": "user",
        "content": "Run the translation chain experiment with noise levels 0, 10, 20, 30, 40, 50"
    }]
)
```

### Via CLI
```bash
# Using the shell script wrapper
./run_full_experiment_gemini.sh

# Or with specific noise levels
./run_agent_chain_gemini.sh 25
```

## Performance Expectations
- Single chain (one noise level): ~5-10 seconds
- Full experiment (7 noise levels): ~35-70 seconds
- Analysis generation: ~5 seconds (local, no API)
- Total end-to-end: ~40-75 seconds

## Best Practices
1. **Run full experiments**: Test all noise levels for complete picture
2. **Save all outputs**: Intermediate files enable debugging
3. **Version control**: Track changes to agent skills
4. **Document findings**: Maintain experiment logs
5. **Compare methods**: Test with different LLM providers


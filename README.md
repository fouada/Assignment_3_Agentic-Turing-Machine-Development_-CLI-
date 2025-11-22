# 📚 Task 3: Agentic Turing Machine Development (CLI)

## 🎯 Project Overview

This project implements a multi-stage translation pipeline to test the robustness of the Attention Mechanism in Large Language Models (LLMs). It quantifies how well the system recovers original semantic meaning after text is corrupted with spelling errors.

### Core Concept
The system processes noisy English text through a chain of three sequential agents:
1. **Agent 1 (The Fixer)**: English (noisy) → French
2. **Agent 2 (The Pivot)**: French → Hebrew
3. **Agent 3 (The Restorer)**: Hebrew → English

By comparing the final output with the original clean sentence using vector embeddings, we measure **semantic drift** across different noise levels.

---

## 🧩 System Architecture

### Agent Chain Design

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGENTIC TURING MACHINE                      │
└─────────────────────────────────────────────────────────────────┘

Input: English (with 0-50% spelling errors)
   │
   ↓
┌──────────────────────────────────────────────┐
│  AGENT 1: The Fixer/Filter                  │
│  ----------------------------------------    │
│  Skill: Ignore spelling errors              │
│  Task: Translate intention to French        │
│  Output: Clean grammatical French           │
└──────────────────────────────────────────────┘
   │
   ↓ French Text
   │
┌──────────────────────────────────────────────┐
│  AGENT 2: The Pivot                         │
│  ----------------------------------------    │
│  Skill: French to Hebrew translation        │
│  Task: Maintain semantic meaning            │
│  Output: Fluent Hebrew                      │
└──────────────────────────────────────────────┘
   │
   ↓ Hebrew Text
   │
┌──────────────────────────────────────────────┐
│  AGENT 3: The Restorer                      │
│  ----------------------------------------    │
│  Skill: Hebrew to English translation       │
│  Task: Complete the translation loop        │
│  Output: Reconstructed English              │
└──────────────────────────────────────────────┘
   │
   ↓
Final Output: English (for comparison)
   │
   ↓
┌──────────────────────────────────────────────┐
│  PYTHON ANALYSIS                            │
│  ----------------------------------------    │
│  • Calculate embeddings                     │
│  • Compute cosine distance                  │
│  • Generate visualization                   │
└──────────────────────────────────────────────┘
```

### Implementation Requirements ✅

- ✅ **CLI-Only Orchestration**: Pure shell scripts, NO Python for agent chaining
- ✅ **Sequential Processing**: Output of Agent N becomes input of Agent N+1
- ✅ **System Prompts ("Skills")**: Each agent has a specific role defined in a prompt file
- ✅ **API-Based Execution**: Using OpenAI API via `curl` commands

---

## 📝 Input Data & Experimental Design

### Original Clean Sentence (16 words)
```
The artificial intelligence system can efficiently process natural language 
and understand complex semantic relationships within textual data.
```

### Noise Levels Tested

| Noise Level | Misspelled Words | Example Text |
|-------------|------------------|--------------|
| **0%**      | 0/16            | `The artificial intelligence system can efficiently...` (clean) |
| **10%**     | 2/16            | `The artifical intelligence systm can efficiently...` |
| **20%**     | 3/16            | `The artifical inteligence systm can efficiently proces...` |
| **30%**     | 5/16            | `The artifical inteligence systm can eficiently proces...` |
| **40%**     | 6/16            | `The artifical inteligence systm can eficiently proces naturel...` |
| **50%**     | 8/16            | `The artifical inteligence systm can eficiently proces naturel langauge...` |

**See full input data in**: `input_data.txt`

---

## 🔧 Installation & Setup

### Prerequisites

1. **Operating System**: macOS, Linux, or Windows (with WSL)
2. **Shell**: Bash 4.0+
3. **Required Tools**:
   - `curl` (for API calls)
   - `jq` (for JSON processing)
   - Python 3.7+ (for analysis only)

### Installation Steps

#### Option A: Using UV (Recommended - 10-100x faster) ⚡

```bash
# 1. Navigate to the project directory
cd /path/to/Assignment_3_Agentic_Turing_Machine_Development_(CLI)

# 2. Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install jq (if not already installed)
# macOS:
brew install jq

# Linux (Ubuntu/Debian):
sudo apt-get install jq

# 4. Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# 5. Set your OpenAI API key
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# 6. Make scripts executable
chmod +x run_agent_chain.sh
chmod +x run_full_experiment.sh
```

**See detailed UV setup guide**: [UV_SETUP.md](UV_SETUP.md)

#### Option B: Using Traditional pip

```bash
# 1. Navigate to the project directory
cd /path/to/Assignment_3_Agentic_Turing_Machine_Development_(CLI)

# 2. Install jq (if not already installed)
# macOS:
brew install jq

# Linux (Ubuntu/Debian):
sudo apt-get install jq

# 3. Create virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Set your OpenAI API key
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# 6. Make scripts executable
chmod +x run_agent_chain.sh
chmod +x run_full_experiment.sh
```

---

## 🚀 Usage

### Option 1: Run Full Experiment (All Noise Levels)

```bash
./run_full_experiment.sh
```

This will:
- Execute the agent chain for noise levels: 0%, 10%, 20%, 30%, 40%, 50%
- Save intermediate outputs (French, Hebrew) and final English outputs
- Create an `outputs/` directory structure

### Option 2: Run Single Noise Level

```bash
./run_agent_chain.sh <noise_level> "<input_text>"

# Example:
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."
```

### Option 3: Run Analysis

After running the experiment, analyze the results:

```bash
python3 analyze_results.py
```

This will:
- Calculate embeddings for original and final outputs
- Compute cosine distances (semantic drift)
- Generate visualization graphs
- Save results to `analysis_results.json`

---

## 📊 Results & Analysis

### Vector Distance Calculation

**Method**: Cosine Distance between embeddings
- **Embedding Model**: `text-embedding-3-small` (OpenAI)
- **Distance Metric**: `Cosine Distance = 1 - Cosine Similarity`
- **Range**: 0 (identical) to 2 (completely opposite)

**Formula**:
$$
\text{Cosine Similarity} = \frac{A \cdot B}{\|A\| \|B\|}
$$

$$
\text{Cosine Distance} = 1 - \text{Cosine Similarity}
$$

Where:
- $A$ = Original clean sentence embedding
- $B$ = Final reconstructed sentence embedding

### Expected Output

The analysis generates:

1. **`semantic_drift_analysis.png`**: Visualization of noise % vs. semantic distance
2. **`semantic_drift_analysis.pdf`**: High-quality PDF version
3. **`analysis_results.json`**: Complete results including:
   - Original sentence
   - Final outputs for each noise level
   - Semantic distances
   - Metadata (models used, metrics)

---

## 📁 Project Structure

```
Task_3_Agentic_Turing_Machine_Development_(CLI)/
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
│
├── input_data.txt                 # Original & noisy sentences
│
├── agent1_skill.txt              # System prompt for Agent 1
├── agent2_skill.txt              # System prompt for Agent 2
├── agent3_skill.txt              # System prompt for Agent 3
│
├── run_agent_chain.sh            # Single run CLI script
├── run_full_experiment.sh        # Full experiment CLI script
│
├── analyze_results.py            # Python analysis script
│
├── outputs/                      # Generated outputs (created at runtime)
│   ├── noise_0/
│   │   ├── agent1_french.txt
│   │   ├── agent2_hebrew.txt
│   │   └── agent3_english.txt
│   ├── noise_10/
│   ├── noise_20/
│   ├── noise_30/
│   ├── noise_40/
│   └── noise_50/
│
├── analysis_results.json         # Analysis output
├── semantic_drift_analysis.png   # Graph (PNG)
└── semantic_drift_analysis.pdf   # Graph (PDF)
```

---

## 🔍 CLI Execution Proof

### Example: Running the Agent Chain for 30% Noise

**Command**:
```bash
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."
```

**Expected Output**:
```
========================================
Running Agent Chain - Noise Level: 30%
========================================

>>> Agent 1: Translating English to French...
Input: The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data.
Output: Le système d'intelligence artificielle peut traiter efficacement le langage naturel et comprendre des relations sémantiques complexes dans les données textuelles.

>>> Agent 2: Translating French to Hebrew...
Input: Le système d'intelligence artificielle peut traiter efficacement le langage naturel et comprendre des relations sémantiques complexes dans les données textuelles.
Output: מערכת הבינה המלאכותית יכולה לעבד ביעילות שפה טבעית ולהבין יחסים סמנטיים מורכבים בתוך נתונים טקסטואליים.

>>> Agent 3: Translating Hebrew to English...
Input: מערכת הבינה המלאכותית יכולה לעבד ביעילות שפה טבעית ולהבין יחסים סמנטיים מורכבים בתוך נתונים טקסטואליים.
Output: The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data.

========================================
Agent Chain Complete!
========================================
Results saved to: outputs/noise_30/
========================================
```

### Example: Running Analysis

**Command**:
```bash
python3 analyze_results.py
```

**Expected Output**:
```
============================================================
SEMANTIC DRIFT ANALYSIS
============================================================

Loading final outputs from agent chain...
Loaded 6 outputs

Calculating embedding for original clean sentence...
Original embedding dimension: 1536

Calculating semantic distances...
------------------------------------------------------------
Noise  0%: Distance = 0.000123
  Original: The artificial intelligence system can efficiently proces...
  Final:    The artificial intelligence system can efficiently proces...

Noise 10%: Distance = 0.001456
  Original: The artificial intelligence system can efficiently proces...
  Final:    The artificial intelligence system can efficiently proces...

[... output for other noise levels ...]

------------------------------------------------------------

Generating visualization...
Graph saved to: semantic_drift_analysis.png
Graph saved to: semantic_drift_analysis.pdf
Results saved to: analysis_results.json
============================================================
```

---

## 🎯 Deliverables Checklist

### ✅ Required Deliverables

1. **✅ Input Data**
   - File: `input_data.txt`
   - Contains: Original clean sentence + noisy versions (0%-50%)

2. **✅ Agent Configuration (System Prompts)**
   - `agent1_skill.txt` - The Fixer/Filter
   - `agent2_skill.txt` - The Pivot
   - `agent3_skill.txt` - The Restorer

3. **✅ CLI Execution Scripts**
   - `run_agent_chain.sh` - Single execution
   - `run_full_experiment.sh` - Full experiment
   - Uses only CLI commands (`curl`, `jq`, shell scripting)
   - NO Python for orchestration

4. **✅ Python Analysis Code**
   - `analyze_results.py`
   - Calculates embeddings
   - Computes cosine distances
   - Generates graphs

5. **✅ Documentation**
   - This `README.md` file
   - Complete instructions
   - CLI command examples
   - Architecture diagrams

6. **✅ Visualization** (Generated after running)
   - `semantic_drift_analysis.png`
   - `semantic_drift_analysis.pdf`
   - X-axis: Noise percentage (0%-50%)
   - Y-axis: Vector distance (semantic drift)

---

## 🔬 Technical Implementation Details

### Agent Orchestration (Pure CLI)

Each agent call uses `curl` to interact with the OpenAI API:

```bash
# Example Agent 1 call structure
curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "system",
        "content": "<system_prompt_from_file>"
      },
      {
        "role": "user",
        "content": "<input_text>"
      }
    ],
    "temperature": 0.3,
    "max_tokens": 500
  }'
```

### Data Flow

1. **Shell Script** reads system prompt from file
2. **Shell Script** constructs JSON payload
3. **curl** sends API request
4. **jq** parses JSON response
5. **Shell Script** extracts output and passes to next agent
6. Repeat for all 3 agents

### Analysis Pipeline

1. **Load** final English outputs from `outputs/noise_*/agent3_english.txt`
2. **Embed** original and final texts using OpenAI embeddings API
3. **Calculate** cosine distance for each noise level
4. **Visualize** using matplotlib
5. **Save** results and graphs

---

## 📈 Expected Results & Interpretation

### Hypothesis

The LLM's attention mechanism should demonstrate robustness against noise:
- **Low Noise (0-20%)**: Minimal semantic drift, distance ≈ 0
- **Medium Noise (30-40%)**: Slight increase in drift
- **High Noise (50%)**: Noticeable drift but still reasonable recovery

### Interpreting the Graph

- **Lower Distance** = Better semantic preservation
- **Higher Distance** = More semantic drift
- **Flat Line** = Excellent robustness
- **Steep Increase** = Sensitivity to noise

---

## 🛠️ Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set"**
   ```bash
   export OPENAI_API_KEY='your-key-here'
   ```

2. **"jq: command not found"**
   ```bash
   # macOS
   brew install jq
   
   # Linux
   sudo apt-get install jq
   ```

3. **"Permission denied" when running scripts**
   ```bash
   chmod +x run_agent_chain.sh run_full_experiment.sh
   ```

4. **API rate limits**
   - The script includes 2-second delays between calls
   - Adjust sleep duration in `run_full_experiment.sh` if needed

---

## 🎓 Academic Context

This project demonstrates:

- **Multi-Agent Systems**: Sequential agent orchestration
- **Attention Mechanisms**: Testing LLM robustness to noise
- **Semantic Similarity**: Vector embeddings and distance metrics
- **CLI Programming**: Shell scripting and API interaction
- **Data Analysis**: Python-based scientific computing

---

## 📄 License

This project is created for academic purposes as part of LLMs and Multi-Agent Orchestration coursework.

---

## 👤 Author

Created for Task 3: Agentic Turing Machine Development (CLI)

---

## 🙏 Acknowledgments

- OpenAI API for LLM capabilities
- `jq` for JSON processing in bash
- Python scientific computing stack (numpy, matplotlib, scikit-learn)



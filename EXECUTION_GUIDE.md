# 🎯 COMPLETE PROJECT EXECUTION GUIDE

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Understanding the Agents](#understanding-the-agents)
5. [Step-by-Step Execution](#step-by-step-execution)
6. [Understanding Results](#understanding-results)
7. [Troubleshooting](#troubleshooting)

---

## 🌟 Project Overview

### What This Project Does
This project tests how well Large Language Models (LLMs) preserve semantic meaning when processing text with spelling errors. It uses a **multi-agent translation pipeline** to measure semantic drift.

### The Process
```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: English text with spelling errors (0%-50% noise)   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  AGENT 1: The Fixer                                         │
│  • Receives: Noisy English                                  │
│  • Does: Ignores spelling errors, understands intent        │
│  • Outputs: Clean French translation                        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  AGENT 2: The Pivot                                         │
│  • Receives: French text                                    │
│  • Does: Maintains semantic meaning                         │
│  • Outputs: Hebrew translation                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  AGENT 3: The Restorer                                      │
│  • Receives: Hebrew text                                    │
│  • Does: Completes the translation loop                     │
│  • Outputs: Reconstructed English                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  ANALYSIS: Python script                                    │
│  • Compares original vs final English                       │
│  • Calculates semantic distance using vector embeddings     │
│  • Generates visualization graph                            │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics
- **Input**: 16-word English sentence
- **Noise Levels**: 0%, 10%, 20%, 30%, 40%, 50%
- **Measurement**: Cosine distance between embeddings
- **Output**: Graph showing semantic drift vs. noise level

---

## 🔧 Prerequisites

### Required Software
1. **Operating System**: macOS, Linux, or Windows with WSL
2. **Shell**: Bash 4.0+
3. **Command-line Tools**:
   - `curl` (HTTP client for API calls)
   - `jq` (JSON processor)
4. **Python**: 3.7 or higher
5. **OpenAI API Key**: Active API key from OpenAI

### Required Knowledge
- Basic command-line usage
- Understanding of environment variables
- Familiarity with running shell scripts

---

## 🚀 Setup Instructions

### STEP 1: Navigate to Project Directory

```bash
cd "/Users/fouadaz/LearningFromUniversity/Learning/LLMSAndMultiAgentOrchestration/course-materials/assignments/Assignment_3_Agentic Turing Machine Development_(CLI)"
```

### STEP 2: Install System Dependencies

#### On macOS:
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install jq
brew install jq

# Verify installation
jq --version
# Expected output: jq-1.6 or similar
```

#### On Linux (Ubuntu/Debian):
```bash
# Update package list
sudo apt-get update

# Install jq
sudo apt-get install jq

# Verify installation
jq --version
```

### STEP 3: Install Python Dependencies

#### Option A: Using UV (Recommended - Faster)
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

#### Option B: Using Traditional pip
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### STEP 4: Set OpenAI API Key

```bash
# Set API key for current session
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# Verify it's set
echo $OPENAI_API_KEY
```

**💡 Tip: Make it Permanent**
```bash
# Add to your shell configuration file
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.zshrc  # For zsh
# OR
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.bashrc  # For bash

# Reload configuration
source ~/.zshrc  # or source ~/.bashrc
```

### STEP 5: Make Scripts Executable

```bash
chmod +x verify_setup.sh
chmod +x run_agent_chain.sh
chmod +x run_full_experiment.sh
```

### STEP 6: Verify Setup

```bash
./verify_setup.sh
```

**Expected Output:**
```
========================================
SETUP VERIFICATION
========================================

✓ jq installed (version 1.6)
✓ curl installed
✓ Python 3.11.14 installed
✓ OpenAI API key is set
✓ All agent skill files present
✓ Scripts are executable
✓ Python packages installed

========================================
✓ ALL CHECKS PASSED!
========================================

You're ready to run the experiment!
```

---

## 🤖 Understanding the Agents

### What is an Agent?

In this project, an **agent** consists of:
1. **System Prompt (Skill File)**: A text file defining the agent's role and instructions
2. **API Call**: Using `curl` to send requests to OpenAI's API
3. **JSON Processing**: Using `jq` to parse responses

### Agent 1: The Fixer

**File**: `agent1_skill.txt`

**Role**: English (with spelling errors) → French

**Key Capabilities**:
- Ignores spelling errors
- Infers correct meaning from context
- Translates the *intention* rather than literal text
- Produces grammatically correct French

**Example System Prompt Structure**:
```
You are Agent 1: The Fixer/Filter

Your role is to translate noisy English text to French.

CRITICAL INSTRUCTIONS:
1. You will receive English text that may contain spelling errors
2. Use context to infer the correct intended meaning
3. Translate the INTENTION (not literal text) into fluent French
4. Output ONLY the French translation - no explanations
```

### Agent 2: The Pivot

**File**: `agent2_skill.txt`

**Role**: French → Hebrew

**Key Capabilities**:
- Direct translation from French to Hebrew
- Maintains semantic meaning
- Produces fluent, natural Hebrew

**Example System Prompt Structure**:
```
You are Agent 2: The Pivot

Your role is to translate French text to Hebrew.

CRITICAL INSTRUCTIONS:
1. You will receive French text
2. Translate it accurately into Hebrew
3. Maintain all semantic meaning
4. Output ONLY the Hebrew translation - no explanations
```

### Agent 3: The Restorer

**File**: `agent3_skill.txt`

**Role**: Hebrew → English

**Key Capabilities**:
- Completes the translation loop
- Converts Hebrew back to English
- Preserves semantic content

**Example System Prompt Structure**:
```
You are Agent 3: The Restorer

Your role is to translate Hebrew text to English.

CRITICAL INSTRUCTIONS:
1. You will receive Hebrew text
2. Translate it accurately into English
3. Preserve all semantic meaning
4. Output ONLY the English translation - no explanations
```

### How Agents Are Created

**Step 1: Create the Skill File**
```bash
# Create a new agent skill file
cat > agent1_skill.txt << 'EOF'
You are Agent 1: The Fixer/Filter
[... instructions ...]
EOF
```

**Step 2: The Script Reads the Skill File**
```bash
# In run_agent_chain.sh
AGENT1_PROMPT=$(cat agent1_skill.txt)
```

**Step 3: Script Constructs JSON Payload**
```bash
AGENT1_PAYLOAD=$(cat <<EOF
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": $(echo "$AGENT1_PROMPT" | jq -Rs .)},
    {"role": "user", "content": $(echo "$INPUT_TEXT" | jq -Rs .)}
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
EOF
)
```

**Step 4: Script Makes API Call**
```bash
AGENT1_RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "$AGENT1_PAYLOAD")
```

**Step 5: Script Extracts Output**
```bash
FRENCH_OUTPUT=$(echo "$AGENT1_RESPONSE" | jq -r '.choices[0].message.content')
```

**Step 6: Output Becomes Input for Next Agent**
```bash
# Agent 1's output (French) → Agent 2's input
AGENT2_PAYLOAD=$(cat <<EOF
{
  "messages": [
    {"role": "system", "content": $(echo "$AGENT2_PROMPT" | jq -Rs .)},
    {"role": "user", "content": $(echo "$FRENCH_OUTPUT" | jq -Rs .)}
  ]
}
EOF
)
```

---

## 📝 Step-by-Step Execution

### 🎯 Method 1: Quick Run (Recommended for First Time)

#### STEP 1: Run Verification
```bash
./verify_setup.sh
```
✅ Ensure all checks pass before proceeding

#### STEP 2: Test Single Execution (Optional but Recommended)
```bash
# Test with 0% noise (clean text)
./run_agent_chain.sh 0 "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."
```

**What to Expect:**
- Script will print progress for each agent
- You'll see the input and output for each translation step
- Takes about 10-15 seconds
- Creates `outputs/noise_0/` directory with results

#### STEP 3: Run Full Experiment
```bash
./run_full_experiment.sh
```

**What Happens:**
- Runs the agent chain 6 times (for noise levels: 0%, 10%, 20%, 30%, 40%, 50%)
- Each run takes 10-15 seconds
- Total time: 2-3 minutes
- Creates 6 output directories under `outputs/`

**Expected Console Output:**
```
========================================
AGENTIC TURING MACHINE - FULL EXPERIMENT
========================================

This will run the agent chain for noise levels: 0%, 10%, 20%, 30%, 40%, 50%
Estimated time: 2-3 minutes
Total API calls: 18 (3 per noise level)

========================================
Running Experiment 1/6: Noise Level 0%
========================================

>>> Agent 1: Translating English to French...
Input: The artificial intelligence system...
Output: Le système d'intelligence artificielle...

>>> Agent 2: Translating French to Hebrew...
Input: Le système d'intelligence artificielle...
Output: מערכת הבינה המלאכותית...

>>> Agent 3: Translating Hebrew to English...
Input: מערכת הבינה המלאכותית...
Output: The artificial intelligence system...

[... continues for other noise levels ...]

========================================
EXPERIMENT COMPLETE!
========================================
```

#### STEP 4: Analyze Results
```bash
python analyze_results.py
```

**What Happens:**
- Reads all final outputs from `outputs/noise_*/agent3_english.txt`
- Calculates embeddings using OpenAI API
- Computes cosine distance for each noise level
- Generates visualization graphs
- Saves detailed results

**Expected Console Output:**
```
============================================================
SEMANTIC DRIFT ANALYSIS
============================================================

Loading final outputs from agent chain...
Loaded 6 outputs (noise levels: 0, 10, 20, 30, 40, 50)

Calculating embedding for original clean sentence...
Original embedding dimension: 1536

Calculating semantic distances...
------------------------------------------------------------
Noise  0%: Distance = 0.000123
  Original: The artificial intelligence system can efficiently process...
  Final:    The artificial intelligence system can efficiently process...

Noise 10%: Distance = 0.001456
  Original: The artificial intelligence system can efficiently process...
  Final:    The artificial intelligence system can efficiently process...

[... continues for all noise levels ...]

------------------------------------------------------------

Generating visualization...
Graph saved to: semantic_drift_analysis.png
Graph saved to: semantic_drift_analysis.pdf
Results saved to: analysis_results.json

============================================================
ANALYSIS COMPLETE!
============================================================
```

#### STEP 5: View Results
```bash
# View the graph
open semantic_drift_analysis.png      # On macOS
# OR
xdg-open semantic_drift_analysis.png  # On Linux

# View detailed JSON results
cat analysis_results.json | jq .

# Browse output directory
ls -R outputs/
```

---

### 🎯 Method 2: Manual Step-by-Step (For Understanding)

#### STEP 1: Examine Input Data
```bash
# View the input sentences
cat input_data.txt
```

**You'll See:**
- Original clean sentence (16 words)
- 6 versions with different noise levels (0%-50%)
- Each misspelled word clearly visible

#### STEP 2: Examine Agent Skills
```bash
# View Agent 1's instructions
cat agent1_skill.txt

# View Agent 2's instructions
cat agent2_skill.txt

# View Agent 3's instructions
cat agent3_skill.txt
```

#### STEP 3: Run Individual Noise Levels

**Test with 0% Noise (Clean):**
```bash
./run_agent_chain.sh 0 "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."
```

**Test with 30% Noise:**
```bash
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."
```

**Test with 50% Noise:**
```bash
./run_agent_chain.sh 50 "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships withn textul data."
```

#### STEP 4: Examine Intermediate Outputs

After each run, check the results:

```bash
# For 30% noise level:
echo "=== Agent 1 Output (French) ==="
cat outputs/noise_30/agent1_french.txt

echo "=== Agent 2 Output (Hebrew) ==="
cat outputs/noise_30/agent2_hebrew.txt

echo "=== Agent 3 Output (Final English) ==="
cat outputs/noise_30/agent3_english.txt
```

#### STEP 5: Compare Original vs Final

```bash
# View original
echo "Original:"
head -2 input_data.txt | tail -1

# View final output for each noise level
echo "Final (0% noise):"
cat outputs/noise_0/agent3_english.txt

echo "Final (50% noise):"
cat outputs/noise_50/agent3_english.txt
```

#### STEP 6: Run Analysis
```bash
python analyze_results.py
```

#### STEP 7: Interpret Results

```bash
# View the graph
open semantic_drift_analysis.png

# View detailed metrics
cat analysis_results.json | jq '.semantic_distances'
```

---

### 🎯 Method 3: Custom Execution

#### Run Specific Noise Levels Only

**Option 1: Create a Custom Script**
```bash
cat > run_custom.sh << 'EOF'
#!/bin/bash

# Run only 0%, 20%, and 40% noise levels
./run_agent_chain.sh 0 "$(grep 'NOISE_0:' input_data.txt | cut -d':' -f2-)"
sleep 2
./run_agent_chain.sh 20 "$(grep 'NOISE_20:' input_data.txt | cut -d':' -f2-)"
sleep 2
./run_agent_chain.sh 40 "$(grep 'NOISE_40:' input_data.txt | cut -d':' -f2-)"

echo "Custom experiment complete!"
EOF

chmod +x run_custom.sh
./run_custom.sh
```

#### Run with Different Input Text

```bash
# Use your own sentence
./run_agent_chain.sh 30 "Your custm sentense with som spelling erors for testing purposs."
```

---

## 📊 Understanding Results

### Output Directory Structure

After running the experiment, you'll have:

```
outputs/
├── noise_0/
│   ├── agent1_french.txt    (French translation)
│   ├── agent2_hebrew.txt    (Hebrew translation)
│   └── agent3_english.txt   (Final English - for comparison)
├── noise_10/
│   ├── agent1_french.txt
│   ├── agent2_hebrew.txt
│   └── agent3_english.txt
├── noise_20/
│   └── ...
├── noise_30/
│   └── ...
├── noise_40/
│   └── ...
└── noise_50/
    └── ...
```

### Analysis Output Files

```
semantic_drift_analysis.png    (Visualization graph - 300 DPI)
semantic_drift_analysis.pdf    (Publication-quality PDF)
analysis_results.json          (Detailed metrics)
```

### Understanding the Graph

**X-Axis**: Percentage of spelling errors (0% → 50%)
**Y-Axis**: Semantic distance (cosine distance)

**Interpretation:**
- **Lower distance** = Better semantic preservation
- **Higher distance** = More semantic drift
- **Flat line** = Excellent LLM robustness
- **Steep increase** = Sensitivity to noise

**Expected Pattern:**
```
Distance
   ↑
   |     *  *  (Gradual increase or flat)
   |  *
   | *
   +----------------------→ Noise %
   0%  10%  20%  30%  40%  50%
```

### Reading the JSON Results

```bash
cat analysis_results.json | jq .
```

**Structure:**
```json
{
  "original_sentence": "The artificial intelligence system...",
  "final_outputs": {
    "0": "The artificial intelligence system...",
    "10": "The artificial intelligence system...",
    "20": "...",
    "30": "...",
    "40": "...",
    "50": "..."
  },
  "semantic_distances": {
    "0": 0.000123,
    "10": 0.001456,
    "20": 0.002789,
    "30": 0.004012,
    "40": 0.005234,
    "50": 0.006789
  },
  "embedding_model": "text-embedding-3-small",
  "distance_metric": "cosine_distance",
  "metadata": {
    "timestamp": "2025-11-23T...",
    "total_experiments": 6
  }
}
```

### Key Metrics Explained

#### Cosine Distance
```
Cosine Distance = 1 - Cosine Similarity

Where:
- Cosine Similarity = (A · B) / (||A|| × ||B||)
- A = Original sentence embedding (1536-dimensional vector)
- B = Final sentence embedding (1536-dimensional vector)
```

**Range:**
- 0.00 = Identical meaning (perfect preservation)
- 0.10 = Very similar (excellent preservation)
- 0.20 = Similar (good preservation)
- 0.50+ = Different meaning (poor preservation)

---

## 🛠️ Troubleshooting

### Issue 1: "OPENAI_API_KEY not set"

**Symptom:**
```
Error: OPENAI_API_KEY environment variable not set
```

**Solution:**
```bash
export OPENAI_API_KEY='sk-your-actual-key-here'
```

**Verify:**
```bash
echo $OPENAI_API_KEY
```

---

### Issue 2: "jq: command not found"

**Symptom:**
```
./run_agent_chain.sh: line 77: jq: command not found
```

**Solution:**
```bash
# On macOS:
brew install jq

# On Linux:
sudo apt-get install jq
```

**Verify:**
```bash
jq --version
```

---

### Issue 3: "Permission denied"

**Symptom:**
```
-bash: ./run_agent_chain.sh: Permission denied
```

**Solution:**
```bash
chmod +x run_agent_chain.sh
chmod +x run_full_experiment.sh
chmod +x verify_setup.sh
```

**Verify:**
```bash
ls -lh *.sh
# Should show: -rwxr-xr-x (x means executable)
```

---

### Issue 4: API Returns "null" or Empty Output

**Symptom:**
Agent output is "null" or empty

**Possible Causes:**
1. Invalid API key
2. Rate limit exceeded
3. Malformed JSON payload
4. Network issues

**Solutions:**

**Test API Key:**
```bash
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq .
```

**Check API Response:**
```bash
# Add debug mode to script
# Edit run_agent_chain.sh and add: set -x
```

**Increase Delay Between Calls:**
```bash
# Edit run_full_experiment.sh
# Change: sleep 2
# To: sleep 5
```

---

### Issue 5: Python Packages Missing

**Symptom:**
```
ModuleNotFoundError: No module named 'openai'
```

**Solution:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Install/reinstall packages
pip install -r requirements.txt
```

**Verify:**
```bash
python3 -c "import openai, numpy, matplotlib, sklearn; print('All packages OK!')"
```

---

### Issue 6: Graph Not Generated

**Symptom:**
No `semantic_drift_analysis.png` file

**Possible Causes:**
1. Missing `outputs/` directory
2. Missing final output files
3. Matplotlib backend issues

**Solutions:**

**Check Outputs Exist:**
```bash
ls -R outputs/
# Should see: noise_0/, noise_10/, ..., noise_50/
# Each should contain: agent3_english.txt
```

**Run Experiment First:**
```bash
./run_full_experiment.sh
```

**Check Matplotlib:**
```bash
python3 -c "import matplotlib; print(matplotlib.get_backend())"
```

---

### Issue 7: Rate Limit Errors

**Symptom:**
```
Error: Rate limit exceeded
```

**Solution:**
```bash
# Increase delay in run_full_experiment.sh
# Edit the file and change sleep duration:
sleep 5  # Instead of sleep 2
```

---

## 📈 Expected Cost

### OpenAI API Usage

**Experiment Execution:**
- 6 noise levels × 3 agents = 18 API calls
- Model: `gpt-4o-mini`
- Estimated cost: ~$0.10

**Analysis:**
- 7 embedding calls (1 original + 6 final outputs)
- Model: `text-embedding-3-small`
- Estimated cost: ~$0.005

**Total Estimated Cost:** Less than $0.15 per complete run

---

## 🎓 What You're Learning

This project demonstrates:

1. ✅ **Multi-Agent Systems**
   - Sequential agent orchestration
   - Agent chaining and data flow
   - Role-based agent design

2. ✅ **CLI Programming**
   - Bash scripting for automation
   - JSON processing with `jq`
   - HTTP API calls with `curl`

3. ✅ **API Integration**
   - RESTful API interaction
   - Authentication and authorization
   - Error handling and retries

4. ✅ **Semantic Analysis**
   - Vector embeddings
   - Cosine distance/similarity
   - Semantic drift measurement

5. ✅ **LLM Testing**
   - Robustness to noisy input
   - Attention mechanism evaluation
   - Translation chain integrity

---

## 📚 Additional Resources

### Documentation Files
- `README.md` - Complete project documentation
- `CLI_AGENT_GUIDE.md` - Detailed CLI agent tutorial
- `DELIVERABLES.md` - Requirements checklist
- `QUICKSTART.md` - 5-minute setup guide
- `CLI_EXECUTION_EXAMPLES.md` - Command examples

### External Resources
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [jq Manual](https://stedolan.github.io/jq/manual/)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)

---

## ✅ Quick Reference Checklist

### Before Starting
- [ ] Python 3.7+ installed
- [ ] `jq` installed
- [ ] `curl` available
- [ ] OpenAI API key obtained
- [ ] Project directory downloaded

### Setup
- [ ] Navigated to project directory
- [ ] Installed Python dependencies
- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Made scripts executable (`chmod +x`)
- [ ] Ran `./verify_setup.sh` successfully

### Execution
- [ ] Ran `./run_full_experiment.sh`
- [ ] All 6 noise levels completed
- [ ] Outputs generated in `outputs/` directory
- [ ] Ran `python analyze_results.py`
- [ ] Graph generated successfully

### Verification
- [ ] Viewed `semantic_drift_analysis.png`
- [ ] Reviewed `analysis_results.json`
- [ ] Examined intermediate outputs
- [ ] Results make sense

---

## 🎉 You're Ready!

### Quick Start Commands (Copy-Paste)

```bash
# 1. Set API key (replace with your key)
export OPENAI_API_KEY='sk-your-key-here'

# 2. Verify setup
./verify_setup.sh

# 3. Run experiment
./run_full_experiment.sh

# 4. Analyze results
python analyze_results.py

# 5. View graph
open semantic_drift_analysis.png
```

---

**Last Updated:** November 23, 2025  
**Project:** Agentic Turing Machine Development (CLI)  
**Version:** 1.0

**Happy Experimenting! 🚀✨**


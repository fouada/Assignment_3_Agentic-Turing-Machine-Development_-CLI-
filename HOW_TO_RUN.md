# 🚀 HOW TO RUN AGENTS VIA CLI

## ✅ Setup Status

```
✅ jq installed (JSON processor)
✅ curl installed (API client)
✅ Python 3.11.14 installed
✅ All dependencies installed (31 packages via UV)
✅ All agent skill files ready
✅ Scripts are executable
⚠️  ONLY MISSING: OpenAI API Key
```

---

## 🎯 Step-by-Step Instructions

### Step 1: Set Your OpenAI API Key

```bash
export OPENAI_API_KEY='sk-your-actual-api-key-here'
```

> **Note:** You'll need to do this every time you open a new terminal session.

### Step 2: Verify Setup

```bash
./verify_setup.sh
```

You should see: `✓ ALL CHECKS PASSED!`

### Step 3: Run Your First Agent Chain!

```bash
# Test with 0% noise (clean text)
./run_agent_chain.sh 0 "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."
```

**What happens:**
1. 🤖 **Agent 1** receives noisy English → outputs clean French
2. 🤖 **Agent 2** receives French → outputs Hebrew
3. 🤖 **Agent 3** receives Hebrew → outputs reconstructed English

**Output will look like:**

```
========================================
Running Agent Chain - Noise Level: 0%
========================================

>>> Agent 1: Translating English to French...
Input: The artificial intelligence system can efficiently...
Output: Le système d'intelligence artificielle peut traiter...

>>> Agent 2: Translating French to Hebrew...
Input: Le système d'intelligence artificielle peut traiter...
Output: מערכת הבינה המלאכותית יכולה לעבד...

>>> Agent 3: Translating Hebrew to English...
Input: מערכת הבינה המלאכותית יכולה לעבד...
Output: The artificial intelligence system can efficiently...

========================================
Agent Chain Complete!
========================================
Results saved to: outputs/noise_0/
```

---

## 🧪 Step 4: Test Different Noise Levels

### 10% Noise (2 misspelled words)
```bash
./run_agent_chain.sh 10 "The artifical intelligence systm can efficiently process natural language and understand complex semantic relationships within textual data."
```

### 30% Noise (5 misspelled words)
```bash
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."
```

### 50% Noise (8 misspelled words)
```bash
./run_agent_chain.sh 50 "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships withn textul data."
```

---

## 🎬 Step 5: Run Full Experiment (All Noise Levels)

```bash
./run_full_experiment.sh
```

This runs the agent chain automatically for all 6 noise levels:
- 0% (clean)
- 10%
- 20%
- 30%
- 40%
- 50%

**Time:** ~2-3 minutes (18 API calls total)

---

## 📊 Step 6: Analyze Results

```bash
# Make sure UV environment is activated
source .venv/bin/activate

# Run analysis
python analyze_results.py
```

**This creates:**
- `analysis_results.json` - Detailed results
- `semantic_drift_analysis.png` - Visualization graph
- `semantic_drift_analysis.pdf` - High-quality PDF

### View the graph:
```bash
open semantic_drift_analysis.png
```

---

## 📂 Understanding the Output

### Directory Structure After Running

```
outputs/
├── noise_0/
│   ├── agent1_french.txt    ← Agent 1 output
│   ├── agent2_hebrew.txt    ← Agent 2 output
│   └── agent3_english.txt   ← Agent 3 output (final)
├── noise_10/
│   ├── agent1_french.txt
│   ├── agent2_hebrew.txt
│   └── agent3_english.txt
├── noise_20/
├── noise_30/
├── noise_40/
└── noise_50/
```

### View Results

```bash
# View all outputs for 30% noise
cat outputs/noise_30/agent1_french.txt
cat outputs/noise_30/agent2_hebrew.txt
cat outputs/noise_30/agent3_english.txt

# Compare original vs final
echo "Original: The artificial intelligence system..."
cat outputs/noise_30/agent3_english.txt
```

---

## 🤖 How The Agents Work

### Agent 1: The Fixer (agent1_skill.txt)
```
Role: English (noisy) → French
Skill: Ignores spelling errors, understands intent
Model: gpt-4o-mini
Temperature: 0.3
```

### Agent 2: The Pivot (agent2_skill.txt)
```
Role: French → Hebrew
Skill: Maintains semantic meaning
Model: gpt-4o-mini
Temperature: 0.3
```

### Agent 3: The Restorer (agent3_skill.txt)
```
Role: Hebrew → English
Skill: Completes translation loop
Model: gpt-4o-mini
Temperature: 0.3
```

---

## 🛠️ Creating a Custom Agent

### Example: Add Agent 4 (Summarizer)

**Step 1:** Create the skill file
```bash
cat > agent4_skill.txt << 'EOF'
You are Agent 4: The Summarizer.

Your role is to create a concise summary.

CRITICAL INSTRUCTIONS:
1. Read the English text
2. Extract the main idea
3. Produce a 1-sentence summary
4. No explanations
EOF
```

**Step 2:** Add to your script
```bash
# In run_agent_chain.sh, add after Agent 3:

AGENT4_PROMPT=$(cat agent4_skill.txt)
AGENT4_PAYLOAD=$(cat <<EOF
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": $(echo "$AGENT4_PROMPT" | jq -Rs .)},
    {"role": "user", "content": $(echo "$FINAL_ENGLISH" | jq -Rs .)}
  ],
  "temperature": 0.3,
  "max_tokens": 100
}
EOF
)

AGENT4_RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$AGENT4_PAYLOAD")

SUMMARY=$(echo "$AGENT4_RESPONSE" | jq -r '.choices[0].message.content')
echo "$SUMMARY" > "$OUTPUT_DIR/agent4_summary.txt"
```

---

## 💡 Key Concepts

### 1. Agent = System Prompt + API Call

An "agent" is simply:
- A **system prompt** (text file defining the role)
- An **API call** to OpenAI (via curl)
- **JSON processing** (via jq)

### 2. Agent Chaining

```
Agent1 Output → Agent2 Input → Agent3 Input → Final Output
```

Each agent's output becomes the next agent's input.

### 3. CLI Tools

- **bash** - Orchestration & scripting
- **curl** - HTTP API calls
- **jq** - JSON parsing
- **cat/echo** - File/string manipulation

---

## 📋 Complete Workflow Checklist

```bash
# ✅ One-time setup (already done!)
cd "/Users/fouadaz/LearningFromUniversity/Learning/LLMSAndMultiAgentOrchestration/course-materials/assignments/Assignment_3_Agentic Turing Machine Development_(CLI)"
source .venv/bin/activate

# ⚠️ Every session (do this now!)
export OPENAI_API_KEY='sk-your-key-here'

# ✅ Verify setup
./verify_setup.sh

# 🚀 Run experiment
./run_full_experiment.sh

# 📊 Analyze
python analyze_results.py

# 👀 View results
open semantic_drift_analysis.png
ls -R outputs/
```

---

## 🎓 What You're Learning

This project teaches:

✅ **Multi-Agent Systems** - Sequential agent orchestration  
✅ **CLI Programming** - Bash scripting for AI workflows  
✅ **API Integration** - RESTful API calls with curl  
✅ **Data Processing** - JSON parsing with jq  
✅ **Semantic Analysis** - Vector embeddings & distance metrics  
✅ **LLM Testing** - Robustness to noisy input  

---

## 🐛 Common Issues & Solutions

### Issue: "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

### Issue: "jq: command not found"
```bash
brew install jq
```

### Issue: "Permission denied"
```bash
chmod +x run_agent_chain.sh run_full_experiment.sh verify_setup.sh
```

### Issue: API returns error
```bash
# Check your API key is valid
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq .
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **HOW_TO_RUN.md** (this file) | Quick start guide |
| **CLI_AGENT_GUIDE.md** | Complete CLI agent tutorial |
| **QUICK_REFERENCE.md** | Command cheat sheet |
| **QUICK_START_UV.md** | UV package manager guide |
| **README.md** | Full project documentation |

---

## 🚀 Ready to Go!

**You now know how to:**
1. ✅ Create agents (skill files + API calls)
2. ✅ Run agents via CLI (bash + curl + jq)
3. ✅ Chain multiple agents sequentially
4. ✅ Test with different noise levels
5. ✅ Analyze semantic drift
6. ✅ Create custom agents

**Next step:** Set your API key and run your first agent chain!

```bash
export OPENAI_API_KEY='sk-your-key-here'
./run_agent_chain.sh 30 "The artifical inteligence systm works well"
```

---

**Happy agent building!** 🤖✨


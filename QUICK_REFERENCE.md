# ⚡ Quick Reference - Running Agents via CLI

## 🎯 Common Commands

### Setup (One Time)
```bash
# 1. Navigate to project
cd "/Users/fouadaz/LearningFromUniversity/Learning/LLMSAndMultiAgentOrchestration/course-materials/assignments/Assignment_3_Agentic Turing Machine Development_(CLI)"

# 2. Activate UV environment
source .venv/bin/activate

# 3. Set API key (do this every new terminal session)
export OPENAI_API_KEY='sk-your-key-here'

# 4. Verify setup
./verify_setup.sh
```

### Run Agents (Daily Use)

```bash
# Run single agent chain (30% noise)
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."

# Run all noise levels (0%, 10%, 20%, 30%, 40%, 50%)
./run_full_experiment.sh

# Analyze results and create graph
python analyze_results.py

# View the results
open semantic_drift_analysis.png
```

## 🤖 What Are The Agents?

| Agent | Input | Output | Role |
|-------|-------|--------|------|
| **Agent 1** | English (noisy) | French | Fixes spelling, translates to French |
| **Agent 2** | French | Hebrew | Translates French to Hebrew |
| **Agent 3** | Hebrew | English | Translates back to English |

## 📂 Where Are The Agents Defined?

```
agent1_skill.txt  ← Agent 1's instructions (system prompt)
agent2_skill.txt  ← Agent 2's instructions (system prompt)
agent3_skill.txt  ← Agent 3's instructions (system prompt)
```

## 🧪 Test Input Data (from input_data.txt)

```bash
# 0% Noise (Clean)
./run_agent_chain.sh 0 "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."

# 10% Noise
./run_agent_chain.sh 10 "The artifical intelligence systm can efficiently process natural language and understand complex semantic relationships within textual data."

# 30% Noise
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."

# 50% Noise
./run_agent_chain.sh 50 "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships withn textul data."
```

## 📊 View Results

```bash
# List all outputs
ls -R outputs/

# View specific agent output
cat outputs/noise_30/agent1_french.txt
cat outputs/noise_30/agent2_hebrew.txt
cat outputs/noise_30/agent3_english.txt

# View analysis
cat analysis_results.json | jq .
```

## 🔧 Manual Agent Call (Advanced)

```bash
# Call a single agent directly
curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "system",
        "content": "You are a translator. Translate English to French."
      },
      {
        "role": "user",
        "content": "Hello world"
      }
    ],
    "temperature": 0.3,
    "max_tokens": 500
  }' | jq -r '.choices[0].message.content'
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `OPENAI_API_KEY not set` | `export OPENAI_API_KEY='sk-...'` |
| `jq: command not found` | `brew install jq` |
| `Permission denied` | `chmod +x *.sh` |
| `No such file or directory` | Check you're in the right directory |

## 📚 Documentation Files

- **CLI_AGENT_GUIDE.md** - Complete guide for creating agents
- **QUICK_START_UV.md** - UV setup quick start
- **README.md** - Full project documentation
- **CLI_EXECUTION_EXAMPLES.md** - More examples

---

**Need help?** Read the full guide: `CLI_AGENT_GUIDE.md`


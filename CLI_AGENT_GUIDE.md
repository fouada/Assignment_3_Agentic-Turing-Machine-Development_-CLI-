# 🤖 CLI Agent Creation & Execution Guide

## Overview

This guide shows you how to create and execute AI agents using **pure CLI commands** (bash + curl + jq). No Python orchestration - just shell scripting!

---

## 🏗️ Agent Architecture

Your project uses a **3-agent sequential pipeline**:

```
┌─────────────────────────────────────────────────┐
│  Input: Noisy English Text                     │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  AGENT 1: The Fixer                            │
│  Role: English (noisy) → French                │
│  Skill: Ignore spelling errors                 │
│  File: agent1_skill.txt                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  AGENT 2: The Pivot                            │
│  Role: French → Hebrew                         │
│  Skill: Maintain semantic meaning             │
│  File: agent2_skill.txt                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  AGENT 3: The Restorer                         │
│  Role: Hebrew → English                        │
│  Skill: Complete translation loop              │
│  File: agent3_skill.txt                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  Output: Reconstructed English Text            │
└─────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### 1. Install Required Tools

```bash
# Check if jq is installed (JSON processor)
jq --version

# If not installed:
# macOS:
brew install jq

# Linux:
sudo apt-get install jq

# Check if curl is installed (HTTP client)
curl --version
```

### 2. Set OpenAI API Key

```bash
# Set your API key (required for each terminal session)
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# Verify it's set
echo $OPENAI_API_KEY
```

### 3. Make Scripts Executable

```bash
cd "/Users/fouadaz/LearningFromUniversity/Learning/LLMSAndMultiAgentOrchestration/course-materials/assignments/Assignment_3_Agentic Turing Machine Development_(CLI)"

chmod +x run_agent_chain.sh
chmod +x run_full_experiment.sh
chmod +x verify_setup.sh
```

---

## 🎯 Method 1: Using Existing Scripts (Easiest)

### Run Single Agent Chain

```bash
# Syntax:
./run_agent_chain.sh <noise_level> "<input_text>"

# Example: Test with 0% noise (clean text)
./run_agent_chain.sh 0 "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."

# Example: Test with 30% noise
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."

# Example: Test with 50% noise
./run_agent_chain.sh 50 "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships withn textul data."
```

### Run Full Experiment (All Noise Levels)

```bash
# This runs the agent chain for 0%, 10%, 20%, 30%, 40%, 50% noise
./run_full_experiment.sh
```

---

## 🛠️ Method 2: Manual CLI Execution (Understanding How It Works)

### Step 1: Define Your Agent's "Skill" (System Prompt)

Create a text file with the agent's instructions:

```bash
# Example: Create a new agent
cat > my_agent_skill.txt << 'EOF'
You are a helpful translation agent.
Your role is to translate English to Spanish.

CRITICAL INSTRUCTIONS:
1. You will receive English text as input
2. Translate it into fluent, grammatically correct Spanish
3. Maintain all semantic meaning
4. Produce only the Spanish translation - no explanations
EOF
```

### Step 2: Call the Agent via curl + OpenAI API

```bash
# Set variables
API_KEY="$OPENAI_API_KEY"
API_URL="https://api.openai.com/v1/chat/completions"
MODEL="gpt-4o-mini"

# Read the agent's skill/prompt
AGENT_SKILL=$(cat my_agent_skill.txt)

# The input text
INPUT_TEXT="Hello, how are you today?"

# Create JSON payload
PAYLOAD=$(cat <<EOF
{
  "model": "$MODEL",
  "messages": [
    {
      "role": "system",
      "content": $(echo "$AGENT_SKILL" | jq -Rs .)
    },
    {
      "role": "user",
      "content": $(echo "$INPUT_TEXT" | jq -Rs .)
    }
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
EOF
)

# Call the API
RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$PAYLOAD")

# Extract the agent's output
OUTPUT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content')

# Display result
echo "Agent Output: $OUTPUT"

# Save to file
echo "$OUTPUT" > agent_output.txt
```

### Step 3: Chain Multiple Agents

```bash
# Agent 1: English → French
AGENT1_SKILL=$(cat agent1_skill.txt)
INPUT="The artifical system works well"

AGENT1_PAYLOAD=$(cat <<EOF
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": $(echo "$AGENT1_SKILL" | jq -Rs .)},
    {"role": "user", "content": $(echo "$INPUT" | jq -Rs .)}
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
EOF
)

AGENT1_RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "$AGENT1_PAYLOAD")

FRENCH_OUTPUT=$(echo "$AGENT1_RESPONSE" | jq -r '.choices[0].message.content')
echo "French: $FRENCH_OUTPUT"

# Agent 2: French → Hebrew (using output from Agent 1)
AGENT2_SKILL=$(cat agent2_skill.txt)

AGENT2_PAYLOAD=$(cat <<EOF
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": $(echo "$AGENT2_SKILL" | jq -Rs .)},
    {"role": "user", "content": $(echo "$FRENCH_OUTPUT" | jq -Rs .)}
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
EOF
)

AGENT2_RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "$AGENT2_PAYLOAD")

HEBREW_OUTPUT=$(echo "$AGENT2_RESPONSE" | jq -r '.choices[0].message.content')
echo "Hebrew: $HEBREW_OUTPUT"

# Continue with Agent 3...
```

---

## 🧪 Method 3: Testing Individual Agents

### Test Agent 1 Only (English → French)

```bash
# Create a test script
cat > test_agent1.sh << 'EOF'
#!/bin/bash
API_KEY="$OPENAI_API_KEY"
AGENT1_SKILL=$(cat agent1_skill.txt)
INPUT="$1"

PAYLOAD=$(cat <<PAYLOAD_EOF
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": $(echo "$AGENT1_SKILL" | jq -Rs .)},
    {"role": "user", "content": $(echo "$INPUT" | jq -Rs .)}
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
PAYLOAD_EOF
)

RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$PAYLOAD")

echo "$RESPONSE" | jq -r '.choices[0].message.content'
EOF

chmod +x test_agent1.sh

# Test it
./test_agent1.sh "The artifical system works eficiently"
```

### Test Agent 2 Only (French → Hebrew)

```bash
cat > test_agent2.sh << 'EOF'
#!/bin/bash
API_KEY="$OPENAI_API_KEY"
AGENT2_SKILL=$(cat agent2_skill.txt)
INPUT="$1"

PAYLOAD=$(cat <<PAYLOAD_EOF
{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": $(echo "$AGENT2_SKILL" | jq -Rs .)},
    {"role": "user", "content": $(echo "$INPUT" | jq -Rs .)}
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
PAYLOAD_EOF
)

RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$PAYLOAD")

echo "$RESPONSE" | jq -r '.choices[0].message.content'
EOF

chmod +x test_agent2.sh

# Test it with French input
./test_agent2.sh "Le système fonctionne bien"
```

---

## 📊 Viewing Results

### Check Output Files

```bash
# List all outputs
ls -lR outputs/

# View specific results
cat outputs/noise_0/agent1_french.txt
cat outputs/noise_0/agent2_hebrew.txt
cat outputs/noise_0/agent3_english.txt

# View all results for a noise level
for file in outputs/noise_30/*.txt; do
  echo "=== $file ==="
  cat "$file"
  echo ""
done
```

### Compare Original vs Final Output

```bash
# Original clean sentence
ORIGINAL="The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."

# Final output after agent chain
FINAL=$(cat outputs/noise_50/agent3_english.txt)

echo "Original: $ORIGINAL"
echo "Final:    $FINAL"
```

---

## 🎓 Understanding the CLI Components

### 1. **jq** - JSON Processor

```bash
# Extract value from JSON
echo '{"name": "Agent1", "output": "Bonjour"}' | jq -r '.output'
# Output: Bonjour

# Convert string to JSON string (escaping)
echo "Hello World" | jq -Rs .
# Output: "Hello World\n"
```

### 2. **curl** - HTTP Client

```bash
# Basic POST request
curl -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{"model": "gpt-4o-mini", "messages": [...]}'

# -s = silent (no progress bar)
# -X POST = HTTP POST method
# -H = header
# -d = data payload
```

### 3. **Bash Scripting**

```bash
# Variables
MY_VAR="hello"
echo $MY_VAR

# Command substitution
OUTPUT=$(cat file.txt)

# Heredoc (multi-line strings)
TEXT=$(cat <<EOF
Line 1
Line 2
EOF
)
```

---

## 🚀 Quick Start Workflow

### Complete Workflow (Copy-Paste Ready)

```bash
# 1. Navigate to project
cd "/Users/fouadaz/LearningFromUniversity/Learning/LLMSAndMultiAgentOrchestration/course-materials/assignments/Assignment_3_Agentic Turing Machine Development_(CLI)"

# 2. Activate UV environment
source .venv/bin/activate

# 3. Set API key
export OPENAI_API_KEY='sk-your-key-here'

# 4. Verify setup
./verify_setup.sh

# 5. Run a single test
./run_agent_chain.sh 30 "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data."

# 6. Run full experiment
./run_full_experiment.sh

# 7. Analyze results
python analyze_results.py

# 8. View the graph
open semantic_drift_analysis.png
```

---

## 🔧 Creating Custom Agents

### Example: Create a 4th Agent

```bash
# 1. Create the agent's skill file
cat > agent4_skill.txt << 'EOF'
You are Agent 4: The Summarizer.

Your role is to create a concise summary of English text.

CRITICAL INSTRUCTIONS:
1. Read the English text carefully
2. Extract the main idea
3. Produce a 1-sentence summary
4. No explanations, only the summary
EOF

# 2. Add to the agent chain script
# Open run_agent_chain.sh and add:

# AGENT 4: Summarize
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
echo "Summary: $SUMMARY"
echo "$SUMMARY" > "$OUTPUT_DIR/agent4_summary.txt"
```

---

## 📝 Key Takeaways

✅ **Agents are defined by text files** (skill prompts)  
✅ **CLI tools handle orchestration** (bash + curl + jq)  
✅ **No Python needed for agent chain** (pure shell scripting)  
✅ **Sequential execution** - output of Agent N → input of Agent N+1  
✅ **API calls via curl** - standard HTTP POST requests  
✅ **JSON processing with jq** - parse API responses  

---

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not set"

```bash
export OPENAI_API_KEY='sk-your-key-here'
```

### Error: "jq: command not found"

```bash
brew install jq  # macOS
sudo apt-get install jq  # Linux
```

### Error: "Permission denied"

```bash
chmod +x run_agent_chain.sh
chmod +x run_full_experiment.sh
```

### API Response is "null"

```bash
# Check the full response for errors
echo "$RESPONSE" | jq .

# Common issues:
# - Invalid API key
# - Rate limit exceeded
# - Malformed JSON payload
```

---

## 📚 Additional Resources

- **OpenAI API Docs**: https://platform.openai.com/docs/api-reference
- **jq Manual**: https://stedolan.github.io/jq/manual/
- **Bash Scripting Guide**: https://www.gnu.org/software/bash/manual/

---

**You're now ready to create and execute AI agents via pure CLI!** 🚀


#!/bin/bash

# Agentic Turing Machine - CLI Agent Chain Execution (Markdown Version)
# This script runs the 3-agent translation pipeline using MARKDOWN skill files
# Demonstrates that agents can be skilled using .md files with rich formatting

set -e  # Exit on error

# Configuration
API_KEY="${OPENAI_API_KEY}"
if [ -z "$API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable not set"
    echo "Please set it with: export OPENAI_API_KEY='your-key-here'"
    exit 1
fi

API_URL="https://api.openai.com/v1/chat/completions"
MODEL="gpt-4o-mini"

# Input parameters
NOISE_LEVEL="$1"
INPUT_TEXT="$2"

if [ -z "$NOISE_LEVEL" ] || [ -z "$INPUT_TEXT" ]; then
    echo "Usage: $0 <noise_level> <input_text>"
    echo "Example: $0 0 'The artificial intelligence system...'"
    exit 1
fi

# Create output directory
OUTPUT_DIR="outputs_md/noise_${NOISE_LEVEL}"
mkdir -p "$OUTPUT_DIR"

echo "========================================"
echo "Running Agent Chain (Markdown Version)"
echo "Noise Level: ${NOISE_LEVEL}%"
echo "Using .md skill files"
echo "========================================"

# Read system prompts from MARKDOWN files
AGENT1_PROMPT=$(cat agent1_skill.md)
AGENT2_PROMPT=$(cat agent2_skill.md)
AGENT3_PROMPT=$(cat agent3_skill.md)

# ============================================
# AGENT 1: English (Noisy) -> French
# ============================================
echo ""
echo ">>> Agent 1: Translating English to French..."
echo "    Skill file: agent1_skill.md"
echo "Input: $INPUT_TEXT"

AGENT1_PAYLOAD=$(cat <<EOF
{
  "model": "$MODEL",
  "messages": [
    {
      "role": "system",
      "content": $(echo "$AGENT1_PROMPT" | jq -Rs .)
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

AGENT1_RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$AGENT1_PAYLOAD")

FRENCH_OUTPUT=$(echo "$AGENT1_RESPONSE" | jq -r '.choices[0].message.content')

if [ -z "$FRENCH_OUTPUT" ] || [ "$FRENCH_OUTPUT" = "null" ]; then
    echo "Error: Agent 1 failed to produce output"
    echo "Response: $AGENT1_RESPONSE"
    exit 1
fi

echo "Output: $FRENCH_OUTPUT"
echo "$FRENCH_OUTPUT" > "$OUTPUT_DIR/agent1_french.txt"

# ============================================
# AGENT 2: French -> Hebrew
# ============================================
echo ""
echo ">>> Agent 2: Translating French to Hebrew..."
echo "    Skill file: agent2_skill.md"
echo "Input: $FRENCH_OUTPUT"

AGENT2_PAYLOAD=$(cat <<EOF
{
  "model": "$MODEL",
  "messages": [
    {
      "role": "system",
      "content": $(echo "$AGENT2_PROMPT" | jq -Rs .)
    },
    {
      "role": "user",
      "content": $(echo "$FRENCH_OUTPUT" | jq -Rs .)
    }
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
EOF
)

AGENT2_RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$AGENT2_PAYLOAD")

HEBREW_OUTPUT=$(echo "$AGENT2_RESPONSE" | jq -r '.choices[0].message.content')

if [ -z "$HEBREW_OUTPUT" ] || [ "$HEBREW_OUTPUT" = "null" ]; then
    echo "Error: Agent 2 failed to produce output"
    echo "Response: $AGENT2_RESPONSE"
    exit 1
fi

echo "Output: $HEBREW_OUTPUT"
echo "$HEBREW_OUTPUT" > "$OUTPUT_DIR/agent2_hebrew.txt"

# ============================================
# AGENT 3: Hebrew -> English
# ============================================
echo ""
echo ">>> Agent 3: Translating Hebrew to English..."
echo "    Skill file: agent3_skill.md"
echo "Input: $HEBREW_OUTPUT"

AGENT3_PAYLOAD=$(cat <<EOF
{
  "model": "$MODEL",
  "messages": [
    {
      "role": "system",
      "content": $(echo "$AGENT3_PROMPT" | jq -Rs .)
    },
    {
      "role": "user",
      "content": $(echo "$HEBREW_OUTPUT" | jq -Rs .)
    }
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
EOF
)

AGENT3_RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "$AGENT3_PAYLOAD")

FINAL_ENGLISH=$(echo "$AGENT3_RESPONSE" | jq -r '.choices[0].message.content')

if [ -z "$FINAL_ENGLISH" ] || [ "$FINAL_ENGLISH" = "null" ]; then
    echo "Error: Agent 3 failed to produce output"
    echo "Response: $AGENT3_RESPONSE"
    exit 1
fi

echo "Output: $FINAL_ENGLISH"
echo "$FINAL_ENGLISH" > "$OUTPUT_DIR/agent3_english.txt"

# ============================================
# SUMMARY
# ============================================
echo ""
echo "========================================"
echo "Agent Chain Complete! (Markdown Version)"
echo "========================================"
echo "Skill Files Used:"
echo "  - agent1_skill.md"
echo "  - agent2_skill.md"
echo "  - agent3_skill.md"
echo ""
echo "Results saved to: $OUTPUT_DIR/"
echo "========================================"


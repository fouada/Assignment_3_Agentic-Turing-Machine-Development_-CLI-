#!/bin/bash
# Create New Agent Skill - Interactive CLI Tool

set -e

echo "🤖 Agent Creator - Claude Agent Skills"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get agent name
read -p "Agent name (e.g., text-summarizer): " AGENT_NAME

if [ -z "$AGENT_NAME" ]; then
    echo "❌ Agent name cannot be empty"
    exit 1
fi

# Check if agent already exists
if [ -d "skills/$AGENT_NAME" ]; then
    echo "❌ Agent '$AGENT_NAME' already exists!"
    echo "   Directory: skills/$AGENT_NAME/"
    exit 1
fi

# Get agent description
read -p "Short description: " DESCRIPTION

# Get capabilities
echo ""
echo "Agent capabilities (one per line, empty line to finish):"
CAPABILITIES=""
while true; do
    read -p "  • " CAP
    if [ -z "$CAP" ]; then
        break
    fi
    CAPABILITIES="${CAPABILITIES}- ${CAP}\n"
done

# Create directory
mkdir -p "skills/$AGENT_NAME"

# Create SKILL.md
cat > "skills/$AGENT_NAME/SKILL.md" << EOF
# ${AGENT_NAME^}

## Description
${DESCRIPTION}

## Capabilities
$(echo -e "$CAPABILITIES")

## When to Use This Skill
Use this skill when you need to [describe use case].

## Instructions

### Core Principles
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

### Processing Steps
1. Read and understand the input
2. Apply the transformation/analysis
3. Format the output according to specifications
4. Return only the result

### Examples

**Example 1 - Basic:**
\`\`\`
Input: [example input]
Output: [example output]
\`\`\`

**Example 2 - Advanced:**
\`\`\`
Input: [complex example input]
Output: [complex example output]
\`\`\`

## Output Format
Return only the processed result as plain text, with no additional commentary, explanations, or metadata.

## Error Handling
- If input is empty, return: "ERROR: No input provided"
- If input is malformed, return: "ERROR: Invalid input format"
- Otherwise, always attempt to process the input

## Performance Notes
- Target processing time: < 5 seconds
- Output should be concise and focused
- Maintain consistency across similar inputs

## Related Skills
- [Related skill 1]
- [Related skill 2]
EOF

echo ""
echo "✅ Agent created successfully!"
echo ""
echo "📁 Location: skills/$AGENT_NAME/SKILL.md"
echo ""
echo "Next steps:"
echo "  1. Edit the skill file:"
echo "     nano skills/$AGENT_NAME/SKILL.md"
echo ""
echo "  2. Add detailed instructions and examples"
echo ""
echo "  3. Test your agent:"
echo "     python3 test_agent.py $AGENT_NAME \"test input\""
echo ""
echo "  4. Use in your pipeline:"
echo "     Add to run_with_skills.py"
echo ""


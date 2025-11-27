#!/bin/bash
# Uninstall Agent Skills from ~/.claude/skills/ directory

set -e

echo "🗑️  Agent Skills Uninstaller"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

TARGET_DIR="$HOME/.claude/skills"

# Check if skills are installed
if [ ! -d "$TARGET_DIR" ]; then
    echo "ℹ️  No skills installed (directory doesn't exist)"
    echo "   Location: $TARGET_DIR"
    exit 0
fi

# Count installed skills from this project
SKILL_COUNT=0
echo "Skills that will be removed:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for skill_name in "english-to-french-translator" "french-to-hebrew-translator" "hebrew-to-english-translator" "translation-chain-coordinator"; do
    if [ -d "$TARGET_DIR/$skill_name" ]; then
        echo "  ✗ $skill_name"
        SKILL_COUNT=$((SKILL_COUNT + 1))
    fi
done

if [ $SKILL_COUNT -eq 0 ]; then
    echo "  (None found)"
    echo ""
    echo "ℹ️  No skills from this project are installed"
    exit 0
fi

echo ""
echo "📍 Location: $TARGET_DIR"
echo ""

# Ask for confirmation
read -p "Remove these $SKILL_COUNT skills? [y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Removing..."
echo ""

# Remove each skill
REMOVED=0
for skill_name in "english-to-french-translator" "french-to-hebrew-translator" "hebrew-to-english-translator" "translation-chain-coordinator"; do
    if [ -d "$TARGET_DIR/$skill_name" ]; then
        echo "  🗑️  Removing: $skill_name"
        rm -rf "$TARGET_DIR/$skill_name"
        REMOVED=$((REMOVED + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Uninstallation Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   Removed: $REMOVED skills"
echo ""
echo "🔍 Verify removal:"
echo "   ls -la ~/.claude/skills/"
echo ""


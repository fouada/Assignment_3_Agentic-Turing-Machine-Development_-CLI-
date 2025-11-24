#!/bin/bash
# Install Agent Skills to ~/.claude/skills/ directory
# This makes them available to Claude Code and Claude applications

set -e

echo "🤖 Agent Skills Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Define paths
SOURCE_DIR="$(pwd)/skills"
TARGET_DIR="$HOME/.claude/skills"

# Check if source skills exist
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Error: skills/ directory not found"
    echo "   Expected: $SOURCE_DIR"
    exit 1
fi

# Count skills
SKILL_COUNT=$(find "$SOURCE_DIR" -name "SKILL.md" | wc -l | tr -d ' ')

if [ "$SKILL_COUNT" -eq 0 ]; then
    echo "❌ Error: No SKILL.md files found in $SOURCE_DIR"
    exit 1
fi

echo "📦 Found $SKILL_COUNT agent skills to install"
echo ""

# List skills that will be installed
echo "Skills to install:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for skill_dir in "$SOURCE_DIR"/*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
        skill_name=$(basename "$skill_dir")
        echo "  ✓ $skill_name"
    fi
done
echo ""

# Ask for confirmation
read -p "Install skills to $TARGET_DIR? [y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo ""
echo "Installing..."
echo ""

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Install each skill
INSTALLED=0
UPDATED=0
FAILED=0

for skill_dir in "$SOURCE_DIR"/*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
        skill_name=$(basename "$skill_dir")
        target_skill_dir="$TARGET_DIR/$skill_name"
        
        if [ -d "$target_skill_dir" ]; then
            echo "  🔄 Updating: $skill_name"
            rm -rf "$target_skill_dir"
            UPDATED=$((UPDATED + 1))
        else
            echo "  ✨ Installing: $skill_name"
            INSTALLED=$((INSTALLED + 1))
        fi
        
        # Copy the skill
        if cp -r "$skill_dir" "$target_skill_dir"; then
            echo "     → $target_skill_dir"
        else
            echo "     ❌ Failed to install $skill_name"
            FAILED=$((FAILED + 1))
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   New installs: $INSTALLED"
echo "   Updated:      $UPDATED"
if [ $FAILED -gt 0 ]; then
    echo "   Failed:       $FAILED"
fi
echo ""
echo "📍 Skills installed to: $TARGET_DIR"
echo ""
echo "🎯 Your skills are now available in:"
echo "   • Claude Code (desktop app)"
echo "   • Claude CLI tools"
echo "   • Any app that reads ~/.claude/skills/"
echo ""
echo "🔍 Verify installation:"
echo "   ls -la ~/.claude/skills/"
echo ""
echo "📝 To update skills later, just run this script again!"
echo ""


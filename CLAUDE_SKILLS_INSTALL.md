# Installing Agent Skills to Claude Directory

## 📍 Overview

Claude applications (Claude Code, Claude Desktop, etc.) automatically load skills from:
```
~/.claude/skills/
```

This guide shows you how to install your agent skills to this directory so they're available across all Claude applications.

---

## 🚀 Quick Install

### Install Skills
```bash
./install_skills.sh
```

This will:
1. Check for skills in `./skills/` directory
2. Copy them to `~/.claude/skills/`
3. Make them available to Claude applications

### Uninstall Skills
```bash
./uninstall_skills.sh
```

---

## 📂 Directory Structure

### Before Installation
```
Your Project/
└── skills/
    ├── english-to-french-translator/SKILL.md
    ├── french-to-hebrew-translator/SKILL.md
    ├── hebrew-to-english-translator/SKILL.md
    └── translation-chain-coordinator/SKILL.md
```

### After Installation
```
~/.claude/
└── skills/
    ├── english-to-french-translator/SKILL.md    ← Installed
    ├── french-to-hebrew-translator/SKILL.md     ← Installed
    ├── hebrew-to-english-translator/SKILL.md    ← Installed
    └── translation-chain-coordinator/SKILL.md   ← Installed
```

---

## 🔄 Complete Workflow

### 1. Develop Skills Locally
```bash
# Create/edit skills in your project
nano skills/english-to-french-translator/SKILL.md

# Test locally
python3 test_agent.py english-to-french-translator "test"
```

### 2. Install to Claude
```bash
# Install skills to ~/.claude/skills/
./install_skills.sh
```

### 3. Use in Claude Applications

**Claude Code:**
- Skills are automatically loaded
- Use them in your coding projects
- No additional configuration needed

**Claude Desktop:**
- Skills available in chat interface
- Claude will detect relevant skills automatically

**Claude API (with skills support):**
```python
import anthropic

client = anthropic.Anthropic()

# Skills are loaded from ~/.claude/skills/
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    # Skills auto-detected when relevant
    messages=[{
        "role": "user",
        "content": "Translate to French: Hello world"
    }]
)
```

### 4. Update Skills
```bash
# Edit skill locally
nano skills/english-to-french-translator/SKILL.md

# Reinstall (overwrites existing)
./install_skills.sh
```

---

## 🛠️ Manual Installation

If you prefer manual installation:

```bash
# Create directory
mkdir -p ~/.claude/skills

# Copy skills
cp -r skills/english-to-french-translator ~/.claude/skills/
cp -r skills/french-to-hebrew-translator ~/.claude/skills/
cp -r skills/hebrew-to-english-translator ~/.claude/skills/
cp -r skills/translation-chain-coordinator ~/.claude/skills/

# Verify
ls -la ~/.claude/skills/
```

---

## 🔍 Verify Installation

### Check Installed Skills
```bash
ls -la ~/.claude/skills/
```

Expected output:
```
english-to-french-translator/
french-to-hebrew-translator/
hebrew-to-english-translator/
translation-chain-coordinator/
```

### View Installed Skill
```bash
cat ~/.claude/skills/english-to-french-translator/SKILL.md
```

### Count Skills
```bash
find ~/.claude/skills -name "SKILL.md" | wc -l
```
Should show: `4`

---

## 🎯 Using Installed Skills

### Option 1: Claude Code

1. Open Claude Code
2. Start a new project or conversation
3. Ask Claude to translate something
4. Claude automatically uses your skills!

**Example:**
```
You: "Translate 'Hello world' to French"
Claude: [Uses english-to-french-translator skill]
        "Bonjour le monde"
```

### Option 2: Claude API

```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Translate this sentence through French, Hebrew, and back to English: 'The artificial intelligence system can process natural language.'"
    }]
)

print(response.content[0].text)
# Claude will use your installed skills automatically!
```

### Option 3: Your Python Scripts

Your existing scripts still work:
```bash
# Still uses skills/ directory in project
python3 run_with_skills.py --all

# Analysis (local)
python3 analyze_results_local.py
```

---

## 🔄 Update Workflow

When you improve a skill:

```bash
# 1. Edit locally
nano skills/english-to-french-translator/SKILL.md

# 2. Test locally (optional)
python3 test_agent.py english-to-french-translator "test"

# 3. Reinstall to Claude
./install_skills.sh

# 4. Skills updated in Claude!
```

---

## 🗑️ Uninstallation

### Remove All Project Skills
```bash
./uninstall_skills.sh
```

### Remove Specific Skill
```bash
rm -rf ~/.claude/skills/skill-name
```

### Remove All Claude Skills
```bash
rm -rf ~/.claude/skills/
```

---

## 📝 Best Practices

### 1. Version Control
```bash
# Keep skills in your project under version control
git add skills/
git commit -m "Update translation skills"

# Install to Claude after committing
./install_skills.sh
```

### 2. Backup Before Major Changes
```bash
# Backup installed skills
tar -czf claude-skills-backup.tar.gz ~/.claude/skills/

# Restore if needed
tar -xzf claude-skills-backup.tar.gz -C ~/
```

### 3. Keep Project and Claude in Sync
```bash
# After pulling changes
git pull
./install_skills.sh  # Update Claude with latest
```

### 4. Test Before Installing
```bash
# Test locally first
python3 test_agent.py agent-name "test input"

# If good, install to Claude
./install_skills.sh
```

---

## 🐛 Troubleshooting

### Skills Not Loading in Claude Code

**Problem:** Claude Code doesn't see your skills

**Solutions:**
```bash
# 1. Verify installation
ls -la ~/.claude/skills/

# 2. Check SKILL.md files exist
find ~/.claude/skills -name "SKILL.md"

# 3. Restart Claude Code

# 4. Reinstall
./uninstall_skills.sh
./install_skills.sh
```

### Permission Errors

**Problem:** Can't write to ~/.claude/

**Solution:**
```bash
# Fix permissions
mkdir -p ~/.claude/skills
chmod 755 ~/.claude
chmod 755 ~/.claude/skills
```

### Skills Conflict

**Problem:** Multiple versions of same skill

**Solution:**
```bash
# Remove old version
rm -rf ~/.claude/skills/old-skill-name

# Install new version
./install_skills.sh
```

---

## 🔗 Related Commands

```bash
# List all installed skills
ls -1 ~/.claude/skills/

# View skill content
cat ~/.claude/skills/agent-name/SKILL.md

# Edit installed skill directly
nano ~/.claude/skills/agent-name/SKILL.md

# Copy skill to project
cp -r ~/.claude/skills/some-skill skills/

# Compare project vs installed
diff skills/agent-name/SKILL.md ~/.claude/skills/agent-name/SKILL.md
```

---

## 📚 Learn More

- **Claude Skills Documentation**: https://www.claude.com/blog/skills
- **Claude Code**: https://claude.ai/code
- **Your Project README**: `README.md`

---

## ✅ Quick Reference

```bash
# INSTALL
./install_skills.sh              # Install all skills to ~/.claude/

# VERIFY
ls -la ~/.claude/skills/         # List installed skills

# UPDATE
./install_skills.sh              # Overwrites with latest

# UNINSTALL
./uninstall_skills.sh            # Remove all project skills

# TEST
python3 test_agent.py agent-name "input"  # Test before installing
```

---

**Your skills are now portable across all Claude applications!** 🎉


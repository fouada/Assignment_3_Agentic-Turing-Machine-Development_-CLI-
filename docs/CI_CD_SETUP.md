# 🔄 CI/CD Setup Guide

Complete guide for setting up GitHub Actions CI/CD for the Agentic Turing Machine project.

## 📋 Quick Setup

### 1. Push to GitHub

```bash
# Initialize and push
git add .
git commit -m "Add CI/CD workflows"
git push origin main
```

### 2. Add API Secret (Required for Experiments)

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your Claude API key
6. Click **Add secret**

### 3. Enable Workflows

Workflows are enabled by default. Check the **Actions** tab to see them running.

---

## 🔧 Available Workflows

### 1. Pipeline CI/CD (`pipeline.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop`
- Pull requests to `main` or `master`
- Manual dispatch

**Jobs:**

| Job | Description | Requires API Key |
|-----|-------------|------------------|
| `validate` | Validates skills & code syntax | No |
| `analyze` | Runs local analysis on existing outputs | No |
| `experiments` | Runs full agent experiments | **Yes** |
| `test-agents` | Tests individual agent skills | **Yes** |

**Manual Trigger Options:**
- `noise_level`: Specific noise level (0-50) or "all"
- `run_experiments`: Enable experiment execution

### 2. Release (`release.yml`)

**Triggers:**
- Push tags starting with `v` (e.g., `v1.0.0`)
- Manual dispatch with version input

**Creates:**
- GitHub Release
- `.tar.gz` and `.zip` archives
- Includes outputs and analysis results

### 3. Validate PR (`validate-pr.yml`)

**Triggers:**
- Pull requests modifying skills, Python, or shell files

**Checks:**
- Skill file structure
- Required sections in SKILL.md
- Python syntax

---

## 🚀 Usage Examples

### Run Full Pipeline on Push

Include `[run-experiments]` in your commit message:

```bash
git commit -m "Update skills [run-experiments]"
git push
```

### Run Specific Noise Level

Go to **Actions** → **Agent Pipeline CI/CD** → **Run workflow**:
- Set `noise_level` to desired value (e.g., `25`)
- Check `run_experiments` checkbox

### Test Individual Agents

Include `[test-agents]` in your commit message:

```bash
git commit -m "Fix agent prompt [test-agents]"
git push
```

### Create a Release

```bash
# Tag and push
git tag v1.0.0
git push origin v1.0.0
```

Or manually:
- Go to **Actions** → **Release** → **Run workflow**
- Enter version (e.g., `v1.0.0`)

---

## 📊 Artifacts

Workflow runs produce downloadable artifacts:

| Artifact | Contents | Retention |
|----------|----------|-----------|
| `analysis-results` | PNG, PDF, JSON analysis files | 30 days |
| `experiment-results` | All outputs + analysis | 30 days |

Access artifacts:
1. Go to **Actions**
2. Click on a workflow run
3. Scroll to **Artifacts** section

---

## 🔐 Secrets Configuration

### Required Secret

| Name | Description | Required For |
|------|-------------|--------------|
| `ANTHROPIC_API_KEY` | Claude API key | Running experiments |

### Setting Up Secrets

```bash
# Via GitHub CLI
gh secret set ANTHROPIC_API_KEY
# Enter your key when prompted
```

Or through the GitHub web interface (Settings → Secrets).

---

## 📁 File Structure

```
.github/
├── workflows/
│   ├── pipeline.yml      # Main CI/CD pipeline
│   ├── release.yml       # Release automation
│   └── validate-pr.yml   # PR validation
└── dependabot.yml        # Dependency updates
```

---

## 🔄 Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Push/PR                                                     │
│    │                                                         │
│    ▼                                                         │
│  ┌─────────────────┐                                        │
│  │    VALIDATE     │ ← Always runs                          │
│  │  • Check skills │                                        │
│  │  • Python syntax│                                        │
│  │  • Shell syntax │                                        │
│  └────────┬────────┘                                        │
│           │                                                  │
│     ┌─────┴─────┐                                           │
│     │           │                                           │
│     ▼           ▼                                           │
│  ┌──────┐  ┌────────────────┐                              │
│  │ANALYZE│  │  EXPERIMENTS   │ ← Only with API key          │
│  │(Local)│  │ • Run agents   │   + trigger flag             │
│  └───┬───┘  │ • Save outputs │                              │
│      │      └───────┬────────┘                              │
│      │              │                                        │
│      └──────┬───────┘                                        │
│             │                                                │
│             ▼                                                │
│      ┌─────────────┐                                        │
│      │  ARTIFACTS  │                                        │
│      │ • PNG graph │                                        │
│      │ • JSON data │                                        │
│      │ • Outputs   │                                        │
│      └─────────────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Customization

### Add New Agent Skill Validation

Edit `.github/workflows/pipeline.yml`:

```yaml
- name: Check skills structure
  run: |
    # Add your new skill
    for skill in "english-to-french-translator" "new-agent-name"; do
      ...
    done
```

### Change Python Version

Edit `env.PYTHON_VERSION` in workflow files:

```yaml
env:
  PYTHON_VERSION: '3.12'  # Change version
```

### Add More Tests

Add new steps to the `validate` job:

```yaml
- name: Custom validation
  run: |
    # Your custom checks
```

---

## ⚠️ Troubleshooting

### "ANTHROPIC_API_KEY not set"

**Cause:** Secret not configured  
**Fix:** Add the secret in repository settings

### Experiments Not Running

**Cause:** Trigger conditions not met  
**Fix:** Include `[run-experiments]` in commit message or use manual dispatch

### Analysis Fails

**Cause:** Missing output files  
**Fix:** Either:
1. Run experiments first
2. Commit existing `outputs/` directory

### Permission Denied

**Cause:** Workflow permissions  
**Fix:** Go to Settings → Actions → General → Workflow permissions → Read and write

---

## 📚 Related Documentation

- [README.md](README.md) - Project overview
- [PIPELINE_EXECUTION.md](PIPELINE_EXECUTION.md) - Local execution guide
- [CLAUDE_SKILLS_INSTALL.md](CLAUDE_SKILLS_INSTALL.md) - Skills installation

---

## 🎯 Best Practices

1. **Test locally first** before pushing
2. **Use specific noise levels** for quick CI tests
3. **Keep outputs committed** for analysis without API calls
4. **Tag releases** for important milestones
5. **Review artifacts** after experiment runs
6. **Monitor API usage** when running experiments

---

## 📞 Support

- Check workflow logs in **Actions** tab
- Review [GitHub Actions documentation](https://docs.github.com/en/actions)
- Open an issue for project-specific problems


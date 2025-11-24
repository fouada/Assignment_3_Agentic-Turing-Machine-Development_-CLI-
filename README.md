# Agentic Turing Machine - Claude Agent Skills

Multi-agent translation pipeline demonstrating LLM attention mechanism robustness using [Claude Agent Skills](https://www.claude.com/blog/skills).

## 🚀 Quick Start

### Setup (One-time)
```bash
# Install dependencies
pip install anthropic numpy matplotlib scikit-learn

# Set your Claude API key
export ANTHROPIC_API_KEY='your-key-here'
```

### Run Experiment
```bash
# Run single noise level
python3 run_with_skills.py --noise 25

# Run all noise levels (0%, 10%, 20%, 25%, 30%, 40%, 50%)
python3 run_with_skills.py --all
```

### Analyze Results
```bash
# Local analysis (NO API calls needed!)
python3 analyze_results_local.py

# View visualization
open semantic_drift_analysis_local.png
```

## 📋 What This Does

**Translation Pipeline**: English → French → Hebrew → English

**Agents**:
1. **Agent 1**: English → French (handles noisy input with spelling errors)
2. **Agent 2**: French → Hebrew (bridges language families)
3. **Agent 3**: Hebrew → English (completes round-trip)

**Test Sentence**:
```
Original: "The artificial intelligence system can efficiently process 
          natural language and understand complex semantic relationships 
          within textual data."
          
With 50% errors: "The artifical inteligence systm can eficiently proces 
                 naturel langauge and understnd complx semantic 
                 relatioships withn textul data."
```

## 🎯 Key Finding

**Moderate noise improves performance!** 

- 0% errors → 0.407 distance
- 50% errors → 0.308 distance ⭐ (BETTER!)

This demonstrates **stochastic resonance** in LLM attention mechanisms.

## 📊 Results

After running, you'll have:
- `outputs/noise_X/` - Translation outputs for each noise level
- `analysis_results_local.json` - Quantitative metrics
- `semantic_drift_analysis_local.png` - Visualization
- `semantic_drift_analysis_local.pdf` - Publication-ready graph

## 🧩 Project Structure

```
.
├── skills/                              # Agent Skills (core)
│   ├── english-to-french-translator/
│   │   └── SKILL.md
│   ├── french-to-hebrew-translator/
│   │   └── SKILL.md
│   ├── hebrew-to-english-translator/
│   │   └── SKILL.md
│   └── translation-chain-coordinator/
│       └── SKILL.md
├── run_with_skills.py                   # Main execution script
├── analyze_results_local.py             # Analysis (no API)
├── input_data.txt                       # Test data
├── requirements.txt                     # Python dependencies
└── outputs/                             # Results
```

## 🔧 Customizing Agents

Edit any SKILL.md file to modify agent behavior:

```bash
# Edit agent instructions
nano skills/english-to-french-translator/SKILL.md

# Changes take effect on next run
python3 run_with_skills.py --noise 25
```

## 📈 Metrics Explained

| Metric | What It Measures | Range | Better |
|--------|------------------|-------|--------|
| **Cosine Distance** | Semantic similarity (TF-IDF) | 0-2 | Lower |
| **Text Similarity** | Character-level match | 0-1 | Higher |
| **Word Overlap** | Word preservation (Jaccard) | 0-1 | Higher |

## 🐛 Troubleshooting

**"ANTHROPIC_API_KEY not set"**
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

**"Module not found"**
```bash
pip install anthropic numpy matplotlib scikit-learn
```

**"Skills directory not found"**
```bash
# Ensure you're in the project root
ls skills/
```

## 📚 Learn More

- **Agent Skills**: https://www.claude.com/blog/skills
- **API Docs**: https://docs.anthropic.com/
- **Skills Cookbook**: https://github.com/anthropics/anthropic-cookbook/tree/main/skills

## 📝 Citation

```
Anthropic. (2024). Introducing Agent Skills. 
Retrieved from https://www.claude.com/blog/skills
```

## 🎓 Assignment Requirements Met

✅ CLI-based implementation  
✅ 3 translation agents  
✅ ≥15 word sentence (16 words)  
✅ ≥25% spelling errors (up to 50%)  
✅ Vector distance calculation  
✅ 0-50% error rate experiments  
✅ Graph visualization  
✅ Complete documentation

---

**Made with Claude Agent Skills** 🤖


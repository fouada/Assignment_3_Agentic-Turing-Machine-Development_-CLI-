# Security Policy

## Supported Versions

We actively maintain security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**DO NOT** open a public issue for security vulnerabilities.

Instead, please email us directly:

- **Fouad Azem** - Fouad.Azem@gmail.com
- **Tal Goldengorn** - T.goldengoren@gmail.com

**Subject line**: `[SECURITY] Brief description of vulnerability`

### What to Include

Please provide:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** assessment
4. **Suggested fix** (if you have one)
5. **Your contact information** for follow-up

### Response Timeline

| Stage | Timeframe |
|-------|-----------|
| Initial response | Within 48 hours |
| Triage and assessment | Within 7 days |
| Fix development | Within 30 days (for critical issues) |
| Public disclosure | After fix is released |

### What to Expect

1. **Acknowledgment**: We'll confirm receipt of your report
2. **Assessment**: We'll evaluate the severity and validity
3. **Updates**: We'll keep you informed of our progress
4. **Credit**: We'll credit you in the security advisory (unless you prefer anonymity)

## Security Considerations

### API Key Protection

This project uses the Anthropic Claude API. Protect your API key:

```bash
# ✅ DO: Use environment variables
export ANTHROPIC_API_KEY='sk-ant-xxx'

# ✅ DO: Use .env files (not committed to git)
echo "ANTHROPIC_API_KEY=sk-ant-xxx" > .env

# ❌ DON'T: Hardcode in source files
# ❌ DON'T: Commit API keys to version control
# ❌ DON'T: Share in public channels
```

### Input Validation

The translation pipeline handles potentially noisy input. We implement:

- **Character-level sanitization** for noise injection
- **Unicode normalization** to prevent homoglyph attacks
- **Length limits** to prevent denial-of-service

### Adversarial Robustness

Our `src/adversarial_robustness.py` module tests for:

| Attack Type | Description | Mitigation |
|-------------|-------------|------------|
| Homoglyph | Unicode lookalike characters | Unicode normalization |
| Invisible chars | Zero-width characters | Character stripping |
| Typosquatting | Strategic typos | Spell checking |
| Prompt injection | Malicious prompts | Skill-based isolation |

### Dependency Security

We regularly audit dependencies:

```bash
# Check for known vulnerabilities
pip-audit

# Update dependencies
uv pip install --upgrade -e ".[all]"

# Verify lockfile integrity
uv pip sync
```

### CI/CD Security

Our GitHub Actions workflows:

- Use pinned action versions
- Limit permissions with `permissions:` blocks
- Store secrets in GitHub Secrets (not in code)
- Run in isolated environments

## Known Security Considerations

### Low Risk

1. **Local file access**: The analysis module reads from `outputs/` and `results/` directories. Ensure these directories don't contain sensitive data.

2. **API cost**: Malicious input could trigger excessive API calls. We implement rate limiting and cost tracking.

### Mitigated

1. **Prompt injection**: Skill-based architecture isolates agent instructions from user input.

2. **Unicode attacks**: Adversarial robustness testing identifies and mitigates Unicode-based attacks.

## Security Best Practices

### For Users

1. **Rotate API keys** regularly
2. **Use minimum permissions** for API keys
3. **Monitor API usage** for anomalies
4. **Keep dependencies updated**

### For Contributors

1. **Never commit secrets** to version control
2. **Use branch protection** rules
3. **Review dependencies** before adding
4. **Write secure code** following OWASP guidelines

## Acknowledgments

We thank the security researchers who help keep this project safe:

*No security vulnerabilities have been reported yet.*

---

## Contact

For security concerns:
- **Email**: Fouad.Azem@gmail.com, T.goldengoren@gmail.com
- **Response time**: Within 48 hours

For general questions, use [GitHub Issues](../../issues) instead.


# ADR-003: Comprehensive Cost Tracking System

**Status:** Accepted  
**Date:** 2025-11-26  
**Decision Makers:** Development Team  
**Technical Story:** API cost transparency and budget management

---

## Context

Claude API usage incurs costs based on token consumption:
- Input tokens: $3.00 per million tokens (Sonnet)
- Output tokens: $15.00 per million tokens (Sonnet)

Running experiments involves:
- Multiple API calls per translation chain (3 stages)
- Multiple noise levels (5 experiments)
- Potential for hundreds of API calls during development

**Without cost tracking:**
- ❌ No visibility into spending
- ❌ Risk of budget overruns
- ❌ Can't optimize for cost
- ❌ Difficult to justify API choices

---

## Decision

Implement a **comprehensive cost tracking system** that:

1. **Records every API call** with token usage
2. **Calculates costs in real-time** using current pricing
3. **Aggregates costs** per experiment and overall
4. **Exports detailed reports** in JSON format
5. **Supports multiple Claude models** with different pricing

### Implementation

```python
class CostTracker:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.requests = []
        self.model_pricing = {
            "claude-3-5-sonnet-20241022": {
                "input": 3.00,   # per 1M tokens
                "output": 15.00
            },
            "claude-3-opus-20240229": {
                "input": 15.00,
                "output": 75.00
            },
            "claude-3-haiku-20240307": {
                "input": 0.25,
                "output": 1.25
            }
        }
    
    def record_request(self, usage):
        """Record API request with token usage."""
        input_cost = (usage.input_tokens / 1_000_000) * self.pricing["input"]
        output_cost = (usage.output_tokens / 1_000_000) * self.pricing["output"]
        
        record = {
            "timestamp": datetime.now(),
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost
        }
        
        self.requests.append(record)
    
    def export_report(self, path):
        """Export cost report to JSON."""
        report = {
            "model": self.model_name,
            "total_requests": len(self.requests),
            "total_cost": sum(r["total_cost"] for r in self.requests),
            "requests": self.requests
        }
        path.write_text(json.dumps(report, indent=2))
```

---

## Rationale

### Why Comprehensive Cost Tracking?

**✅ Advantages:**

1. **Budget Transparency**
   - Know exactly how much each experiment costs
   - Track spending in real-time
   - Prevent unexpected bills

2. **Cost Optimization**
   - Identify expensive operations
   - Compare costs across models
   - Make informed model selection

3. **Research Documentation**
   - Include costs in research reports
   - Show cost-performance tradeoffs
   - Reproducible cost analysis

4. **Debugging**
   - Detect unusual token usage
   - Identify inefficient prompts
   - Optimize skill designs

5. **Compliance & Reporting**
   - Detailed audit trail
   - Per-request breakdown
   - Exportable reports

---

## Alternatives Considered

### Alternative 1: No Cost Tracking

```python
# ❌ NOT CHOSEN - Just use API without tracking
response = client.messages.create(...)
# No idea how much this cost!
```

**Pros:**
- ✅ Simpler implementation
- ✅ Less code

**Cons:**
- ❌ **No visibility:** Don't know spending
- ❌ **Budget risk:** Could overspend
- ❌ **No optimization:** Can't improve costs
- ❌ **Unprofessional:** Not production-ready

**Why Rejected:** Completely unacceptable for any serious project

---

### Alternative 2: Manual Calculation Post-Hoc

```python
# ❌ NOT CHOSEN - Calculate costs manually after
# Look at API dashboard, export CSV, calculate in Excel
```

**Pros:**
- ✅ No code needed

**Cons:**
- ❌ **Manual work:** Error-prone, time-consuming
- ❌ **Delayed feedback:** Only know costs after fact
- ❌ **Not per-experiment:** Can't attribute costs
- ❌ **No automation:** Doesn't scale

**Why Rejected:** Not automated, not integrated, not useful

---

### Alternative 3: Simple Token Counter

```python
# ❌ NOT CHOSEN - Just count tokens, no costs
total_tokens = 0
for response in responses:
    total_tokens += response.usage.input_tokens + response.usage.output_tokens
print(f"Total tokens: {total_tokens}")
```

**Pros:**
- ✅ Simple implementation
- ✅ Basic visibility

**Cons:**
- ❌ **No cost calculation:** User has to compute
- ❌ **No per-request detail:** Aggregated only
- ❌ **No export:** Not saved anywhere
- ❌ **Limited value:** Token count without context

**Why Rejected:** Too simplistic, doesn't provide actionable insights

---

## Consequences

### Positive Consequences

1. **✅ Complete Cost Visibility**
   - Every cent accounted for
   - Per-request breakdown
   - Exportable reports

2. **✅ Budget Control**
   - Monitor spending in real-time
   - Set alerts (future feature)
   - Prevent overruns

3. **✅ Optimization Insights**
   - Identify expensive prompts
   - Compare model costs
   - Optimize token usage

4. **✅ Professional Quality**
   - Production-ready feature
   - Audit trail
   - Compliance support

5. **✅ Research Value**
   - Cost-performance analysis
   - Include in academic papers
   - Reproducible results

### Negative Consequences

1. **⚠️ Small Overhead**
   - ~0.1ms per request (negligible)
   - Small memory footprint

2. **⚠️ Additional Code**
   - ~100 lines (well worth it)
   - Needs testing

### Mitigation

- **Performance:** Overhead is negligible (<0.1% of total time)
- **Complexity:** Well-encapsulated in CostTracker class
- **Testing:** Comprehensive unit tests ensure accuracy

---

## Implementation Details

### Cost Calculation

```python
def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost based on token usage.
    
    Formula:
        input_cost = (input_tokens / 1,000,000) × $3.00
        output_cost = (output_tokens / 1,000,000) × $15.00
        total_cost = input_cost + output_cost
    
    Example:
        Input: 1,234 tokens
        Output: 567 tokens
        
        input_cost = (1,234 / 1,000,000) × $3.00 = $0.003702
        output_cost = (567 / 1,000,000) × $15.00 = $0.008505
        total_cost = $0.012207 ≈ $0.01
    """
    input_cost = (input_tokens / 1_000_000) * PRICING[model]["input"]
    output_cost = (output_tokens / 1_000_000) * PRICING[model]["output"]
    return input_cost + output_cost
```

### Usage Pattern

```python
# Initialize tracker
tracker = CostTracker(model_name="claude-3-5-sonnet-20241022")

# Make API call
response = client.messages.create(...)

# Record usage
tracker.record_request(response.usage)

# Later: Export report
tracker.export_report(Path("results/cost_analysis.json"))
```

### Sample Output

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "total_requests": 15,
  "total_input_tokens": 12450,
  "total_output_tokens": 8930,
  "total_cost": 0.171360,
  "breakdown_by_stage": {
    "stage_1_en_to_fr": 0.057120,
    "stage_2_fr_to_he": 0.057120,
    "stage_3_he_to_en": 0.057120
  },
  "cost_per_noise_level": {
    "0": 0.034272,
    "25": 0.034272,
    "50": 0.034272,
    "75": 0.034272,
    "100": 0.034272
  }
}
```

---

## Validation & Testing

### Test Cases

1. **Accurate Cost Calculation**
   ```python
   def test_cost_calculation():
       tracker = CostTracker("claude-3-5-sonnet")
       usage = Mock(input_tokens=1000, output_tokens=500)
       tracker.record_request(usage)
       
       expected = (1000/1e6)*3 + (500/1e6)*15
       assert tracker.get_total_cost() == expected
   ```

2. **Multiple Requests Aggregation**
   ```python
   def test_multiple_requests():
       tracker = CostTracker("claude-3-5-sonnet")
       for _ in range(10):
           tracker.record_request(usage)
       
       assert len(tracker.requests) == 10
       assert tracker.get_total_cost() > 0
   ```

3. **Report Export**
   ```python
   def test_export_report(tmp_path):
       tracker = CostTracker("claude-3-5-sonnet")
       tracker.record_request(usage)
       
       report_path = tmp_path / "cost.json"
       tracker.export_report(report_path)
       
       assert report_path.exists()
       data = json.loads(report_path.read_text())
       assert "total_cost" in data
   ```

---

## Pricing Information (as of 2025-11-26)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Use Case |
|-------|----------------------|------------------------|----------|
| Claude 3.5 Sonnet | $3.00 | $15.00 | **Default:** Best balance |
| Claude 3 Opus | $15.00 | $75.00 | Highest quality |
| Claude 3 Haiku | $0.25 | $1.25 | Fastest, cheapest |

### Typical Experiment Costs

**Single Translation Chain (3 stages):**
- Average: ~4,000 input tokens, ~2,000 output tokens
- Cost: ~$0.042 per chain

**Full Experiment (5 noise levels):**
- 5 chains × $0.042 = ~$0.21
- 15 API calls total

**Development/Testing (100 runs):**
- 100 × $0.042 = ~$4.20
- **Cost tracking helps stay within budget!**

---

## Related Decisions

- [ADR-001: Claude Agent Skills](ADR-001-claude-agent-skills.md) - API usage patterns
- [ADR-002: Local Embeddings](ADR-002-local-embeddings.md) - Avoiding embedding API costs
- [ADR-004: Error Handling](ADR-004-error-handling.md) - Handling API errors

---

## References

1. [Anthropic Pricing](https://www.anthropic.com/api#pricing)
2. [Claude API Documentation](https://docs.anthropic.com/claude/reference/)
3. [Token Counting Guide](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)

---

## Future Enhancements

### Potential Features (Not Currently Implemented)

1. **Cost Alerts**
   ```python
   tracker.set_budget_limit(5.00)  # Alert if over $5
   tracker.set_alert_threshold(0.8)  # Alert at 80%
   ```

2. **Cost Prediction**
   ```python
   predicted_cost = tracker.predict_experiment_cost(
       num_chains=10,
       avg_input_tokens=4000,
       avg_output_tokens=2000
   )
   ```

3. **Model Comparison**
   ```python
   tracker.compare_models([
       "claude-3-5-sonnet",
       "claude-3-haiku"
   ])
   # Output: Haiku would save 88% ($0.05 vs $0.42)
   ```

4. **Real-time Dashboard**
   ```python
   tracker.start_dashboard()  # Live cost monitoring
   ```

---

**Last Updated:** 2025-11-26  
**Status:** Implemented and Accepted  
**Review Date:** When Anthropic updates pricing

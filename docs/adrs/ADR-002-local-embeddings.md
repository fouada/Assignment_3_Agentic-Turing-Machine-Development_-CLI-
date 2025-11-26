# ADR-002: Local TF-IDF Embeddings for Semantic Analysis

**Status:** Accepted  
**Date:** 2025-11-26  
**Decision Makers:** Development Team  
**Technical Story:** Semantic drift measurement implementation

---

## Context

We need to measure semantic similarity between original input and final output to quantify semantic drift across the translation chain. The system must:
- Calculate similarity between text pairs
- Work offline (no external dependencies)
- Be fast and deterministic
- Provide meaningful metrics
- Minimize API costs

### Requirements
- Measure semantic similarity at multiple noise levels
- Support statistical analysis of results
- Generate reproducible results
- Process 5+ text pairs per experiment

---

## Decision

We will use **local TF-IDF (Term Frequency-Inverse Document Frequency) embeddings** with **cosine distance** for semantic similarity measurement.

### Implementation Details

1. **Embedding Generation:** scikit-learn's `TfidfVectorizer`
2. **Similarity Metric:** Cosine distance
3. **Additional Metrics:** Word overlap, character similarity
4. **No External APIs:** All computation local

### Code Example
```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def get_local_embedding(texts: List[str]) -> np.ndarray:
    """Generate local TF-IDF embeddings."""
    vectorizer = TfidfVectorizer()
    embeddings = vectorizer.fit_transform(texts)
    return embeddings.toarray()

def calculate_cosine_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine distance between two vectors."""
    similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )
    return 1 - similarity  # Convert to distance
```

---

## Rationale

### Why TF-IDF + Cosine Distance?

**✅ Advantages:**

1. **No External Dependencies**
   - Runs completely offline
   - No API costs for embeddings
   - No rate limits
   - Fast execution (<50ms)

2. **Deterministic Results**
   - Same input → same output
   - Reproducible experiments
   - Easy to debug and validate

3. **Proven Effectiveness**
   - Well-established NLP technique
   - Good for comparing similar documents
   - Captures lexical similarity

4. **Computational Efficiency**
   - O(n) complexity for small documents
   - Vectorized NumPy operations
   - Minimal memory footprint

5. **Interpretability**
   - Cosine distance in [0, 2] range
   - 0 = identical, 2 = completely different
   - Easy to explain to stakeholders

6. **No Training Required**
   - Works out-of-the-box
   - No model to train or fine-tune
   - No dependency on pre-trained models

**❌ Limitations:**

1. **Lexical Only**
   - Doesn't capture deep semantics
   - "Car" and "automobile" treated as different
   - No understanding of synonyms

2. **Order Insensitive**
   - Bag-of-words approach
   - "Dog bites man" ≈ "Man bites dog"
   - Position information lost

3. **Short Text Challenges**
   - Less effective for very short texts
   - Sparse vectors for single sentences

---

## Alternatives Considered

### Alternative 1: External Embedding APIs (OpenAI, Cohere)

**Example:**
```python
# ❌ NOT CHOSEN
import openai

def get_embedding(text: str) -> List[float]:
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']
```

**Pros:**
- ✅ State-of-the-art semantic understanding
- ✅ Captures synonyms and context
- ✅ Better for short texts

**Cons:**
- ❌ **API costs:** $0.0001/1K tokens (adds up)
- ❌ **Network dependency:** Requires internet
- ❌ **Latency:** 200-500ms per request
- ❌ **Rate limits:** Throttling issues
- ❌ **Non-deterministic:** May change over time

**Why Rejected:**
- **Cost:** Would add $0.05-0.10 per experiment
- **Dependency:** Internet required
- **Complexity:** Additional error handling needed
- **Overkill:** TF-IDF sufficient for our use case

---

### Alternative 2: Pre-trained Transformers (BERT, Sentence-BERT)

**Example:**
```python
# ❌ NOT CHOSEN
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    return model.encode(text)
```

**Pros:**
- ✅ Excellent semantic understanding
- ✅ Captures context and nuance
- ✅ Local execution (after download)
- ✅ State-of-the-art performance

**Cons:**
- ❌ **Large dependency:** 80-400MB model download
- ❌ **Memory overhead:** ~500MB RAM
- ❌ **Slow inference:** 50-200ms per text (CPU)
- ❌ **Complexity:** CUDA/GPU setup for speed
- ❌ **Overkill:** Not needed for lexical similarity

**Why Rejected:**
- **Overhead:** Large model for simple task
- **Performance:** Slower than TF-IDF
- **Complexity:** More dependencies
- **Sufficient Alternative:** TF-IDF meets our needs

---

### Alternative 3: Simple Edit Distance (Levenshtein)

**Example:**
```python
# ❌ NOT CHOSEN
import Levenshtein

def calculate_similarity(text1: str, text2: str) -> float:
    distance = Levenshtein.distance(text1, text2)
    max_len = max(len(text1), len(text2))
    return 1 - (distance / max_len)
```

**Pros:**
- ✅ Very simple
- ✅ Fast for short texts
- ✅ Character-level precision

**Cons:**
- ❌ **No semantic understanding:** Pure character matching
- ❌ **Position sensitive:** "The cat sat" vs "Sat the cat" = very different
- ❌ **Doesn't handle paraphrasing:** "Hello" vs "Hi" = totally different
- ❌ **Poor for translations:** Word order often changes

**Why Rejected:**
- Too simplistic for semantic analysis
- Doesn't capture meaning preservation
- Not suitable for translation quality

---

## Consequences

### Positive Consequences

1. **✅ Zero Additional API Costs**
   - All analysis is local
   - No embedding API fees
   - Budget stays under control

2. **✅ Fast Analysis**
   - Complete analysis in <1 second
   - No network latency
   - Instant results

3. **✅ Reproducible Research**
   - Same inputs always give same outputs
   - Can verify results
   - Scientific validity

4. **✅ Offline Capability**
   - Works without internet
   - No rate limit issues
   - Reliable execution

5. **✅ Simple Dependencies**
   - scikit-learn already needed
   - NumPy already needed
   - No additional installs

### Negative Consequences

1. **⚠️ Limited Semantic Understanding**
   - Won't catch all meaning changes
   - Synonyms treated as different
   - May underestimate semantic drift

2. **⚠️ Baseline Quality**
   - Good enough, not best-in-class
   - Acceptable trade-off for cost/complexity
   - Could upgrade later if needed

### Mitigation Strategies

**For Limited Semantic Understanding:**
- ✅ Use **multiple metrics** (cosine distance + word overlap)
- ✅ Combine with **character similarity**
- ✅ Provide **human-readable outputs** for manual validation
- ✅ Document limitations in analysis report

**For Future Enhancement:**
- 📋 Add option for external embeddings (feature flag)
- 📋 Support pluggable embedding backends
- 📋 Benchmark against BERT embeddings

---

## Mathematical Foundation

### TF-IDF Formula

**Term Frequency (TF):**
$$\text{tf}(t,d) = \frac{\text{count of term } t \text{ in document } d}{\text{total terms in } d}$$

**Inverse Document Frequency (IDF):**
$$\text{idf}(t, D) = \log\frac{N}{|\{d \in D : t \in d\}|}$$

**TF-IDF:**
$$\text{tfidf}(t,d,D) = \text{tf}(t,d) \times \text{idf}(t,D)$$

### Cosine Distance Formula

**Cosine Similarity:**
$$\text{similarity}(x,y) = \frac{x \cdot y}{||x|| \cdot ||y||} = \frac{\sum_{i=1}^{n} x_i y_i}{\sqrt{\sum_{i=1}^{n} x_i^2} \cdot \sqrt{\sum_{i=1}^{n} y_i^2}}$$

**Cosine Distance:**
$$d(x,y) = 1 - \text{similarity}(x,y)$$

**Range:** [0, 2]
- 0 = identical vectors
- 1 = orthogonal (no similarity)
- 2 = opposite directions

---

## Validation & Testing

### Test Cases

1. **Identical Texts**
   ```python
   text1 = text2 = "Hello world"
   distance = calculate_cosine_distance(embed(text1), embed(text2))
   assert distance ≈ 0  # Should be nearly identical
   ```

2. **Completely Different Texts**
   ```python
   text1 = "Paris is the capital of France"
   text2 = "Dogs bark loudly at night"
   distance = calculate_cosine_distance(embed(text1), embed(text2))
   assert distance > 0.8  # Should be very different
   ```

3. **Similar Meanings**
   ```python
   text1 = "The cat sat on the mat"
   text2 = "A feline rested on the rug"
   # Note: TF-IDF won't recognize these as very similar
   # This is an accepted limitation
   ```

### Success Metrics

- ✅ Embedding generation: <50ms
- ✅ Cosine distance calculation: <1ms
- ✅ Identical texts: distance < 0.01
- ✅ Different texts: distance > 0.5
- ✅ Reproducibility: 100% same results

---

## Implementation Checklist

- [x] Implement `get_local_embedding()`
- [x] Implement `calculate_cosine_distance()`
- [x] Implement `calculate_word_overlap()`
- [x] Add unit tests for all metrics
- [x] Validate against known text pairs
- [x] Document mathematical formulas
- [x] Add error handling for edge cases
- [x] Export results to JSON

---

## Related Decisions

- [ADR-001: Claude Agent Skills](ADR-001-claude-agent-skills.md) - Why we need semantic analysis
- [ADR-003: Cost Tracking](ADR-003-cost-tracking.md) - Avoiding additional costs
- [ADR-005: Testing Strategy](ADR-005-testing-strategy.md) - How we test embeddings

---

## References

1. **TF-IDF:**
   - [Scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
   - [Understanding TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)

2. **Cosine Similarity:**
   - [Cosine Similarity Explained](https://en.wikipedia.org/wiki/Cosine_similarity)
   - [NumPy Documentation](https://numpy.org/doc/stable/)

3. **Alternatives:**
   - [Sentence-BERT](https://www.sbert.net/)
   - [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

---

## Future Considerations

### Potential Upgrades (Not Currently Implemented)

1. **Hybrid Approach**
   ```python
   # Combine TF-IDF with simple semantic features
   def enhanced_similarity(text1, text2):
       tfidf_sim = calculate_cosine_distance(...)
       word_overlap = calculate_word_overlap(...)
       return 0.7 * tfidf_sim + 0.3 * word_overlap
   ```

2. **Configurable Embedding Backend**
   ```python
   # Allow switching between backends
   if config.embedding_type == "tfidf":
       embeddings = get_local_embedding(texts)
   elif config.embedding_type == "openai":
       embeddings = get_openai_embedding(texts)
   ```

3. **Caching**
   ```python
   # Cache embeddings for repeated analysis
   @lru_cache(maxsize=128)
   def get_cached_embedding(text: str) -> np.ndarray:
       return get_local_embedding([text])[0]
   ```

---

**Last Updated:** 2025-11-26  
**Status:** Implemented and Accepted  
**Review Date:** 2026-01-26 (reassess if needs change)

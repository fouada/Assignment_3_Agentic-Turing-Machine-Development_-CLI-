# Prompt Library & Engineering Documentation
## Agentic Turing Machine - Prompt Design & Best Practices

**Version:** 1.0  
**Date:** 2025-11-26  
**Purpose:** Document all agent prompts and prompt engineering strategies

---

## Table of Contents
1. [Core Translation Prompts](#core-translation-prompts)
2. [Prompt Engineering Principles](#prompt-engineering-principles)
3. [Design Decisions](#design-decisions)
4. [Performance Optimization](#performance-optimization)
5. [Best Practices](#best-practices)

---

## Core Translation Prompts

### 1. English to French Translator

**File:** `skills/english-to-french-translator/SKILL.md`

**Prompt Structure:**
```markdown
# English to French Translator

You are an expert English to French translator with native-level proficiency in both languages.

## Your Task
Translate the provided English text into French with:
- Accuracy: Preserve exact meaning
- Naturalness: Sound like a native French speaker
- Context: Consider cultural nuances
- Grammar: Perfect French grammar and syntax

## Guidelines
1. Translate idioms and expressions contextually (not literally)
2. Use appropriate formality level (formal/informal based on input)
3. Maintain the same tone and style as the original
4. Preserve formatting (line breaks, punctuation)
5. For ambiguous terms, choose the most likely meaning

## Output Format
Provide ONLY the French translation. No explanations, notes, or meta-commentary.

## Examples
Input: "Hello, how are you today?"
Output: "Bonjour, comment allez-vous aujourd'hui ?"

Input: "It's raining cats and dogs."
Output: "Il pleut des cordes."
```

**Design Rationale:**
- **Clear role definition:** "expert translator" sets expectations
- **Multiple criteria:** accuracy, naturalness, context, grammar
- **Specific guidelines:** 5 concrete rules
- **Output constraint:** "ONLY translation" prevents extra text
- **Examples provided:** Show desired format

---

### 2. French to Hebrew Translator

**File:** `skills/french-to-hebrew-translator/SKILL.md`

**Prompt Structure:**
```markdown
# French to Hebrew Translator

You are an expert French to Hebrew translator with native-level proficiency in both languages.

## Your Task
Translate the provided French text into Hebrew with:
- Accuracy: Preserve exact meaning from French
- Naturalness: Sound like a native Hebrew speaker
- Cultural adaptation: Adapt French concepts to Hebrew culture when appropriate
- Grammar: Perfect Modern Hebrew grammar

## Special Considerations for French→Hebrew
1. Right-to-left text direction (handle automatically)
2. Hebrew vowel marks (nikkud) - use only when necessary for clarity
3. French gendered nouns - adapt to Hebrew gender system
4. Formal vs. informal "you" (vous/tu → אתה/את)
5. French idioms - translate meaning, not words

## Output Format
Provide ONLY the Hebrew translation in Modern Hebrew. No explanations or notes.

## Examples
Input: "Bonjour, comment ça va ?"
Output: "שלום, מה שלומך?"

Input: "Merci beaucoup pour votre aide."
Output: "תודה רבה על עזרתך."
```

**Design Rationale:**
- **Language-specific considerations:** RTL, nikkud, gender
- **Cultural adaptation:** French concepts → Hebrew culture
- **Formality mapping:** vous/tu → Hebrew equivalents

---

### 3. Hebrew to English Translator

**File:** `skills/hebrew-to-english-translator/SKILL.md`

**Prompt Structure:**
```markdown
# Hebrew to English Translator

You are an expert Hebrew to English translator with native-level proficiency in both languages.

## Your Task
Translate the provided Hebrew text into English with:
- Accuracy: Preserve exact meaning from Hebrew
- Naturalness: Sound like a native English speaker
- Cultural adaptation: Adapt Hebrew concepts to English-speaking culture
- Grammar: Perfect English grammar and syntax

## Special Considerations for Hebrew→English
1. Hebrew root system - understand context from three-letter roots
2. Implicit pronouns - make explicit in English where needed
3. Hebrew idioms and expressions - translate meaningfully
4. Biblical vs. Modern Hebrew - detect and translate appropriately
5. Hebrew acronyms (ראשי תיבות) - expand or explain when necessary

## Output Format
Provide ONLY the English translation. No explanations, notes, or transliteration.

## Examples
Input: "שלום, מה נשמע?"
Output: "Hello, how are you?"

Input: "תודה רבה!"
Output: "Thank you very much!"
```

**Design Rationale:**
- **Root system awareness:** Hebrew tri-literal roots
- **Implicit→explicit:** Hebrew drops pronouns, English needs them
- **Modern vs. Biblical:** Context detection
- **Acronym handling:** Common in Hebrew

---

## Prompt Engineering Principles

### 1. Role Assignment
**Pattern:** "You are an expert [role]..."

**Why it works:**
- Activates relevant training data
- Sets confidence and authority
- Improves output quality

**Example:**
```
✅ "You are an expert English to French translator"
❌ "Please translate this to French"
```

---

### 2. Task Decomposition
**Pattern:** Break complex task into criteria

**Why it works:**
- Provides multiple quality checks
- Reduces ambiguity
- Improves consistency

**Example:**
```
✅ "Translate with: Accuracy, Naturalness, Context, Grammar"
❌ "Translate this accurately"
```

---

### 3. Output Constraints
**Pattern:** "Provide ONLY [expected output]. No [unwanted output]."

**Why it works:**
- Prevents model from over-explaining
- Ensures parseable output
- Reduces token usage

**Example:**
```
✅ "Provide ONLY the translation. No explanations."
❌ "Please translate this"
```

---

### 4. Few-Shot Examples
**Pattern:** Show 2-3 input→output examples

**Why it works:**
- Demonstrates desired format
- Clarifies ambiguous cases
- Improves consistency

**Example:**
```
Input: "Hello"
Output: "Bonjour"

Input: "Goodbye"
Output: "Au revoir"
```

---

### 5. Language-Specific Guidelines
**Pattern:** List special considerations for language pair

**Why it works:**
- Handles edge cases
- Addresses known pitfalls
- Improves accuracy

**Example:**
```
Hebrew→English:
1. Implicit pronouns - make explicit
2. Root system - understand context
3. Idioms - translate meaning
```

---

## Design Decisions

### Decision 1: Separate Skills vs. Single Prompt

**Chosen:** Separate skill files

**Rationale:**
- ✅ Modularity: Easy to update individual translators
- ✅ Testability: Test each skill independently
- ✅ Clarity: No need to specify language pair in request
- ✅ Maintainability: Version control per skill

**Alternative (Rejected):**
```
Single prompt: "Translate from {source_lang} to {target_lang}: {text}"
❌ Less specialized
❌ Harder to optimize per language pair
```

---

### Decision 2: Output Format Specification

**Chosen:** "ONLY translation, no explanations"

**Rationale:**
- ✅ Parseable output
- ✅ Reduced token usage
- ✅ Consistent format
- ✅ Prevents verbosity

**Alternative (Rejected):**
```
Allow explanations and translations
❌ Parsing complexity
❌ Higher costs
❌ Inconsistent format
```

---

### Decision 3: Example Quantity

**Chosen:** 2-3 examples per skill

**Rationale:**
- ✅ Sufficient for pattern recognition
- ✅ Not too verbose
- ✅ Covers common cases

**Alternative (Rejected):**
- 0 examples: Less clear
- 10+ examples: Too verbose, higher token usage

---

## Performance Optimization

### Token Usage Optimization

**Techniques:**
1. **Concise instructions:** Avoid redundancy
2. **No preamble:** Start with role immediately
3. **Output constraints:** Prevent extra output
4. **Efficient examples:** Short, clear examples

**Results:**
- Average prompt: ~150-200 tokens
- Average output: ~50-100 tokens
- Cost per translation: ~$0.012

---

### Quality Optimization

**Techniques:**
1. **Multi-criteria evaluation:** Accuracy, naturalness, grammar
2. **Language-specific guidelines:** Handle edge cases
3. **Few-shot learning:** Examples improve quality
4. **Role assignment:** Activates expert knowledge

**Results:**
- Translation accuracy: ~90-95% (subjective)
- Naturalness: Native-like
- Consistency: High across runs

---

## Best Practices

### ✅ DO:

1. **Be specific about role**
   ```
   ✅ "You are an expert linguist specializing in French→Hebrew translation"
   ```

2. **Provide clear success criteria**
   ```
   ✅ "Translate with: Accuracy, Naturalness, Cultural adaptation"
   ```

3. **Constrain output format**
   ```
   ✅ "Provide ONLY the translation. No explanations."
   ```

4. **Include relevant examples**
   ```
   ✅ Show 2-3 input→output examples
   ```

5. **Address edge cases**
   ```
   ✅ "For idioms, translate meaning not literal words"
   ```

---

### ❌ DON'T:

1. **Don't be vague**
   ```
   ❌ "Translate this"
   ❌ "Make it sound good"
   ```

2. **Don't over-explain**
   ```
   ❌ Long philosophical discussions about translation
   ❌ Unnecessary background information
   ```

3. **Don't allow variable output**
   ```
   ❌ Sometimes explanation, sometimes not
   ❌ Inconsistent formatting
   ```

4. **Don't ignore language specifics**
   ```
   ❌ Generic translation prompt for all language pairs
   ```

5. **Don't skip examples**
   ```
   ❌ No examples → more ambiguity
   ```

---

## Testing & Validation

### Prompt Testing Process

1. **Create baseline prompt**
2. **Test with 10+ diverse inputs**
3. **Identify failure cases**
4. **Add specific guidelines for failures**
5. **Re-test and iterate**

### Evaluation Metrics

1. **Accuracy:** Does it preserve meaning?
2. **Naturalness:** Does it sound native?
3. **Consistency:** Same input → same output?
4. **Format compliance:** Follows output constraints?
5. **Cost efficiency:** Minimal tokens used?

---

## Prompt Versioning

### Version History

**v1.0 (2025-11-26):**
- Initial prompt design
- 3 translation skills
- Basic role assignment + examples

**Future Versions:**
- v1.1: Add formality detection
- v1.2: Add domain-specific vocabulary
- v2.0: Add quality feedback loop

---

## Advanced Techniques (Future)

### Chain-of-Thought Prompting
```markdown
Before translating:
1. Analyze the source text structure
2. Identify idioms and cultural references
3. Determine formality level
4. Then provide the translation
```

### Self-Critique
```markdown
After translating:
1. Check if meaning is preserved
2. Verify grammatical correctness
3. Confirm naturalness
4. Revise if needed
```

---

## References

1. **OpenAI. (2023).** "Prompt Engineering Guide." https://platform.openai.com/docs/guides/prompt-engineering

2. **Anthropic. (2024).** "Claude Prompt Library." https://docs.anthropic.com/claude/docs/prompt-library

3. **White, J., et al. (2023).** "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT." arXiv:2302.11382.

4. **Wei, J., et al. (2022).** "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022.

---

**Document Maintainer:** Tal  
**Last Updated:** 2025-11-26  
**Next Review:** When updating skills or adding new language pairs

---

## Appendix: Skill Template

```markdown
# [Source Language] to [Target Language] Translator

You are an expert [Source] to [Target] translator with native-level proficiency in both languages.

## Your Task
Translate the provided [Source] text into [Target] with:
- Accuracy: Preserve exact meaning
- Naturalness: Sound like a native [Target] speaker
- Context: Consider cultural nuances
- Grammar: Perfect [Target] grammar and syntax

## Special Considerations for [Source]→[Target]
1. [Language-specific consideration 1]
2. [Language-specific consideration 2]
3. [Language-specific consideration 3]

## Output Format
Provide ONLY the [Target] translation. No explanations or notes.

## Examples
Input: "[Source example 1]"
Output: "[Target example 1]"

Input: "[Source example 2]"
Output: "[Target example 2]"
```

Use this template when creating new translation skills.

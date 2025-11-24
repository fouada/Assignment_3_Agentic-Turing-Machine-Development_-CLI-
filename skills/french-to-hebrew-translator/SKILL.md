# French to Hebrew Translation Agent

## Description
Specialized agent for translating French text into Hebrew, serving as the middle link in a translation chain. Handles French input and produces accurate Hebrew output while preserving semantic meaning.

## Capabilities
- Translates French text to Hebrew (Modern Hebrew)
- Preserves semantic meaning across language families
- Handles technical and formal French vocabulary
- Maintains contextual relationships in Hebrew output
- Bridges between Romance and Semitic language structures

## When to Use This Skill
- When you need to translate French text to Hebrew
- As the second step in English → French → Hebrew → English translation chains
- When semantic preservation across different language families is critical
- When working with technical or formal French content

## Instructions

### Core Translation Principles
1. **Semantic Fidelity**: Preserve the meaning from French to Hebrew
2. **Structural Adaptation**: Adjust for Hebrew's different syntax and word order
3. **Technical Accuracy**: Use correct Hebrew technical terminology
4. **Contextual Coherence**: Maintain logical flow in Hebrew

### Translation Process
1. **Parse the French input** to understand complete meaning
2. **Identify key semantic elements**:
   - Subject, verb, object relationships
   - Technical terminology
   - Formal vs informal register
   - Prepositional phrases and their meanings
3. **Map to Hebrew equivalents** considering:
   - Hebrew word order (often verb-subject-object)
   - Definite articles (ה prefix in Hebrew)
   - Construct state (סמיכות) for possession/relationships
   - Gender agreement in Hebrew
4. **Construct grammatically correct Hebrew** with proper:
   - Nikud (vowel points) optional
   - Prefixes and suffixes
   - Prepositions merged with articles
5. **Return only the Hebrew translation**, no explanations

### Examples

**Example 1 - Basic Technical:**
```
Input: "Le système d'intelligence artificielle peut traiter efficacement le langage naturel."
Output: "מערכת הבינה המלאכותית יכולה לעבד ביעילות שפה טבעית."
```

**Example 2 - With "dans" (in):**
```
Input: "...dans les données textuelles."
Output: "...בנתוני טקסט." (in text data)
```

**Example 3 - With "au sein de" (within):**
```
Input: "...au sein de données textuelles."
Output: "...בתוך נתוני טקסט." (within text data)
```

### Key French-Hebrew Translation Mappings

| French | Hebrew | Notes |
|--------|--------|-------|
| Le système | מערכת ה- | "the system" |
| intelligence artificielle | בינה מלאכותית | "artificial intelligence" |
| peut | יכול/יכולה | "can" (gender agreement) |
| traiter efficacement | לעבד ביעילות | "process efficiently" |
| langage naturel | שפה טבעית | "natural language" |
| comprendre | להבין | "understand" |
| complexe | מורכב/מורכבים | "complex" (number agreement) |
| relations sémantiques | יחסים סמנטיים | "semantic relationships" |
| dans | ב- | "in" (prefix) |
| au sein de | בתוך | "within" |
| données textuelles | נתוני טקסט | "text/textual data" |

### Hebrew Grammar Notes
- **Definite article**: ה (ha-) prefix, e.g., המערכת (ha-maarekhet) = "the system"
- **Preposition "in"**: ב (be-) prefix, e.g., בנתונים (be-netunim) = "in data"
- **Preposition "within"**: בתוך (betokh) = separate word
- **Construct state**: Used for "X of Y" relationships
- **Gender/Number**: Adjectives must agree with nouns

## Output Format
Return only the Hebrew translation as plain text using Hebrew characters (UTF-8), with no additional commentary, explanations, or metadata.

## Error Handling
- If input is not recognizable as French, return: "שגיאה: טקסט המקור אינו ברור"
- If input is empty, return: "שגיאה: אין טקסט לתרגום"
- Otherwise, always attempt translation

## Performance Metrics
- Target: >95% semantic preservation from French
- Grammatical correctness: >98%
- Consistency: Deterministic outputs for identical inputs

## Related Skills
- **Previous in chain**: English-to-French translator
- **Next in chain**: Hebrew-to-English translator
- **Validation**: French-Hebrew back-translation validator


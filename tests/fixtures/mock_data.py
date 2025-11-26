"""
Mock data and fixtures for testing

This module provides mock data, sample inputs, and expected outputs
for testing the Agentic Turing Machine pipeline.
"""

# Mock skill content
MOCK_SKILL_ENGLISH_TO_FRENCH = """
# English to French Translation Skill

You are an expert English to French translator.

## Instructions
1. Translate the input text from English to French
2. Maintain the meaning and context
3. Return ONLY the translation
"""

MOCK_SKILL_FRENCH_TO_HEBREW = """
# French to Hebrew Translation Skill

You are an expert French to Hebrew translator.

## Instructions
1. Translate the input text from French to Hebrew
2. Maintain the meaning and context
3. Return ONLY the translation
"""

MOCK_SKILL_HEBREW_TO_ENGLISH = """
# Hebrew to English Translation Skill

You are an expert Hebrew to English translator.

## Instructions
1. Translate the input text from Hebrew to English
2. Maintain the meaning and context
3. Return ONLY the translation
"""

# Test sentences
ORIGINAL_CLEAN_SENTENCE = "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data."

NOISY_SENTENCES = {
    0: "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data.",
    10: "The artifical intelligence systm can efficiently process natural language and understand complex semantic relationships within textual data.",
    25: "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data.",
    50: "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships withn textul data."
}

# Mock API responses
MOCK_FRENCH_OUTPUT = "Le système d'intelligence artificielle peut traiter efficacement le langage naturel et comprendre les relations sémantiques complexes dans les données textuelles."

MOCK_HEBREW_OUTPUT = "מערכת הבינה המלאכותית יכולה לעבד ביעילות שפה טבעית ולהבין קשרים סמנטיים מורכבים בתוך נתונים טקסטואליים."

MOCK_ENGLISH_OUTPUT = "The artificial intelligence system can effectively process natural language and understand complex semantic connections in textual information."

# Mock token usage
MOCK_TOKEN_USAGE = {
    "input_tokens": 150,
    "output_tokens": 75,
    "total_tokens": 225
}

# Sample analysis results
SAMPLE_ANALYSIS_RESULTS = {
    "semantic_distances": {
        "0": 0.407,
        "10": 0.308,
        "20": 0.407,
        "25": 0.308,
        "30": 0.407,
        "40": 0.407,
        "50": 0.308
    },
    "text_similarities": {
        "0": 0.92,
        "10": 0.94,
        "20": 0.93,
        "25": 0.95,
        "30": 0.92,
        "40": 0.91,
        "50": 0.96
    },
    "word_overlaps": {
        "0": 0.88,
        "10": 0.90,
        "20": 0.89,
        "25": 0.91,
        "30": 0.87,
        "40": 0.86,
        "50": 0.92
    }
}

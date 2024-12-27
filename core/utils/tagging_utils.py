# bible-analysis/core/utils/tagging_utils.py

"""bible-analysis/core/utils/tagging_utils.py"""

import spacy

from config.tagging_config import EXCLUSION_KEYWORDS, LIFESPAN_INDICATORS

# Load spaCy model
nlp = spacy.load("en_core_web_sm", disable=["parser"])


def get_context(doc, span_or_token, window=3):
    """Get surrounding words for a token or span."""
    if isinstance(span_or_token, spacy.tokens.Token):
        start = max(0, span_or_token.i - window)
        end = min(len(doc), span_or_token.i + window + 1)
    elif isinstance(span_or_token, spacy.tokens.Span):
        start = max(0, span_or_token.start - window)
        end = min(len(doc), span_or_token.end + window)
    else:
        raise ValueError("Input must be a Token or Span.")

    return " ".join([doc[i].text for i in range(start, end)])


def calculate_confidence(sentence_text):
    """Calculates confidence based on lifespan indicators and exclusion keywords."""
    indicator_matches = sum(
        1 for phrase in LIFESPAN_INDICATORS if phrase in sentence_text
    )
    exclusion_matches = sum(1 for excl in EXCLUSION_KEYWORDS if excl in sentence_text)
    return (
        indicator_matches / (indicator_matches + 1)
        if indicator_matches > 0 and exclusion_matches == 0
        else 0
    )


def initialize_results():
    """Initialize the results dictionary."""
    return {
        "PERSON": [],
        "DATE": [],
        "GPE": [],
        "ORG": [],
        "NORP": [],
        "occupations": [],
        "lifespans": [],
        "relationships": [],
        "events": [],
    }


def deduplicate_records(records):
    """deduplicate_records"""
    unique = set()
    deduplicated = []
    for record in records:
        key = (record["book"], record["chapter"], record["verse"], record["type"])
        if key not in unique:
            unique.add(key)
            deduplicated.append(record)
    return deduplicated

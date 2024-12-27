# bible-analysis/core/tagger/lifespan_tagging.py

"""bible-analysis/core/tagger/lifespan_tagging.py"""

import re

from config.tagging_config import LIFESPAN_CONFIDENCE_THRESHOLD
from core.utils.tagging_utils import (
    calculate_confidence,
    get_context,
    initialize_results,
)


def tag_lifespan_phrases(doc, verse_text, unique_tags) -> dict[str, list]:
    """Detect lifespan phrases and include context."""
    res = initialize_results()

    person, years = None, None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person = ent.text
        elif ent.label_ in {"CARDINAL", "DATE"}:
            years = extract_numeric_value(ent.text)
            if years and person:
                confidence = calculate_confidence(verse_text.lower())
                if confidence > LIFESPAN_CONFIDENCE_THRESHOLD:
                    lifespan_key = (person, years)
                    if lifespan_key not in unique_tags:
                        context = get_context(doc, ent)
                        res["lifespans"].append(
                            {
                                "person": person,
                                "explicit lifespan": years,
                                "confidence": round(confidence, 2),
                                "trigger": f"'{person}' and '{years}'",
                                "context": context,
                            }
                        )
                        unique_tags.add(lifespan_key)
    return res["lifespans"]


def extract_numeric_value(verse_text):
    """Extracts a numeric value from verse_text if it’s purely numeric."""
    numeric_text = re.sub(r"[^\d]", "", verse_text)
    return int(numeric_text) if numeric_text.isdigit() else None

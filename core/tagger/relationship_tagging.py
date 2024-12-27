# bible-analysis/core/tagger/relationship_tagging.py

"""bible-analysis/core/tagger/relationship_tagging.py"""

from core.utils.tagging_utils import get_context, initialize_results
from config.tagging_config import RELATIONSHIP_KEYWORDS


def tag_relationships(doc, verse_text, unique_tags) -> dict[str, list]:
    """Detect relationships in the verse text."""
    res = initialize_results()

    for keyword in RELATIONSHIP_KEYWORDS:
        if keyword in verse_text.lower():
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    relationship_key = f"RELATIONSHIP-{ent.text.strip()}"
                    if relationship_key not in unique_tags:
                        res["relationships"].append(
                            {
                                "trigger": ent.text.strip(),
                                "context": get_context(doc, ent),
                            }
                        )
                        unique_tags.add(relationship_key)
    return res["relationships"]

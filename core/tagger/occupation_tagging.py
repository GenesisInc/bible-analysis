# bible-analysis/core/tagger/occupation_tagging.py

"""tag occupations."""

from config.tagging_config import occupation_keywords
from core.utils.tagging_utils import get_context, initialize_results


def tag_occupations(doc) -> dict[str, list]:
    """Tag occupations and include context."""
    res = initialize_results()

    res["OCCUPATION"] = [
        {"trigger": token.lemma_, "context": get_context(doc, token)}
        for token in doc
        if token.lemma_ in occupation_keywords
    ]

    return res["OCCUPATION"]

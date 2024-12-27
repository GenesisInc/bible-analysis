# bible-analysis/core/nlp_tagger/occupation_tagging.py

"""bible-analysis/core/nlp_tagger/occupation_tagging.py"""

from core.utils.tagging_utils import get_context, initialize_results

from config.tagging_config import occupation_keywords


def tag_occupations(doc) -> dict[str, list]:
    """Tag occupations and include context."""
    res = initialize_results()

    res["occupations"] = [
        {"trigger": token.lemma_, "context": get_context(doc, token)}
        for token in doc
        if token.lemma_ in occupation_keywords
    ]

    return res["occupations"]

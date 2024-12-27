# bible-analysis/core/nlp_tagger/event_tagging.py

""" bible-analysis/core/nlp_tagger/event_tagging.py"""

from config.tagging_config import EVENT_KEYWORDS
from core.utils.tagging_utils import get_context, initialize_results


def tag_events(doc) -> dict[str, list]:
    """Detect events in the document."""
    res = initialize_results()

    for token in doc:
        if token.text.lower() in EVENT_KEYWORDS:
            res["events"].append(
                {
                    "trigger": token.text.lower().strip(),
                    "context": get_context(doc, token),
                }
            )
    return res["events"]

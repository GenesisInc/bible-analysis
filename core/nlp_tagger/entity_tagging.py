# bible-analysis/core/nlp_tagger/entity_tagging.py

""" bible-analysis/core/nlp_tagger/entity_tagging.py"""
from core.utils.tagging_utils import get_context, initialize_results


def tag_named_entities(doc, unique_tags) -> dict[str, list]:
    """Tag named entities from the document, including context."""
    res = initialize_results()
    for ent in doc.ents:
        if ent.label_ in res:  # Match against top-level keys
            entity_key = (ent.label_, ent.text.strip())
            if entity_key not in unique_tags:
                context = get_context(doc, ent)
                res[ent.label_].append(
                    {"trigger": ent.text.strip(), "context": context}
                )
                unique_tags.add(entity_key)
    return res

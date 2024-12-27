# bible-analysis/commands/tag_entities.py
"""Command: tag-entities."""

from core.utils import file_utils, tagging_utils
from core.tagger.entity_tagging import tag_named_entities
from core.tagger.lifespan_tagging import tag_lifespan_phrases
from core.tagger.occupation_tagging import tag_occupations
from core.tagger.relationship_tagging import tag_relationships
from core.tagger.event_tagging import tag_events
from core.utils.logger_utils import get_logger

logger = get_logger(__name__)


def process_chapter(book, chapter_num, verses, translation):
    """Process a single chapter and tag its content."""
    chapter_results = {}
    for verse_num, verse_text in verses.items():
        doc = tagging_utils.nlp(verse_text)  # Load NLP model once per verse

        unique_tags = set()
        chapter_results[str(verse_num)] = {}
        chapter_results[str(verse_num)] = tag_named_entities(doc, unique_tags)
        chapter_results[str(verse_num)]["occupations"] = tag_occupations(doc)
        chapter_results[str(verse_num)]["lifespans"] = tag_lifespan_phrases(
            doc,
            verse_text,
            unique_tags,
        )
        chapter_results[str(verse_num)]["relationships"] = tag_relationships(
            doc, verse_text, unique_tags
        )
        chapter_results[str(verse_num)]["events"] = tag_events(doc)

    return chapter_results


def perform_entity_analysis(input_file, output_json, output_csv, translation, books):
    """Perform entity analysis using modular taggers."""
    bible_data = file_utils.load_from_json(input_file)
    combined_results = []

    for book, chapters in bible_data[translation].items():
        if books and book not in books:
            continue

        for chapter_num, verses in chapters.items():
            chapter_results = process_chapter(book, chapter_num, verses, translation)

            # Flatten and deduplicate chapter results
            flat_results = flatten_chapter_results(chapter_results, book, chapter_num)
            deduplicated_results = tagging_utils.deduplicate_records(flat_results)

            combined_results.extend(deduplicated_results)

    # Save results
    file_utils.save_to_json(combined_results, output_json)
    file_utils.save_combined_results_to_csv(combined_results, output_csv)

    logger.debug(
        "Entity analysis completed. Results saved to %s and %s", output_json, output_csv
    )


def flatten_chapter_results(chapter_results, book, chapter_num):
    """Flatten chapter results into a list of records."""
    flat_results = []
    for verse_num, results in chapter_results.items():
        if not isinstance(results, dict):  # Debug unexpected data structure
            raise ValueError(f"Expected results as a dict but got {type(results)}")
        for result_type, items in results.items():
            for item in items:
                if not isinstance(item, dict):  # Debug unexpected data structure
                    raise ValueError(
                        f"Expected item as a dict but got {type(item)},\nitem: {item}"
                    )

                # pull out these and remove from item
                trigger = item["trigger"]
                context = item["context"]

                # remove below to avoid duplicates in "extras"
                del item["context"]
                del item["trigger"]

                flat_results.append(
                    {
                        "book": book,
                        "chapter": chapter_num,
                        "verse": verse_num,
                        "type": result_type,
                        "trigger": trigger,
                        "context": context,
                        "extras": item,
                    }
                )

    return flat_results

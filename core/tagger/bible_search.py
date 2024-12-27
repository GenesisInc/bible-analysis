# bible-analysis/core/tagger/bible_search.py
""" search text / phrases in bible  """

import csv
import json
import re
import sys

from core.utils.logger_utils import get_logger

logger = get_logger(__file__.rsplit("/", 1)[-1])


def load_bible_data(bible_json_path):
    """Load Bible data from JSON file."""
    with open(bible_json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def search_bible(bible_data, regex, translation="nwt"):
    """Search for matches in the Bible text using a regex."""
    matches = []
    logger.debug("searching for regex: '%s'", regex)
    for book, chapters in bible_data[translation].items():
        for chapter, verses in chapters.items():
            for verse, text in verses.items():
                if re.search(regex, text, re.IGNORECASE):  # Match based on regex
                    matches.append(
                        {
                            "book": book,
                            "chapter": chapter,
                            "verse": verse,
                            "text": text,
                        }
                    )
    return matches


def write_csv_output(matches, total_matches, translation):
    """Write matches to stdout in CSV format."""
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["book", "chapter", "verse", "text"],
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writeheader()
    writer.writerows(matches)

    # Print summary to stderr to separate it from CSV output
    print(
        f"Showing top {len(matches)} of {total_matches}"
        + f" matches from '{translation}' translation",
        file=sys.stderr,
    )


def find_matches(
    bible_json_path, phrase, translation="nwt", top_n=10, output_csv=False
):
    """Find top matches for a phrase in Bible text."""
    bible_data = load_bible_data(bible_json_path)

    # Normalize input and compile regex
    phrase = phrase.strip().lower()
    regex = rf"{re.escape(phrase)}"  # Match substrings both single or multiple words

    # Search the Bible
    matches = search_bible(bible_data, regex, translation)

    # Total matches
    total_matches = len(matches)

    # Sort and limit matches
    sorted_matches = sorted(matches, key=lambda x: len(x["text"]))[:top_n]

    if output_csv:
        write_csv_output(sorted_matches, total_matches, translation)
        return None  # Explicitly return None for consistency

    print(
        f"Showing top {len(sorted_matches)} of {total_matches}"
        + f"matches from '{translation}' translation"
    )
    return sorted_matches

# bible-analysis/core/nlp_tagger/reference_extrator.py
"""entity analysis extract few entities from bible"""

import json

from core.utils.logger_utils import get_logger

logger = get_logger(__file__.rsplit("/", 1)[-1])


# called by main.py->Cmd.extract_reference
def extract_reference(bible_json_path, reference, translation):
    """Extracts text for a given Bible reference."""
    with open(bible_json_path, "r", encoding="utf-8") as file:
        bible_data = json.load(file)

    # Use the previously defined `get_bible_text` function
    return get_bible_text(reference, bible_data, translation)


def parse_reference(reference):
    """
    Parses a Bible reference string into book, chapter, and verse details.

    Special cases:
    - Single-chapter books (like Jude): Prefix "1:" to standalone verse numbers or ranges.
    """
    reference = reference.strip()
    if not reference:
        raise ValueError("Invalid reference format")

    # Step 1: Split by space to separate book and reference
    parts = reference.rsplit(" ", 1)
    if len(parts) == 1:
        # Only the book name is provided
        book = parts[0].lower()
        rest = ""
    else:
        book = parts[0].lower()
        rest = parts[1]  # This contains chapter:verse or a range

    # Step 2: Handle single-chapter books
    single_chapter_books = {"jude", "philemon", "2 john", "3 john"}
    if book in single_chapter_books:
        if "-" in rest:  # Range like "4-8"
            start, end = rest.split("-")
            if ":" not in start:
                start = f"1:{start}"  # Prefix chapter 1
            if ":" not in end:
                end = f"1:{end}"  # Prefix chapter 1
            rest = f"{start}-{end}"
        elif ":" not in rest:  # Single verse like "4"
            rest = f"1:{rest}"  # Prefix chapter 1

    return book, rest


def get_bible_text(reference, bible_data, translation):
    """Extracts Bible text based on a reference string."""
    try:
        book, verses = parse_reference(reference)
        if not verses:
            # Return the whole book
            return fetch_entire_book(bible_data, book)

        start_chapter, start_verse, end_chapter, end_verse = parse_verse_range(verses)
        return fetch_verses(
            bible_data,
            translation,
            book,
            start_chapter,
            start_verse,
            end_chapter,
            end_verse,
        )
    except KeyError as e:
        return f"Error: Missing key in Bible data - {str(e)}"
    except ValueError as e:
        return f"Error: Invalid reference format - {str(e)}"
    except TypeError as e:
        return f"Error: Type error encountered - {str(e)}"


def fetch_verses(
    bible_data, translation, book, start_chapter, start_verse, end_chapter, end_verse
):
    """Fetches verses across chapter and verse ranges."""
    result = []
    for chapter in range(start_chapter, end_chapter + 1):
        chapter_key = str(chapter)
        if chapter_key not in bible_data[translation].get(book, {}):
            continue

        verse_start = start_verse if chapter == start_chapter else 1
        verse_end = (
            end_verse
            if chapter == end_chapter
            else max(map(int, bible_data[translation][book][chapter_key].keys()))
        )

        for verse in range(verse_start, verse_end + 1):
            verse_key = str(verse)
            if verse_key in bible_data[translation][book][chapter_key]:
                result.append(bible_data[translation][book][chapter_key][verse_key])

    return " ".join(result)


def fetch_entire_book(bible_data, book):
    """Fetches all chapters and verses of a book."""
    result = []
    book_data = bible_data["nwt"].get(book, {})
    for chapter_key in sorted(book_data.keys(), key=int):
        chapter_data = book_data[chapter_key]
        for _, verse_text in sorted(chapter_data.items(), key=lambda x: int(x[0])):
            result.append(verse_text)
    return " ".join(result)


def parse_verse_range(verses):
    """Parses a verse range into start and end chapter/verse."""
    if "-" in verses:
        start, end = verses.split("-")
        start_chapter, start_verse = map(int, start.split(":"))
        if ":" in end:
            end_chapter, end_verse = map(int, end.split(":"))
        else:
            end_chapter = start_chapter
            end_verse = int(end)
    elif ":" in verses:
        start_chapter, start_verse = map(int, verses.split(":"))
        end_chapter, end_verse = start_chapter, start_verse
    else:
        start_chapter = int(verses)
        start_verse = 1
        end_chapter, end_verse = start_chapter, None
    return start_chapter, start_verse, end_chapter, end_verse

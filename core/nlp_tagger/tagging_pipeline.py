"""entity analysis extract few entities from bible"""

# bible-analysis/core/nlp_tagger/tagging_pipeline.py

import csv
import json
import os
import re
import unicodedata
from multiprocessing import Pool
from pathlib import Path

import spacy

from core.utils import file_utils
from core.utils.logger_utils import get_logger

logger = get_logger(__file__.rsplit("/", 1)[-1])

# Load spaCy model
nlp = spacy.load("en_core_web_sm", disable=["parser"])

# Constants
OUTPUT_DIR = Path("analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# BASE_PATH = "../newWorldTranslation/english/2013-release"

EXCLUSION_KEYWORDS = {"reigned", "gathered to", "length of", "satisfied with years"}
# LIFESPAN_INDICATORS = {"lived for", "was", "amounted to", "were", "to be"}
LIFESPAN_INDICATORS = {"lived for", "became father to", "amounted to", "died at age"}


# Occupation keywords for matching
occupation_keywords = {
    "apothecary",
    "architect",
    "armor maker",
    "armor-bearer",
    "astrologer",
    "astronomer",
    "baker",
    "beggar",
    "blacksmith",
    "builder of city walls",
    "camel driver",
    "caretaker of sacred items",
    "carpenter",
    "charioteer",
    "chief of army",
    "choir member",
    "cook",
    "cupbearer",
    "cupmaker",
    "dancer",
    "dealer in purple cloth",
    "dyer",
    "elder",
    "executioner",
    "farmer",
    "fisher",
    "fisherman",
    "flock herder",
    "gatekeeper",
    "goldsmith",
    "governor",
    "harvester",
    "herder",
    "high priest",
    "horseman",
    "hunter",
    "judge",
    "king",
    "lawyer",
    "linen worker",
    "mason",
    "merchant",
    "metalworker",
    "midwife",
    "miller",
    "musician",
    "perfumer",
    "physician",
    "potter",
    "priest’s assistant",
    "priest",
    "prophet",
    "queen",
    "sandal maker",
    "scout",
    "scribe",
    "servant",
    "shepherd",
    "shipbuilder",
    "shipmaster",
    "singer",
    "slave",
    "slavegirl",
    "soldier",
    "spy",
    "stonecutter",
    "tax collector",
    "teacher",
    "temple servant",
    "tent weaver",
    "tent-dweller",
    "tentmaker",
    "trader",
    "vineyard keeper",
    "weaver",
    "winemaker",
}


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


def load_bible_json(file_path):
    """Loads the Bible JSON data."""
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def tag_chapter_entities(chapter_data):
    """Extracts entities and occupations for all verses in a chapter."""
    chapter_entities = {
        verse_num: {
            "entities": {"PERSON": [], "DATE": [], "GPE": [], "ORG": [], "NORP": []},
            "occupations": [],
        }
        for verse_num in chapter_data
    }

    # Process each verse in the chapter
    for verse_num, doc in zip(
        chapter_data.keys(), nlp.pipe(chapter_data.values(), batch_size=50)
    ):
        for ent in doc.ents:
            # Extract named entities
            if ent.label_ == "PERSON" and ent.text.strip()[0].isupper():
                chapter_entities[verse_num]["entities"]["PERSON"].append(
                    ent.text.strip()
                )
            elif ent.label_ in chapter_entities[verse_num]["entities"]:
                chapter_entities[verse_num]["entities"][ent.label_].append(
                    ent.text.strip()
                )

        # Extract occupations (use lemma to ensure consistent forms)
        occupations = [
            token.lemma_ for token in doc if token.lemma_ in occupation_keywords
        ]
        chapter_entities[verse_num]["occupations"].extend(occupations)

    return chapter_entities


# Multiprocessing-friendly wrapper for chapter processing
def process_chapter(args):
    """Processes a single chapter for multiprocessing."""
    book, chapter_num, chapter_data = args
    chapter_results = {
        verse_num: tag_entities_and_lifespan(verse_text, book, chapter_num, verse_num)
        for verse_num, verse_text in chapter_data.items()
    }
    return book, chapter_num, chapter_results


def perform_entity_analysis(
    bible_file, output_json_file, output_csv_file, translation="nwt", books=None
):
    """Extract entities, occupations, and lifespans using multiprocessing."""
    # Step 1: Load Bible data
    logger.debug("Loading Bible data from %s", bible_file)
    bible_data = load_bible_json(bible_file)

    # Step 2: Prepare tasks for multiprocessing
    tasks = prepare_tasks(bible_data, translation, books)

    # Step 3: Process tasks in parallel
    results = process_tasks_parallel(tasks)

    # Step 4: Reorganize results into a nested JSON structure
    combined_results = reorganize_results(results)

    # Step 5: Save JSON output
    file_utils.save_to_json(combined_results, output_json_file)

    # Step 6: Save CSV output
    save_combined_results_to_csv(combined_results, output_csv_file)


def save_combined_results_to_csv(data, output_csv_file):
    """Save entities, occupations, and lifespan details to a CSV file."""
    with open(output_csv_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Book", "Chapter", "Verse", "Type", "Text"])

        for book, chapters in data.items():
            for chapter, verses in chapters.items():
                for verse_num, results in verses.items():
                    # Write entities
                    for entity_type, entity_list in results["entities"].items():
                        for entity in entity_list:
                            writer.writerow(
                                [book, chapter, verse_num, entity_type, entity]
                            )

                    # Write occupations
                    for occupation in results["occupations"]:
                        writer.writerow(
                            [book, chapter, verse_num, "OCCUPATION", occupation]
                        )

                    # Write lifespans
                    for lifespan in results["lifespans"]:
                        writer.writerow(
                            [
                                book,
                                chapter,
                                verse_num,
                                "LIFESPAN",
                                lifespan["Context"]["Text"],
                            ]
                        )


def prepare_tasks(bible_data, translation, books):
    """Prepares tasks for multiprocessing."""
    return [
        (book, chapter_num, chapter_data)
        for book, chapters in bible_data[translation].items()
        if not books or book in books
        for chapter_num, chapter_data in chapters.items()
    ]


def process_tasks_parallel(tasks):
    """Processes tasks in parallel using multiprocessing."""
    with Pool() as pool:
        return pool.map(process_chapter, tasks)


def reorganize_results(results):
    """Reorganizes the results into a nested JSON structure."""
    entities_and_occupations = {}
    for book, chapter_num, chapter_data in results:
        if book not in entities_and_occupations:
            entities_and_occupations[book] = {}
        entities_and_occupations[book][chapter_num] = chapter_data
    return entities_and_occupations


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


def tag_entities_and_lifespan(verse_text, book, chapter, verse_num):
    """Extract entities, occupations, and lifespan details from a verse."""
    doc = nlp(verse_text)
    results = {
        "entities": {"PERSON": [], "DATE": [], "GPE": [], "ORG": [], "NORP": []},
        "occupations": [],
        "lifespans": [],
    }

    # Tag named entities
    for ent in doc.ents:
        if ent.label_ in results["entities"]:
            results["entities"][ent.label_].append(ent.text.strip())

    # Detect occupations
    results["occupations"] = [
        token.lemma_ for token in doc if token.lemma_ in occupation_keywords
    ]

    # Detect lifespan phrases
    person, years = None, None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person = ent.text
        elif ent.label_ in {"CARDINAL", "DATE"}:
            years = extract_numeric_value(ent.text)
            if years and person:
                confidence = calculate_confidence(verse_text.lower())
                if confidence > 0:
                    results["lifespans"].append(
                        {
                            "Person": person,
                            "Explicit Lifespan": years,
                            "Confidence": round(confidence, 2),
                            "Context": {
                                "Reference": get_reference(book, chapter, verse_num),
                                "Text": verse_text,
                            },
                        }
                    )

    return results


def normalize_unicode(text):
    """Cleans up Unicode characters, standardizes spaces, and trims around punctuation."""
    # Define replacements in a dictionary for flexibility and readability
    replacements = {
        "\u00A0": " ",  # Non-breaking space to regular space
        "\n": " ",  # Newline to space
        "\u2019": "'",  # Right single quotation mark to apostrophe
        "\u02b9": "",  # Modifier letter prime (remove)
        "\u00b7": "",  # Middle dot (remove)
    }

    # Apply replacements using the dictionary
    for unicode_char, replacement in replacements.items():
        text = text.replace(unicode_char, replacement)

    # Normalize to ASCII, removing accents and other diacritics
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    # Remove extra spaces around punctuation and collapse multiple spaces
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)  # Remove space before punctuation
    text = re.sub(r"\s{2,}", " ", text).strip()  # Collapse multiple spaces to single

    return text


def get_reference(book, chapter, verse_num):
    """Generates a verse reference in 'Book Chapter:Verse' format."""
    # book_name = book.split("-")[1]
    return f"{book} {int(chapter)}:{verse_num}"


def extract_numeric_value(verse_text):
    """Extracts a numeric value from verse_text if it’s purely numeric."""
    numeric_text = re.sub(r"[^\d]", "", verse_text)
    return int(numeric_text) if numeric_text.isdigit() else None


def detect_lifespan_phrases(verse_text, book, chapter, verse_num):
    """Detect lifespan-related phrases in a verse."""
    lifespans = []

    # Process the verse text for lifespan phrases
    doc = nlp(verse_text)
    person, years = None, None

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person = ent.text
        elif ent.label_ in {"CARDINAL", "DATE"}:
            years = extract_numeric_value(ent.text)
            if years and person:  # Ensure both person and years are available
                confidence = calculate_confidence(verse_text.lower())
                if confidence > 0:
                    lifespans.append(
                        {
                            "Person": person,
                            "Explicit Lifespan": years,
                            "Confidence": round(confidence, 2),
                            "Context": {
                                "Reference": get_reference(book, chapter, verse_num),
                                "Text": verse_text,
                            },
                        }
                    )

    return lifespans


def process_lifespan(input_file, json_output, csv_output):
    """Process lifespan statements and update results."""
    # Load Bible data from JSON file
    with open(input_file, "r", encoding="utf-8") as file:
        bible_data = json.load(file)

    # Load existing JSON data if available
    if os.path.exists(json_output):
        with open(json_output, "r", encoding="utf-8") as json_file:
            combined_data = json.load(json_file)
    else:
        combined_data = {}

    # Prepare to update the CSV
    csv_exists = os.path.exists(csv_output)
    csv_file = open(csv_output, "a", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)

    # Write header if CSV does not exist
    if not csv_exists:
        csv_writer.writerow(["Book", "Chapter", "Verse", "Type", "Text"])

    # Navigate the structure (e.g., "nwt")
    for _, books in bible_data.items():
        for book, chapters in books.items():
            for chapter, verses in chapters.items():
                for verse_num, verse_text in verses.items():
                    verse_text = normalize_unicode(verse_text)
                    lifespans = detect_lifespan_phrases(
                        verse_text, book, chapter, verse_num
                    )

                    # Ensure the JSON structure is initialized properly
                    book_data = combined_data.setdefault(book, {})
                    chapter_data = book_data.setdefault(chapter, {})
                    verse_data = chapter_data.setdefault(
                        verse_num,
                        {
                            "entities": {
                                "PERSON": [],
                                "DATE": [],
                                "GPE": [],
                                "ORG": [],
                                "NORP": [],
                            },
                            "occupations": [],
                            "lifespans": [],
                        },
                    )

                    # Append lifespan data
                    if "lifespans" not in verse_data:
                        verse_data["lifespans"] = []  # Ensure the key exists

                    for lifespan in lifespans:
                        verse_data["lifespans"].append(lifespan)
                        # Update CSV
                        csv_writer.writerow(
                            [
                                book,
                                chapter,
                                verse_num,
                                "LIFESPAN",
                                lifespan["Context"]["Text"],
                            ]
                        )

    # Save updated JSON
    with open(json_output, "w", encoding="utf-8") as json_file:
        json.dump(combined_data, json_file, indent=2, ensure_ascii=True)

    # Close the CSV file
    csv_file.close()


def save_results(data, data_type):
    """Saves results to JSON and CSV files based on data type."""
    json_path = OUTPUT_DIR / f"{data_type}.json"
    csv_path = OUTPUT_DIR / f"{data_type}.csv"

    # Save JSON file
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=True)

    # Save CSV file
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        if data_type == "entities":
            # Header for entities
            writer.writerow(
                [
                    "Book",
                    "Chapter",
                    "Entity_Type",
                    "Entity_Name",
                    "Count",
                    "Verse",
                    "Context",
                ]
            )
            for book, chapters in data.items():
                for chapter, entities in chapters.items():
                    for entity_type, names in entities.items():
                        for name, entity_data in names.items():
                            for context in entity_data["Context"]:
                                writer.writerow(
                                    [
                                        book,
                                        chapter,
                                        entity_type,
                                        name,
                                        entity_data["Count"],
                                        context["Reference"],
                                        context["Text"],
                                    ]
                                )
        elif data_type == "lifespans":
            # Header for lifespans
            writer.writerow(
                [
                    "Book",
                    "Chapter",
                    "Person",
                    "Explicit Lifespan",
                    "Confidence",
                    "Verse",
                    "Context",
                ]
            )
            for book, chapters in data.items():
                for chapter, lifespans in chapters.items():
                    for person, lifespan_entries in lifespans.items():
                        for entry in lifespan_entries:
                            writer.writerow(
                                [
                                    book,
                                    chapter,
                                    person,
                                    entry["Explicit Lifespan"],
                                    entry["Confidence"],
                                    entry["Context"]["Reference"],
                                    entry["Context"]["Text"],
                                ]
                            )
        else:
            print(f"Unsupported data type: {data_type}.")
            print("Only 'entities' and 'lifespans' are supported.")

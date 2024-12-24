""" test bible module"""

import unittest

import pytest
import spacy

from core.nlp_tagger.lifespan_tagger import extract_context, tag_entities_from_verse
from core.nlp_tagger.tagger import extract_reference, parse_reference

# Load spaCy's English NLP model for testing
nlp = spacy.load("en_core_web_sm")


def test_parse_reference_valid_cases():
    """Test valid Bible reference parsing with right-to-left approach."""
    # Single-word book names
    assert parse_reference("Genesis 1:1") == ("genesis", "1:1")

    # Multi-word book names
    assert parse_reference("1 John 1:3") == ("1 john", "1:3")
    assert parse_reference("Song of Solomon 2:4") == ("song of solomon", "2:4")

    # Multi-word book names with range
    assert parse_reference("1 Samuel 3:2-3:2") == ("1 samuel", "3:2-3:2")

    # Edge case: Only book name
    assert parse_reference("Exodus") == ("exodus", "")


def test_parse_reference_invalid_cases():
    """Test invalid Bible reference parsing."""
    with pytest.raises(ValueError, match="Invalid reference format"):
        parse_reference("")  # Empty string

    with pytest.raises(ValueError, match="Invalid reference format"):
        parse_reference(" ")  # Whitespace only


def test_parse_reference_single_chapter_books():
    """Test references for single-chapter books."""
    # Single-chapter books with just a verse number
    assert parse_reference("Jude 1") == ("jude", "1:1")
    assert parse_reference("Philemon 5") == ("philemon", "1:5")
    assert parse_reference("2 John 3") == ("2 john", "1:3")
    assert parse_reference("3 John 8") == ("3 john", "1:8")

    # Single-chapter books with explicit chapter and verse
    assert parse_reference("Jude 1:1") == ("jude", "1:1")
    assert parse_reference("Philemon 1:5") == ("philemon", "1:5")


def test_parse_reference_edge_cases():
    """Test edge cases for single-chapter books and ranges."""
    # Single-chapter books with standalone verses
    assert parse_reference("Jude 4") == ("jude", "1:4")
    assert parse_reference("2 John 4") == ("2 john", "1:4")

    # Single-chapter books with ranges
    assert parse_reference("Jude 4-8") == ("jude", "1:4-1:8")
    assert parse_reference("2 John 4-8") == ("2 john", "1:4-1:8")

    # Explicit chapter/verse references (no prefixing needed)
    assert parse_reference("Jude 1:4") == ("jude", "1:4")
    assert parse_reference("2 John 1:4-1:8") == ("2 john", "1:4-1:8")


def test_single_verse(mocker):
    """test_single_verse"""
    mocker.patch(
        "builtins.open",
        mocker.mock_open(
            read_data='{"nwt": {"genesis": {"1": {"1": "In the beginning God created the heavens and the earth."}}}}'
        ),
    )
    ref = "Genesis 1:1"
    result = extract_reference("path/to/bible.json", ref, "nwt")
    assert result == "In the beginning God created the heavens and the earth."


def test_verse_range(mocker):
    """test_verse_range"""
    mock_data = '{"nwt": {"genesis": {"1": {"5": "God called the light Day.", "6": "And God said, Let there be a firmament.", "7": "God made the expanse and separated the waters."}}}}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))
    ref = "Genesis 1:5-7"
    result = extract_reference("path/to/bible.json", ref, "nwt")
    assert "God called the light Day." in result and "God made the expanse" in result


def test_multiple_chapters(mocker):
    """test_multiple_chapters"""
    mock_data = '{"nwt": {"genesis": {"1": {"7": "God made the expanse.", "8": "God called the expanse Heaven."}, "2": {"1": "The heavens and the earth were completed.", "3": "God blessed the seventh day."}}}}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))
    ref = "Genesis 1:7-2:3"
    result = extract_reference("path/to/bible.json", ref, "nwt")
    assert (
        "God made the expanse." in result and "God blessed the seventh day." in result
    )


def test_book_with_number(mocker):
    """test_book_with_number"""
    mock_data = '{"nwt": {"1 john": {"1": {"3": "That which we have seen and heard"}}}}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))
    ref = "1 John 1:3"
    result = extract_reference("path/to/bible.json", ref, "nwt")
    assert "That which we have seen and heard" in result


def test_cross_chapter_single_verse(mocker):
    """test_cross_chapter_single_verse"""
    mock_data = (
        '{"nwt": {"1 samuel": {"3": {"2": "The lamp of God had not yet gone out."}}}}'
    )
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))
    ref = "1 Samuel 3:2-3:2"
    result = extract_reference("path/to/bible.json", ref, "nwt")
    assert "The lamp of God had not yet gone out." in result


def test_invalid_reference(mocker):
    """test_invalid_reference"""
    mocker.patch("builtins.open", mocker.mock_open(read_data="{}"))
    ref = "Invalid Reference"
    result = extract_reference("path/to/bible.json", ref, "nwt")
    assert "Error: Invalid reference format" in result


class TestMain(unittest.TestCase):
    """test main module"""

    def test_possessive_handling(self):
        """Test that possessive phrases are handled correctly."""
        text = "This is the history of Noah’s sons, Shem, Ham, and Japheth."
        doc = nlp(text)
        # Emulate entity recognition for "Shem"
        start, end = 5, 6  # Position of "Shem" in tokenized text
        context = extract_context(text, start, end)
        expected_context = "the history of Noah's sons, Shem, Ham"
        self.assertEqual(context, expected_context)

    def test_dangling_possessive(self):
        """Test that possessive phrases starting with a dangling "'s" are not misrepresented."""
        text = "His brother’s name was Jubal. He was the founder of all those who play the harp and the pipe."
        doc = nlp(text)
        # Emulate entity recognition for "Jubal"
        start, end = 4, 5  # Position of "Jubal" in tokenized text
        context = extract_context(text, start, end)
        expected_context = "His brother's name was Jubal. He"
        self.assertEqual(context, expected_context)

    def test_context_extraction(self):
        """Test general context extraction to ensure surrounding words are correctly captured."""
        text = "Adam's life was long and fulfilling, with many generations to come."
        doc = nlp(text)
        # Emulate entity recognition for "Adam"
        start, end = 0, 1  # Position of "Adam" in tokenized text
        context = extract_context(text, start, end)
        expected_context = "Adam's life was"
        self.assertEqual(context, expected_context)

    def test_entity_extraction_with_reference(self):
        """Test entity extraction function to ensure references are handled accurately."""
        verse_text = "This is the history of Noah’s sons, Shem, Ham, and Japheth."
        verse_num = 1
        entities = {"PERSON": {}}
        book = "01-Genesis"
        chapter = "010"
        tag_entities_from_verse(verse_text, verse_num, entities, book, chapter)

        # Expected output in entities dict
        expected_output = {
            "PERSON": {
                "Noah": {
                    "Count": 1,
                    "Context": [
                        {
                            "Reference": "Genesis 10:1",
                            "Text": "the history of Noah's sons",
                        }
                    ],
                },
                "Shem": {
                    "Count": 1,
                    "Context": [
                        {"Reference": "Genesis 10:1", "Text": "Noah's sons, Shem, Ham"}
                    ],
                },
            }
        }

        self.assertEqual(entities, expected_output)


if __name__ == "__main__":
    unittest.main()

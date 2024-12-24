"""manipulator - merge & extract json"""

# bible-analysis/core/translation_loader/translation_manager.py

from core.utils.logger_utils import get_logger

logger = get_logger(__file__.rsplit("/", 1)[-1])


def extract_translation(multi_translation_data, translation_name):
    """
    Extracts a specific translation from the multi-translation format to single-translation format.

    Args:
        multi_translation_data (dict): Multi-translation JSON data.
        translation_name (str): Translation key to extract (e.g., "asv", "kj21", "nwt").

    Returns:
        dict: Single-translation format JSON with the specified translation.
    """
    single_translation_data = {}

    logger.debug("extracting '%s' from '%s", translation_name, multi_translation_data)
    for book, chapters in multi_translation_data.items():
        if book not in single_translation_data:
            single_translation_data[book] = {}

        for chapter, verses in chapters.items():
            if chapter not in single_translation_data[book]:
                single_translation_data[book][chapter] = {}

            for verse, translations in verses.items():
                if translation_name in translations:
                    single_translation_data[book][chapter][verse] = translations[
                        translation_name
                    ]

    return {translation_name: single_translation_data}

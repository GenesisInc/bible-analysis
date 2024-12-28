# bible-analysis/cli/parsers_extract.py
def setup_extract_parser(subparsers):
    """Prepare extract parser."""
    translation_parser = subparsers.add_parser(
        "extract",
        help="Extract a specific translation from the multi-translation JSON.",
    )
    translation_parser.add_argument(
        "--input-file",
        type=str,
        default="data/multi_translation.json",
        help="Input JSON file for multi-translation Bible data (default: %(default)s).",
    )
    translation_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        help="Translation to extract (e.g., 'asv', 'kj21', 'nwt').",
    )
    translation_parser.add_argument(
        "--output-file",
        type=str,
        default="data/extracted_translation.json",
        help="Output JSON file for extracted translation (default: %(default)s).",
    )

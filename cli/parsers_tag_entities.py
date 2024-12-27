# bible-analysis/cli/parsers_tag_entities.py
def setup_tag_entities_parser(subparsers):
    """Set up tag-entities parser."""
    extract_parser = subparsers.add_parser(
        "tag-entities",
        help="Extract entities, occupations, and lifespans from Bible JSON data.",
    )
    extract_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file for Bible data (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--output-json",
        type=str,
        default="data/output/bible_entities.json",
        help="Output JSON file for extracted entities (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--output-csv",
        type=str,
        default="data/output/bible_entities.csv",
        help="Output CSV file for extracted entities (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--books",
        type=str,
        nargs="*",
        help="Specify one or more books to extract entities from (e.g., genesis exodus).",  # noqa: E501
    )
    extract_parser.add_argument(
        "--translation",
        type=str,
        default="nwt",
        help="Bible translation, e.g., nwt | asv | kj21",
    )

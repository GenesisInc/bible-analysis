# bible-analysis/cli/parsers_reference.py
def setup_reference_parser(subparsers):
    """Prepare reference parser."""
    reference_parser = subparsers.add_parser(
        "reference",
        help="Extract text for a specific Bible reference.",
    )
    reference_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file for Bible data (default: %(default)s).",
    )
    reference_parser.add_argument(
        "--reference",
        type=str,
        required=True,
        help="Bible reference to extract (e.g., 'Gen 1:1', 'John 3:16').",
    )
    reference_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        help="Bible translation, ex: nwt | asv | kj21 ",
    )

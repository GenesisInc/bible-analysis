# bible-analysis/cli/parsers_search.py
def setup_search_parser(subparsers):
    """Prepare search parser."""
    search_parser = subparsers.add_parser(
        "search",
        help="Search for a phrase in the Bible text and display matches.",
    )
    search_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file for Bible data (default: %(default)s).",
    )
    search_parser.add_argument(
        "--phrase",
        type=str,
        required=True,
        help="Phrase to search for in the Bible text.",
    )
    search_parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of top matches to display (default: %(default)s).",
    )
    search_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        help="Bible translation, ex: nwt | asv | kj21 ",
    )
    search_parser.add_argument(
        "--csv", action="store_true", help="Output the results in CSV format."
    )

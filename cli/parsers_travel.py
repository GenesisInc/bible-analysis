# bible-analysis/cli/parsers_travel.py
def setup_travel_parser(subparsers):
    """Prepare travel parser."""
    reference_parser = subparsers.add_parser(
        "trips",
        help="view travels",
    )
    reference_parser.add_argument(
        "--input-file",
        type=str,
        default="data/input/travel/journey_data.json",
        help="vivew travel map (default: %(default)s).",
    )
    reference_parser.add_argument(
        "--output-file",
        type=str,
        default="data/output/travel-maps.csv",
        help="vivew travel map (default: %(default)s).",
    )

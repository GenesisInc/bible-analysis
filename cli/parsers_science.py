# bible-analysis/cli/parsers_science.py
def setup_timeline_parser(subparsers):
    """Set up timeline parser for generating charts."""
    timeline_parser = subparsers.add_parser(
        "science",
        help="Generate timeline charts for scientific and biblical events.",
    )
    timeline_parser.add_argument(
        "--input-file",
        type=str,
        default="data/input/science/facts.json",
        help="Input CSV file for timeline data (default: %(default)s).",
    )
    timeline_parser.add_argument(
        "--add-event",
        action="store_true",
        help="Add a new event to the timeline data.",
    )
    timeline_parser.add_argument(
        "--item",
        type=str,
        help="Name of the event (e.g., 'The Expanding Universe').",
    )
    timeline_parser.add_argument(
        "--category",
        type=str,
        help="Category of the event (e.g., 'Cosmology').",
    )
    timeline_parser.add_argument(
        "--bible-reference",
        type=str,
        help="Bible reference associated with the event (e.g., 'Isaiah 40:22').",
    )
    timeline_parser.add_argument(
        "--recorded-timeframe",
        type=int,
        help="Timeframe when the event was recorded (e.g., -700).",
    )
    timeline_parser.add_argument(
        "--scientific-comment-year",
        type=int,
        help="Year when scientists commented on the event (e.g., 1929).",
    )
    timeline_parser.add_argument(
        "--confirmed",
        type=bool,
        help="Whether the detail is confirmed by scientists (True/False).",
    )
    timeline_parser.add_argument(
        "--scientific-commentary",
        type=str,
        help="Details of the scientific commentary.",
    )

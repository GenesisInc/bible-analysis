# bible-analysis/cli/parsers.py
"""CLI argument parsers."""

import argparse

from .parsers_extract import setup_extract_parser
from .parsers_reference import setup_reference_parser
from .parsers_science import setup_timeline_parser
from .parsers_search import setup_search_parser
from .parsers_tag_entities import setup_tag_entities_parser
from .parsers_travel import setup_travel_parser


def setup_parsers():
    """Set up argument parsers for all sub-commands."""
    parser = argparse.ArgumentParser(
        description="CLI to process Bible text, extract entities, and perform searches."
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Add parsers for each command
    setup_tag_entities_parser(subparsers)
    setup_search_parser(subparsers)
    setup_reference_parser(subparsers)
    setup_extract_parser(subparsers)
    setup_travel_parser(subparsers)
    setup_timeline_parser(subparsers)

    return parser

# bible-analysis/commands/handle_command.py
"""Command handler."""

import json

from commands.extract import extract_translation
from commands.mapper import map_travel
from commands.reference import extract_reference
from commands.search import search_bible
from commands.tag_entities import perform_entity_analysis
from core.utils.file_utils import load_from_json
from core.utils.logger_utils import get_logger
from core.utils.text_utils import parse_year
from core.visuals import visualizer

logger = get_logger(__file__.rsplit("/", 1)[-1])


def handle_command(args):  # noqa: C901
    """Handle the parsed command."""
    if args.command == "tag-entities":
        logger.debug("Starting entity tagging for %s", args.input_file)
        perform_entity_analysis(
            args.input_file,
            args.output_json,
            args.output_csv,
            args.translation,
            books=args.books,
        )
    elif args.command == "search":
        logger.debug("Searching for phrase: '%s' in %s", args.phrase, args.input_file)

        matches = search_bible(args)
        if not args.csv:
            for match in matches:
                print(
                    f"{match['book']} {match['chapter']}:{match['verse']} - {match['text']}"  # noqa: E501
                )
        logger.debug("Search completed.")
        if matches:
            logger.debug("Found %d matches.", len(matches))
    elif args.command == "reference":
        result = extract_reference(args.input_file, args.reference, args.translation)
        print(result)
    elif args.command == "trips":
        map_travel(args.input_file)
    elif args.command == "extract":
        with open(args.input_file) as f:
            multi_translation_data = json.load(f)

        single_translation_data = extract_translation(
            multi_translation_data, args.translation
        )

        with open(args.output_file, "w") as f:
            json.dump(single_translation_data, f, indent=4)

        print(f"Extracted {args.translation} translation saved to {args.output_file}")
    elif args.command == "science":
        events = load_from_json(args.input_file)
        if args.add_event:
            new_event = {
                "Item": args.item,
                "Category": args.category,
                "Bible Reference": args.bible_reference,
                "Recorded Timeframe": args.recorded_timeframe,
                "Detail Confirmed by Scientists": args.confirmed,
                "Scientific Commentary": args.scientific_commentary,
                "Scientific Comment Year": args.scientific_comment_year,
                "Timeframe Difference": args.scientific_comment_year
                - parse_year(args.recorded_timeframe),
            }
            events.append(new_event)
            with open(args.input_file, "w") as file:
                json.dump(events, file, indent=4)
            print(f"Added event: {new_event}")
        else:
            visualizer.generate_mermaid_charts(events)
    else:
        print("Invalid command. Use --help for available options.")

"""main"""

import argparse
import json

from core.processing import entity_extractor, bible_search
from core.translation_loader import bible_gw_loader, jw_loader, translation_manager


def setup_parsers():
    """Set up argument parsers for all sub-commands."""
    parser = argparse.ArgumentParser(
        description="CLI to process Bible text, extract entities, and perform searches."
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    setup_load_nwt_parser(subparsers)
    setup_load_gateway_parser(subparsers)
    setup_extract_entities_parser(subparsers)
    setup_search_parser(subparsers)
    setup_extract_reference_parser(subparsers)
    setup_extract_translation_parser(subparsers)
    setup_merge_translation_parser(subparsers)

    return parser


def setup_load_nwt_parser(subparsers):
    """setup load-jworg parser"""
    nwt_parser = subparsers.add_parser(
        "load-jworg",
        help="Load New World Translation (NWT) data into JSON format.",
    )
    nwt_parser.add_argument(
        "--input-dir",
        type=str,
        default="newWorldTranslation/english/2013-release",
        help="Base path for NWT Bible text files (default: %(default)s).",
    )
    nwt_parser.add_argument(
        "--output-file",
        type=str,
        default="data/nwt_bible.json",
        help="Output JSON file for NWT data (default: %(default)s).",
    )


def setup_load_gateway_parser(subparsers):
    """setup load-gateway parser"""
    gateway_parser = subparsers.add_parser(
        "load-gateway",
        help="Load bible-gateway translations from .txt files into JSON format.",
    )
    gateway_parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Input directory containing .txt files for KJ21/ASV.",
    )
    gateway_parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Output directory for generated JSON files.",
    )


def setup_extract_entities_parser(subparsers):
    """setup extract-entities parser"""
    extract_parser = subparsers.add_parser(
        "extract-entities",
        help="Extract entities and occupations from Bible JSON data.",
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
        default="data/bible_entities.json",
        help="Output JSON file for extracted entities (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--output-csv",
        type=str,
        default="data/bible_entities.csv",
        help="Output CSV file for extracted entities (default: %(default)s).",
    )
    extract_parser.add_argument(
        "--books",
        type=str,
        nargs="*",
        help="Specify one or more books to extract entities from (e.g., genesis exodus).",
    )
    extract_parser.add_argument(
        "--translation",
        type=str,
        default="nwt",
        help="Bible translation, ex: nwt | asv | kj21 ",
    )


def setup_search_parser(subparsers):
    """setup search parser"""
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


def setup_extract_reference_parser(subparsers):
    """setup extract-reference parser"""
    reference_parser = subparsers.add_parser(
        "extract-reference",
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


def setup_extract_translation_parser(subparsers):
    """setup extract-translation parser"""
    translation_parser = subparsers.add_parser(
        "extract-translation",
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


def setup_merge_translation_parser(subparsers):
    """setup merge-translation parser"""
    merge_parser = subparsers.add_parser(
        "merge-translation",
        help="merge a specific translation to multi-translation JSON.",
    )
    merge_parser.add_argument(
        "--input-file",
        type=str,
        default="data/nwt_bible.json",
        help="Input JSON file to merge to multi-translation.json (default: %(default)s).",
    )
    merge_parser.add_argument(
        "--translation",
        type=str,
        required=True,
        help="Translation to extract (e.g., 'asv', 'kj21', 'nwt').",
    )
    merge_parser.add_argument(
        "--output-file",
        type=str,
        default="data/extracted_translation.json",
        help="Output JSON file for extracted translation (default: %(default)s).",
    )


def handle_command(args):
    """Handle the parsed command."""
    if args.command == "load-jworg":
        jw_loader.generate_bible_json(args.input_dir, args.output_file)
    elif args.command == "load-gateway":
        bible_gw_loader.extract_verses_from_txt(args.input_dir, args.output_dir)
    elif args.command == "extract-entities":
        entity_extractor.perform_entity_analysis(
            args.input_file,
            args.output_json,
            args.output_csv,
            args.translation,
            books=args.books,
        )
    elif args.command == "search":
        matches = bible_search.find_matches(
            args.input_file,
            args.phrase,
            args.translation,
            top_n=args.top_n,
            output_csv=args.csv,
        )
        if not args.csv:
            for match in matches:
                print(
                    f"{match['book']} {match['chapter']}:{match['verse']} - {match['text']}"
                )
    elif args.command == "extract-reference":
        result = entity_extractor.extract_reference(
            args.input_file, args.reference, args.translation
        )
        print(result)
    elif args.command == "extract-translation":
        with open(args.input_file, "r", encoding="utf-8") as f:
            multi_translation_data = json.load(f)

        single_translation_data = translation_manager.extract_translation(
            multi_translation_data, args.translation
        )

        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(single_translation_data, f, indent=4)

        print(f"Extracted {args.translation} translation saved to {args.output_file}")

    elif args.command == "merge-translation":
        with open(args.output_file, "r", encoding="utf-8") as out:
            multi_translation_data = json.load(out)
        with open(args.input_file, "r", encoding="utf-8") as inp:
            input_translation_data = json.load(inp)

        merged_data = translation_manager.merge_translations(
            input_translation_data, multi_translation_data, args.translation
        )

        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, indent=4)

        print(f"Merged {args.translation} translation saved to {args.output_file}")
    else:
        print("Invalid command. Use --help for available options.")


def main():
    """Main function to handle CLI."""
    parser = setup_parsers()
    args = parser.parse_args()
    handle_command(args)


if __name__ == "__main__":
    main()

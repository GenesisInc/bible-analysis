# bible-analysis/core/visuals/visualizer.py
"""visualization."""

from core.utils.text_utils import parse_year


def generate_mermaid_charts(events, output_file="data/science/charts.md"):
    """Generate Mermaid.js Timeline and Gantt chart with Markdown headers."""
    with open(output_file, "w", encoding="utf-8") as file:
        # Write Timeline Header
        file.write("# Timeline and Gantt Charts\n\n")
        file.write("## Timeline: Scientific and Biblical Events\n\n")
        file.write("```mermaid\n")
        file.write("timeline\n")
        file.write("    title Timeline: Scientific and Biblical Events\n")

        for event in events:
            year = parse_year(event["Recorded Timeframe"])
            file.write(f"    {year}: {event['Item']} ({event['Category']})\n")

        file.write("```\n\n")

        # Write Gantt Chart Header
        file.write("## Gantt Chart: Scientific and Biblical Events\n\n")
        file.write("```mermaid\n")
        file.write("gantt\n")
        file.write("    title Gantt Chart: Scientific and Biblical Events\n")
        file.write("    dateFormat  YYYY\n")

        # Separate events into BCE and CE sections
        file.write("    section BCE Events\n")
        for event in events:
            year = parse_year(event["Recorded Timeframe"])
            if year < 0:
                file.write(f"    {event['Item']}: milestone, {year}, 1d\n")

        file.write("    section CE Events\n")
        for event in events:
            year = parse_year(event["Recorded Timeframe"])
            if year >= 0:
                file.write(f"    {event['Item']}: milestone, {year}, 1d\n")

        file.write("```\n")

    print(f"Mermaid.js charts written to {output_file}")

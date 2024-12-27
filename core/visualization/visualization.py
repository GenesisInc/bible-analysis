# bible-analysis/core/visualization/visualization.py
"""visualization """


def parse_year(year_str):
    """Parse year string into a single integer."""
    year_str = year_str.strip()

    # Handle ranges explicitly (e.g., "2000-1500 BCE")
    if "-" in year_str and not year_str.startswith(
        "-"
    ):  # Check it's a range, not a negative year
        start, end = year_str.split("-")
        start = start.replace("~", "").strip()
        if not start.isdigit():
            raise ValueError(f"Invalid year range start: '{start}' in '{year_str}'")
        if "BCE" in end:
            return -int(start)  # Use the earliest year in the range
        return int(start)  # Default to the earliest year

    # Handle single years (negative or positive)
    if "BCE" in year_str:
        year = year_str.replace("BCE", "").replace("~", "").strip()
        if not year.isdigit():
            raise ValueError(f"Invalid BCE year: '{year}' in '{year_str}'")
        return -int(year)
    elif "CE" in year_str:
        year = year_str.replace("CE", "").replace("~", "").strip()
        if not year.isdigit():
            raise ValueError(f"Invalid CE year: '{year}' in '{year_str}'")
        return int(year)
    else:
        year = year_str.replace("~", "").strip()
        if year.startswith("-"):  # Allow negative years
            try:
                return int(year)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid negative year: '{year}' in '{year_str}'"
                ) from exc
        if not year.isdigit():
            raise ValueError(f"Invalid year: '{year}' in '{year_str}'")
        return int(year)


def generate_mermaid_charts(events, output_file="data/output/science/charts.md"):
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

# bible-analysis/core/utils/text_utils.py

"""text utils."""

import json


def ensure_json_format(text):
    """ensure_json_format."""
    if isinstance(text, str):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"text": text, "context": None}
    return text


def parse_year(year_str):  # noqa: C901
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

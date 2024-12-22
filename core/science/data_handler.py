"""handle data"""

import json


def read_events(file_path):
    """Read events from a JSON file."""
    with open(file_path, mode="r", encoding="utf-8") as file:
        return json.load(file)


def add_event(file_path, event):
    """Add a new event to the JSON file."""
    events = read_events(file_path)  # Load existing events
    events.append(event)  # Add the new event
    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(events, file, indent=4)  # Write back the updated data


def update_event(file_path, search_key, search_value, updated_event):
    """Update an existing event in the JSON file."""
    events = read_events(file_path)  # Load existing events
    for event in events:
        if event.get(search_key) == search_value:  # Find the event to update
            event.update(updated_event)  # Update the event with new data
    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(events, file, indent=4)  # Write back the updated data

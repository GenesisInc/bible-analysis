"""mapper"""

import platform
import subprocess

import folium
from folium import FeatureGroup, LayerControl

from core.utils import file_utils
from core.utils.logger_utils import get_logger

logger = get_logger(__file__.rsplit("/", 1)[-1])


def map_travel(travel_file):
    """Generate and display the biblical journeys map."""
    logger.debug("mapping trip details from %s", travel_file)
    updated_map_file_path = "data/output/Enhanced_Biblical_Journeys_Map.html"
    biblical_travel_data = file_utils.load_from_json(travel_file)
    generate_enhanced_biblical_map_with_routes(
        biblical_travel_data, updated_map_file_path
    )
    print(f"generated trips map with {len(biblical_travel_data)} points")
    open_map(updated_map_file_path)


def generate_enhanced_biblical_map_with_routes(data, file_path):
    """
    Generate an interactive map with enhanced features:
    - Highlight source and destination on line click.
    - Associate journeys with location markers.
    - Include source and destination in line popups.

    Args:
    - data (list of dict): A list of dictionaries containing all travel details.
    - file_path (str): The file path to save the HTML map.

    Returns:
    - str: Path to the generated HTML file.
    """
    logger.debug("generating maps with routes")

    # Initialize a map centered near Israel
    m = folium.Map(location=[31.5, 35.5], zoom_start=6)

    # Dictionaries for managing locations and their associated journeys
    location_journeys, location_coordinates = process_location_data(data)

    # Add routes and markers
    markers = create_marker_layer(data, location_journeys, location_coordinates)
    routes = create_route_layer(data)

    # Add feature groups to the map
    m.add_child(markers)
    m.add_child(routes)

    # Add layer control for toggling markers and routes
    m.add_child(LayerControl())

    # Save the map to an HTML file
    m.save(file_path)
    return file_path


def process_location_data(data):
    """
    Extracts and organizes location data from journeys.

    Args:
    - data (list): List of journey dictionaries.

    Returns:
    - location_journeys (dict): Mapping of locations to associated journeys.
    - location_coordinates (dict): Mapping of locations to their coordinates.
    """
    location_journeys = {}
    location_coordinates = {}

    for journey in data:
        source_name = journey["source_name"]
        dest_name = journey["destination_name"]
        source_coords = journey["lat_long_source"]
        dest_coords = journey["lat_long_destination"]

        # Update location-to-journeys mapping and coordinates
        location_journeys.setdefault(source_name, []).append(journey["journey"])
        location_coordinates[source_name] = source_coords

        location_journeys.setdefault(dest_name, []).append(journey["journey"])
        location_coordinates[dest_name] = dest_coords

    return location_journeys, location_coordinates


def create_marker_layer(data, location_journeys, location_coordinates):
    """
    Creates a layer for markers with popups for source, destination, and top journeys.

    Args:
    - data (list): List of journey dictionaries.
    - location_journeys (dict): Mapping of locations to associated journeys.
    - location_coordinates (dict): Mapping of locations to their coordinates.

    Returns:
    - FeatureGroup: A Folium feature group containing markers.
    """
    markers = FeatureGroup(name="Markers")
    logger.debug("creating marker layers")

    for journey in data:
        source_coords = journey["lat_long_source"]
        dest_coords = journey["lat_long_destination"]

        # Source marker
        source_popup = generate_marker_popup(journey["source_name"], journey, "Source")
        folium.Marker(
            location=source_coords,
            popup=folium.Popup(source_popup, max_width=300),
            icon=folium.Icon(color="green", icon="info-sign"),
        ).add_to(markers)

        # Destination marker
        destination_popup = generate_marker_popup(
            journey["destination_name"], journey, "Destination"
        )
        folium.Marker(
            location=dest_coords,
            popup=folium.Popup(destination_popup, max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(markers)

    # Add markers for top journeys per location
    for location, journeys in location_journeys.items():
        top_journeys = "<br>".join(journeys[:3])  # Get top 3 journeys
        location_popup = (
            f"<b>Location:</b> {location}<br><b>Top Journeys:</b><br>{top_journeys}"
        )
        folium.Marker(
            location=location_coordinates[location],
            popup=folium.Popup(location_popup, max_width=300),
            icon=folium.Icon(color="orange", icon="flag"),
        ).add_to(markers)

    return markers


def create_route_layer(data):
    """
    Creates a layer for routes with polylines connecting source and destination.

    Args:
    - data (list): List of journey dictionaries.

    Returns:
    - FeatureGroup: A Folium feature group containing routes.
    """
    routes = FeatureGroup(name="Routes")
    logger.debug("creating routes")

    for journey in data:
        line_popup = generate_route_popup(journey)
        polyline = folium.PolyLine(
            [journey["lat_long_source"], journey["lat_long_destination"]],
            color="purple",
            weight=2.5,
            tooltip=f"{journey['journey']} ({journey['distance_km']} km)",
            popup=folium.Popup(line_popup, max_width=300),
        )
        routes.add_child(polyline)

    return routes


def generate_marker_popup(location, journey, marker_type):
    """
    Generates a popup HTML string for a marker.

    Args:
    - location (str): Location name.
    - journey (dict): Journey details.
    - marker_type (str): Type of marker ("Source" or "Destination").

    Returns:
    - str: HTML string for the marker popup.
    """
    logger.debug("generating marker popups")

    return (
        f"<b>{marker_type}:</b> {location}<br>"
        f"<b>Associated Journey:</b> {journey['journey']}<br>"
        f"<b>Timeframe:</b> {journey['timeframe']}<br>"
        f"<b>People Involved:</b> {journey['people_involved']}<br>"
        f"<b>Scripture Reference:</b> {journey['scripture_reference']}"
    )


def generate_route_popup(journey):
    """
    Generates a popup HTML string for a route.

    Args:
    - journey (dict): Journey details.

    Returns:
    - str: HTML string for the route popup.
    """
    logger.debug("generating route popups")

    return (
        f"<b>Journey:</b> {journey['journey']}<br>"
        f"<b>Distance:</b> {journey['distance_km']} km<br>"
        f"<b>Source:</b> {journey['source_name']}<br>"
        f"<b>Destination:</b> {journey['destination_name']}<br>"
        f"<b>Timeframe:</b> {journey['timeframe']}<br>"
        f"<b>People Involved:</b> {journey['people_involved']}<br>"
        f"<b>Scripture Reference:</b> {journey['scripture_reference']}"
    )


def open_map(file_path):
    """
    Open the generated HTML map in Safari on macOS.

    Args:
    - file_path (str): The path to the HTML file.
    """
    if platform.system() == "Darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "Safari", file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to open map in Safari: {e}")
    else:
        print("This function is designed for macOS and requires Safari.")


if __name__ == "__main__":
    map_travel("data/input/travel/journey_data.json")

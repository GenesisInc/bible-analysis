"""mapper"""

import platform
import subprocess

import folium
from folium import FeatureGroup, LayerControl

from core.travel import journey_data


def map_travel():
    """Generate and display the biblical journeys map."""
    updated_map_file_path = "Enhanced_Biblical_Journeys_Map.html"
    generate_enhanced_biblical_map_with_routes(
        journey_data.biblical_travel_data, updated_map_file_path
    )
    open_map(updated_map_file_path)


def generate_enhanced_biblical_map_with_routes(data, file_path):
    """
    Generate an interactive map using folium with enhanced features:
    - Highlight source and destination on line click.
    - Associate journeys with location markers.
    - Include source and destination in line popups.

    Args:
    - data (list of dict): A list of dictionaries containing all travel details.
    - file_path (str): The file path to save the HTML map.

    Returns:
    - str: Path to the generated HTML file.
    """
    # Initialize a map centered near Israel
    m = folium.Map(location=[31.5, 35.5], zoom_start=6)

    # Create feature groups for dynamic layers
    markers = FeatureGroup(name="Markers")
    routes = FeatureGroup(name="Routes")

    # Dictionary to group journeys by location for associating
    location_journeys = {}
    location_coordinates = {}

    # Add routes and markers with enhanced features
    for journey in data:
        source_coords = journey["lat_long_source"]
        dest_coords = journey["lat_long_destination"]

        # Update location-to-journeys mapping and coordinates
        location_journeys.setdefault(journey["source_name"], []).append(
            journey["journey"]
        )
        location_coordinates[journey["source_name"]] = source_coords

        location_journeys.setdefault(journey["destination_name"], []).append(
            journey["journey"]
        )
        location_coordinates[journey["destination_name"]] = dest_coords

        # Add markers for source and destination
        source_popup = (
            f"<b>Location:</b> {journey['source_name']}<br>"
            f"<b>Associated Journey:</b> {journey['journey']}<br>"
            f"<b>Timeframe:</b> {journey['timeframe']}<br>"
            f"<b>People Involved:</b> {journey['people_involved']}<br>"
            f"<b>Scripture Reference:</b> {journey['scripture_reference']}"
        )
        destination_popup = (
            f"<b>Location:</b> {journey['destination_name']}<br>"
            f"<b>Associated Journey:</b> {journey['journey']}<br>"
            f"<b>Timeframe:</b> {journey['timeframe']}<br>"
            f"<b>Scripture Reference:</b> {journey['scripture_reference']}"
        )

        # Markers for source and destination
        source_marker = folium.Marker(
            location=source_coords,
            popup=folium.Popup(source_popup, max_width=300),
            icon=folium.Icon(color="green", icon="info-sign"),
        )
        destination_marker = folium.Marker(
            location=dest_coords,
            popup=folium.Popup(destination_popup, max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign"),
        )

        # Add these markers to the map
        markers.add_child(source_marker)
        markers.add_child(destination_marker)

        # Add line connecting source and destination with trip details
        line_popup = (
            f"<b>Journey:</b> {journey['journey']}<br>"
            f"<b>Distance:</b> {journey['distance_km']} km<br>"
            f"<b>Source:</b> {journey['source_name']}<br>"
            f"<b>Destination:</b> {journey['destination_name']}<br>"
            f"<b>Timeframe:</b> {journey['timeframe']}<br>"
            f"<b>People Involved:</b> {journey['people_involved']}<br>"
            f"<b>Scripture Reference:</b> {journey['scripture_reference']}"
        )
        line = folium.PolyLine(
            [source_coords, dest_coords],
            color="purple",
            weight=2.5,
            tooltip=f"{journey['journey']} ({journey['distance_km']} km)",
            popup=folium.Popup(line_popup, max_width=300),
        )

        # Add a click handler to highlight the route and markers
        line.add_child(folium.ClickForMarker())
        routes.add_child(line)

    # Add top 3 journeys to each marker popup
    for loc, journeys in location_journeys.items():
        top_journeys = "<br>".join(journeys[:3])  # Get top 3 journeys
        location_popup = (
            f"<b>Location:</b> {loc}<br><b>Top Journeys:</b><br>{top_journeys}"
        )
        folium.Marker(
            location=location_coordinates[loc],  # Coordinates of the location
            popup=folium.Popup(location_popup, max_width=300),
            icon=folium.Icon(color="orange", icon="flag"),
        ).add_to(m)

    # Add feature groups to the map
    m.add_child(markers)
    m.add_child(routes)

    # Add layer control for toggling markers and routes
    m.add_child(LayerControl())

    # Save the map to an HTML file
    m.save(file_path)
    return file_path


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
    map_travel()

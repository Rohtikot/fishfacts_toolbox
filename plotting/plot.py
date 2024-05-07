from pandas import DataFrame
from plotting.utils import get_speed_color
import pandas as pd
import folium
import os


# Make a function that takes a dataframe and plots a speed track of the track line
def plot_vessel_track(input_df: DataFrame, m: folium.Map = None, vessel_name: str = 'Not specified') -> folium.Map:
    # If m argument is not passed, create new map object based on mean coordinates of input dataframe
    if m is None:
        mean_latitude = input_df['latitude'].mean()
        mean_longitude = input_df['longitude'].mean()
        m = initialize_map(mean_latitude, mean_longitude)

    m = plot_eez_zones(m)
    m = plot_other_zones(m)

    # Get next latitude and longitude
    input_df['next_latitude'] = input_df['latitude'].shift(-1)
    input_df['next_longitude'] = input_df['longitude'].shift(-1)

    for index, row in input_df.iloc[:-1].iterrows():
        timestamp = row['timestamp']
        lat = row['latitude']
        lon = row['longitude']
        next_lat = row['next_latitude']
        next_lon = row['next_longitude']
        speed = row['speed']
        speed_color = get_speed_color(speed)

        popup_text = f"<div style='width: 160px;'>" \
                     f"<b>Vessel name:</b>: {vessel_name}<br>" \
                     f"<b>Date</b>: {timestamp}<br>" \
                     f"<b>Latitude</b>: {lat}<br>" \
                     f"<b>Longitude</b>: {lon}<br>" \
                     f"<b>Speed</b>: {speed} knots<br>"

        folium.PolyLine(
            locations=[(lat, lon), (next_lat, next_lon)],
            color=speed_color,
            weight=2,
            opacity=1,
            popup=popup_text
        ).add_to(m)

    folium.LayerControl().add_to(m)

    return m


# Create plot function that plots eez zones as layer on top of folium map. Extra layers need to be each its own layer.
def plot_eez_zones(m: folium.Map = None) -> folium.Map:
    # If m argument is not passed, create new map object based on mean coordinates of input dataframe
    if m is None:
        m = initialize_map()

    # Get path of EEZ zones
    cur_file_path = os.path.abspath(__file__)
    par_file_dir = os.path.dirname(cur_file_path)
    eez_zones_path = os.path.join(par_file_dir, '../zones/eez_zones')
    eez_zones_folder = os.listdir(eez_zones_path)

    # TODO: Make a layer (feature group) that contains fill color, so that fill colors can be enabled/disabled
    # Plot EEZ zones
    polygon_group = folium.FeatureGroup(name='EEZ zones')
    for zone in eez_zones_folder:
        polygon_df = pd.read_csv(os.path.join(eez_zones_path, zone))
        if zone.split('_')[0] == 'neafc':
            polygon = plot_polygon(polygon_df, fill=True, fill_opacity=0.1, fill_color='white')
        elif zone.split('_')[0] == 'joined':
            polygon = plot_polygon(polygon_df, fill=True, fill_opacity=0.15, fill_color='green')
        else:
            polygon = plot_polygon(polygon_df, fill=True, fill_opacity=0.05, fill_color='turquoise')
        polygon.add_to(polygon_group)
        polygon_group.add_to(m)

    return m


def plot_other_zones(m: folium.Map = None) -> folium.Map:
    # If m argument is not passed, create new map object based on mean coordinates of input dataframe
    if m is None:
        m = initialize_map()

    # Get path of other zones
    cur_file_path = os.path.abspath(__file__)
    par_file_dir = os.path.dirname(cur_file_path)
    other_zones_path = os.path.join(par_file_dir, '../zones/other_zones')
    other_zones_folder = os.listdir(other_zones_path)

    # Plot other zones in a layer each
    for zone in other_zones_folder:
        group_name = get_zone_name(zone)
        polygon_group = folium.FeatureGroup(name=group_name, show=False)
        polygon_df = pd.read_csv(os.path.join(other_zones_path, zone))
        polygon = plot_polygon(polygon_df, color='yellow', fill=True, fill_opacity=0.2, fill_color='yellow')
        polygon.add_to(polygon_group)
        polygon_group.add_to(m)

    return m


# Plot single polygon
def plot_polygon(input_df: DataFrame, color: str = 'grey', **kwargs) -> folium.Polygon:
    # Default parameters for polygon
    default_kwargs = {
        'color': color,
        'weight': 0.5,
        'opacity': 0.5,
        'fill': False,
        'fill_opacity': 0,
        'fill_color': color
    }

    # Merge custom kwargs with default kwargs
    merged_kwargs = {**default_kwargs, **kwargs}

    # Plot polygon
    polygon = folium.Polygon(
        locations=zip(input_df['latitude'], input_df['longitude']),
        **merged_kwargs
    )

    return polygon


# Function to initialize folium map object
def initialize_map(lat: float = 62.0, lon: float = -7.0) -> folium.Map:
    m = folium.Map(location=(lat, lon), zoom_start=5)

    tiles = [
        'OpenStreetMap',
        'CartoDB positron',
        'Esri NatGeoWorldMap',
        'CartoDB dark_matter'
    ]

    for tile in tiles:
        folium.TileLayer(tile).add_to(m)

    return m


def get_zone_name(file_name):
    # Function to return proper name according to passed file
    names = {
        'norway250_nm.csv': 'Norway 250 nm zone',
        'norway250_nm_w_fjords.csv': 'Norway 250 m zone incl. fjords',
        'norway_eez_north_62.csv': 'Norway EEZ north 62N',
        'norway_eez_south_62.csv': 'Norway EEZ south 62N'
    }

    if file_name in names:
        return names[file_name]
    else:
        return file_name

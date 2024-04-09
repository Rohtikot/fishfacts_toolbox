from pandas import DataFrame
from utils import get_speed_color
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

    m = plot_eez_zones(m)

    return m


# Create plot function that plots eez zones as layer on top of folium map. Extra layers need to be each its own layer.
def plot_eez_zones(m: folium.Map = None) -> folium.Map:
    eez_zones_folder = os.listdir('../zones/eez_zones')
    other_zones_folder = os.listdir('../zones/other_zones')

    # If m argument is not passed, create new map object based on mean coordinates of input dataframe
    if m is None:
        m = initialize_map()

    # Plot EEZ zones
    for zone in eez_zones_folder:
        polygon_df = pd.read_csv(os.path.join('../zones/eez_zones', zone))

        # TODO: Missing the feature group here (toggle-able eez zones on the map. Plan is to make it a passable argument
        #  for the "plot_polygon" function and add it as a feature group there. See latest ChatGPT example in
        #  conversation "Plotting module 09.04.2024"
        polygon_group_eez = folium.FeatureGroup(name='EEZ zones')
        m = plot_polygon(polygon_df, m=m)

    return m


# Plot single polygon
def plot_polygon(input_df: DataFrame, color: str = 'grey', m: folium.Map = None) -> folium.Map:
    # If m argument is not passed, create new map object
    if m is None:
        m = initialize_map(tiles='light')

    # Plot polygon
    folium.Polygon(
        locations=zip(input_df['latitude'], input_df['longitude']),
        color=color,
        weight=0.5,
        opacity=0.5,
        fill=False,
        fill_opacity=0,
        fill_color=color
    ).add_to(m)

    return m


# Function to initialize folium map object
def initialize_map(lat: float = 62, lon: float = -7, tiles: str = 'dark') -> folium.Map:
    if tiles.lower() == 'dark':
        tile_setting = 'cartodb dark_matter'
    else:
        tile_setting = 'OpenStreetMap'

    return folium.Map(location=(lat, lon), zoom_start=5, tiles=tile_setting)


if __name__ == '__main__':
    ms = plot_eez_zones()
    ms.save('testpolygon.html')

    print('Run plot_track.py')

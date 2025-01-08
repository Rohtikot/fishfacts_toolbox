import geopandas as gpd
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
                     f"<b>Vessel name:</b> {vessel_name}<br>" \
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

    # Plot EEZ zones
    polygon_group_line = folium.FeatureGroup(name='EEZ zones (lines)')
    polygon_group_fill = folium.FeatureGroup(name='EEZ zones (fill)', show=False)

    for zone in eez_zones_folder:
        polygon_df = pd.read_csv(os.path.join(eez_zones_path, zone))
        if zone.split('_')[0] == 'neafc':
            polygon_line = plot_polygon(polygon_df)
            polygon_fill = plot_polygon(polygon_df, weight=0.05, fill=True, fill_opacity=0.1, fill_color='white')
        elif zone.split('_')[0] == 'joined':
            polygon_line = plot_polygon(polygon_df)
            polygon_fill = plot_polygon(polygon_df, weight=0.05, fill=True, fill_opacity=0.15, fill_color='green')
        else:
            polygon_line = plot_polygon(polygon_df)
            polygon_fill = plot_polygon(polygon_df, weight=0.05, fill=True, fill_opacity=0.12, fill_color='turquoise')

        polygon_line.add_to(polygon_group_line)
        polygon_fill.add_to(polygon_group_fill)

        polygon_group_line.add_to(m)
        polygon_group_fill.add_to(m)

    return m


def plot_eez_zones_w_shorelines(m: folium.Map) -> folium.Map:
    # Define a style function for customizing polygons
    def style_function(feature):
        return {
            "fillColor": "turquoise",  # Fill color
            "color": "grey",          # Border color
            "weight": 0.05,           # Border thickness
            "fillOpacity": 0.1        # Transparency
        }

    # Areas' ids from Marine Regions
    ids = [
        5690,
        5684,
        5683,
        5675,
        5676,
        5687,
        5694,
        5674,
        5686,
        5669,
        5668,
        3293,
        5696,
        8435,
        5681,
        5680,
        8437,
        33181,
        8438,
        5677
    ]

    path = r"C:\Users\tokit\Downloads\World_EEZ_v12_20231025\World_EEZ_v12_20231025\eez_v12.shp"
    df = gpd.read_file(path)

    # Select multipolygons from each country
    selected_df = df[(df['MRGID'].isin(ids))]

    feature_group = folium.FeatureGroup(name="Selected EEZ Zones")

    # Add each multipolygon to the map
    for _, row in selected_df.iterrows():
        folium.GeoJson(
            row.geometry,
            style_function=style_function,
            name=f"Feature {row.name}"
        ).add_to(feature_group)

    feature_group.add_to(m)

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
        if zone.endswith('.csv'):  # in case there are non-csv files in directory
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
        locations=input_df[['latitude', 'longitude']].values.tolist(),
        **merged_kwargs
    )

    return polygon


# Function to initialize folium map object
def initialize_map(lat: float = 62.0, lon: float = -7.0) -> folium.Map:
    m = folium.Map(location=(lat, lon), zoom_start=5)

    tiles = {
        'OpenStreetMap': 'Open Street Map',
        'CartoDB.Positron': 'Positron',
        'CartoDB.PositronNoLabels': 'Positron (no labels)',
        'Stadia.StamenToner': 'Stamen Toner',
        'Stadia.StamenTonerBackground': 'Stamen Toner (no labels)',
        'Stadia.AlidadeSmoothDark': 'Alidade Smooth Dark',
        'CartoDB.Voyager': 'Voyager',
        'CartoDB.VoyagerNoLabels': 'Voyager (no labels)',
        'OpenStreetMap.HOT': 'OpenStreetMap HOT',
        'CartoDB.DarkMatter': 'Dark Matter',
        'CartoDB.DarkMatterNoLabels': 'Dark Matter (no labels)',
    }

    for key, value in tiles.items():
        folium.TileLayer(key, name=value).add_to(m)

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

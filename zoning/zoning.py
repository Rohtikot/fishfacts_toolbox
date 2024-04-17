from time import time
from tqdm import tqdm
import pandas as pd
from shapely.geometry import Point, Polygon
import os

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)


# Make function that goes through data frame and assigns zones to each row
def which_zone(point: Point, polygons: list[(str, Polygon)]) -> str | None:
    for zone in polygons:
        if is_vessel_in_polygon(point, zone[1]):
            return zone[0]  # return name of zone

    return 'Undefined'


def get_polygons_and_names_from_dir(directory: str) -> list[(str, Polygon)]:
    polygons = []

    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            name, polygon = read_polygon_from_csv(file_path)
            polygons.append((name, polygon))

    return polygons


def read_polygon_from_csv(csv_file_path: str) -> (str, Polygon):
    _df = pd.read_csv(csv_file_path)
    coordinates = [(row['latitude'], row['longitude']) for _, row in _df.iterrows()]

    _, filename = os.path.split(csv_file_path)
    name, _ = os.path.splitext(filename)

    polygon = Polygon(coordinates)

    return name, polygon


# Function that takes a location and a polygon
def is_vessel_in_polygon(point: Point, polygon: Polygon) -> bool:
    return True if polygon.contains(point) else False


path = r"C:\Users\tokit\OneDrive\Desktop\Rapportir\Themis\2023\raw\vessel_Beinur_20230101T0000-20240101T0000.xlsx"
df = pd.read_excel(path)
zones_dir = r'../zones/eez_zones'

list_of_polygons = get_polygons_and_names_from_dir(zones_dir)

time_start = time()
df['eez_zone'] = df.apply(lambda row: which_zone(Point(row['latitude'], row['longitude']), list_of_polygons), axis=1)
time_end = time()
print(f"Elapsed time: {time_end-time_start:.01f} s ({df.shape[0] / (time_end-time_start):.01f} it/s)")

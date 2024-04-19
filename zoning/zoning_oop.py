from time import time
import pandas as pd
from shapely.geometry import Point, Polygon
import os
from interpolating.interpolate import interpolate_dataframe


class ZoneAssigner:
    def __init__(self, polygons_directory):
        self.polygons = self.get_polygons_from_dir(polygons_directory)

    def which_zone(self, point):
        for zone in self.polygons:
            if point.within(zone[1]):
                return zone[0]  # return name of zone
        return None

    def get_polygons_from_dir(self, directory):
        polygons = []
        for file_name in os.listdir(directory):
            if file_name.endswith('.csv'):
                file_path = os.path.join(directory, file_name)
                name, polygon = self.read_polygon_from_csv(file_path)
                polygons.append((name, polygon))
        return polygons

    def read_polygon_from_csv(self, csv_file_path):
        _df = pd.read_csv(csv_file_path)
        coordinates = [(row['latitude'], row['longitude']) for _, row in _df.iterrows()]
        _, filename = os.path.split(csv_file_path)
        name, _ = os.path.splitext(filename)
        polygon = Polygon(coordinates)
        return name, polygon

    def assign_zones_to_dataframe(self, input_df):
        input_df['eez_zone'] = input_df.apply(
            lambda row: self.which_zone(Point(row['latitude'], row['longitude'])),
            axis=1)
        return input_df


# Example usage
if __name__ == "__main__":
    time_read_start = time()
    path = r"C:\Users\tokit\OneDrive\Desktop\Rapportir\Sæson rapportir\Sild 2023\Íslendsk\raw\vessel_Adalsteinn_Jonsson_20220101T1200-20230301T1200.xlsx"
    zones_dir = r'../zones/eez_zones'
    df = pd.read_excel(path)
    time_read_end = time()

    time_zone_start = time()
    df_with_zones = ZoneAssigner(zones_dir).assign_zones_to_dataframe(df)
    time_zone_end = time()
    print(df_with_zones.head())

    read_time = time_read_end - time_read_start
    zoning_time = time_zone_end - time_zone_start

    print(f"Df read time:\t{read_time:10.4f} s")
    print(f"Zn apply time:\t{zoning_time:10.4f} s")

    print(f"Total time:\t\t{read_time+zoning_time:10.4f} s")
    print(f"{df.shape[0]} rows")

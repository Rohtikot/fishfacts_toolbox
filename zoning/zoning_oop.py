from time import time
import pandas as pd
from shapely.geometry import Point, Polygon
import os


class NamedPolygon:
    def __init__(self, polygon: Polygon, name: str = None):
        self.polygon = polygon
        self.name = name


class ZoneAssigner:
    def __init__(self, polygons_directory):
        self.polygons = self.get_polygons_from_dir(polygons_directory)

    def which_zone(self, point):
        for polygon in self.polygons:
            if point.within(polygon.polygon):
                return polygon.name  # return name of zone
        return None

    def get_polygons_from_dir(self, directory):
        polygons = []
        for file_name in os.listdir(directory):
            if file_name.endswith('.csv'):
                file_path = os.path.join(directory, file_name)
                polygon = self.read_polygon_from_csv(file_path)
                polygons.append(polygon)
        return polygons

    def read_polygon_from_csv(self, csv_file_path):
        _df = pd.read_csv(csv_file_path)
        coordinates = [(row['latitude'], row['longitude']) for _, row in _df.iterrows()]

        # Get name of file
        _, filename = os.path.split(csv_file_path)
        name, _ = os.path.splitext(filename)

        # Initialize named polygon
        polygon = NamedPolygon(Polygon(coordinates), name)

        return polygon

    def assign_zones_to_dataframe(self, input_df):
        input_df['eez_zone'] = input_df.apply(
            lambda row: self.which_zone(Point(row['latitude'], row['longitude'])),
            axis=1)
        return input_df


# Example usage
if __name__ == "__main__":

    path = r"/Users/tokithorsteinsson/Downloads/interpolated_vessel_476_Frank Bonefaas_20230702T0000-20230708T0000.xlsx"
    zones_dir = r'../zones/eez_zones'
    pd.set_option('display.width', None)
    df = pd.read_excel(path)

    df_with_zones = ZoneAssigner(zones_dir).assign_zones_to_dataframe(df)
    print(df_with_zones.head(20))

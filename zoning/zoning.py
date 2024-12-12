import pandas as pd
from shapely.geometry import Point, Polygon
import os
from time import time


class NamedPolygon:
    def __init__(self, polygon: Polygon, name: str = None):
        self.polygon = polygon
        self.name = name


class ZoneAssigner:
    def __init__(self, ais_df, polygon_path):
        self.ais_df = ais_df
        self.polygon_path = polygon_path

    @staticmethod
    def which_zone(point: Point, polygons: list[NamedPolygon]):
        for polygon in polygons:
            if point.within(polygon.polygon):
                return polygon.name

    def get_polygons_from_dir(self):
        polygons = []
        for file_name in os.listdir(self.polygon_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.polygon_path, file_name)
                polygon = self.read_polygon_from_csv(file_path)
                polygons.append(polygon)
        return polygons

    def get_polygons_from_file(self, group_name):
        polygons = []
        polygon_df = pd.read_csv(self.polygon_path)

        grouped = polygon_df.groupby(group_name)

        for polygon_name, group in grouped:
            coordinates = zip(group['latitude'], group['longitude'])
            polygon = NamedPolygon(Polygon(coordinates), str(polygon_name))
            polygons.append(polygon)

        return polygons

    @staticmethod
    def read_polygon_from_csv(csv_file_path):
        _df = pd.read_csv(csv_file_path)
        coordinates = zip(_df['latitude'], _df['longitude'])

        # Get name of file
        _, filename = os.path.split(csv_file_path)
        name, _ = os.path.splitext(filename)

        polygon = NamedPolygon(Polygon(coordinates), name)

        return polygon

    def assign_zones(self, group_name: str = None):
        if os.path.isfile(self.polygon_path):
            polygons = self.get_polygons_from_file(group_name)
        elif os.path.isdir(self.polygon_path):
            polygons = self.get_polygons_from_dir()

        return self.ais_df.apply(
            lambda row: self.which_zone(Point(row['latitude'], row['longitude']), polygons), axis=1)


# Example use
r"""
if __name__ == "__main__":
    import os
    path = r"C:\Users\tokit\OneDrive\Desktop\Klaksvíkskip"
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        harbors_dir = r'../zones/harbors'
        factory_path = r'../zones/factories/fo_factories.csv'
        df = pd.read_excel(file_path)

        df['harbor'] = ZoneAssigner(df, harbors_dir).assign_zones()
        df['factory'] = ZoneAssigner(df, factory_path).assign_zones('factory')
        print(df)
        df.to_excel(file_path, index=False)
"""
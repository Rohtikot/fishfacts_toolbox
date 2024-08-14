import pandas as pd
import folium

path = 'fo_harbors.csv'

df = pd.read_csv(path)

grouped = df.groupby('harbor')

m = folium.Map(location=(62, -7), tiles='cartodb dark_matter', zoom_start=10)

for name, harbor in grouped:
    coordinates = harbor[['latitude', 'longitude']].values.tolist()
    folium.Polygon(
        locations=coordinates,
    ).add_to(m)

m.save('map.html')

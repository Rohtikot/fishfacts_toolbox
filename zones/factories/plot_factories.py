import pandas as pd
import folium

path = 'fo_factories.csv'

df = pd.read_csv(path)

grouped = df.groupby('factory')

m = folium.Map(location=(62.237849, -6.801817), tiles='cartodb dark_matter', zoom_start=15)

for name, harbor in grouped:
    print(name)
    print(harbor)
    coords = harbor[['latitude', 'longitude']].values.tolist()
    folium.Polygon(
        locations=coords,
        fill=True,
        opacity=0.5,
        tooltip=f"{name}"
    ).add_to(m)

m.save('factories.html')

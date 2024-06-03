import pandas as pd
import folium
from plotting.utils import get_speed_color

path_trips = r"C:\Users\tokit\OneDrive\Desktop\Oil testing 26. mar 2024\Frank Bonefaas - oil testing\bonefaas trips.xlsx"
df_trips = pd.read_excel(path_trips)

path_ais = r"C:\Users\tokit\OneDrive\Desktop\Oil testing 26. mar 2024\Frank Bonefaas - oil testing\vessel_476_Frank Bonefaas_20230101T0000-20240101T0000.xlsx"
df_ais = pd.read_excel(path_ais)


vessel_name = 'Frank Bonefaas'

df_trips = df_trips[df_trips['vessel_name'] == vessel_name]
print(df_trips)
m = folium.Map(location=(63, -8), zoom_start=5, tiles='cartodb dark_matter')

# Create a dictionary to store FeatureGroups for each trip
trip_feature_groups = {}
count = 0
for idx, ro in df_trips.iterrows():
    trip_start = ro['start']
    trip_end = ro['end']
    df_piece = df_ais[(df_ais['timestamp'] >= trip_start) & (df_ais['timestamp'] <= trip_end)]

    print_trip_start = trip_start.strftime("%Y-%m-%d %H:%M:%S")
    print_trip_end = trip_end.strftime("%Y-%m-%d %H:%M:%S")

    # Create a FeatureGroup for each trip
    fg_trip = folium.FeatureGroup(name=f'Trip {count + 1} {print_trip_start, print_trip_end}', show=False)

    for index, row in df_piece[0:-2].iterrows():
        date_time = row['timestamp']
        lat = row['latitude']
        lon = row['longitude']
        speed = row['speed']
        popup_text = f"<div style='width: 160px;'>" \
                     f"<b>Vessel:</b>: {vessel_name}<br>" \
                     f"<b>Date</b>: {date_time}<br>" \
                     f"<b>Latitude</b>: {lat}<br>" \
                     f"<b>Longitude</b>: {lon}<br>" \
                     f"<b>Speed</b>: {speed} knots<br>"

        color = get_speed_color(row['speed'])
        vessel_trajectory = folium.PolyLine(
            locations=[(row['latitude'], row['longitude']),
                       (df_ais.loc[index + 1, 'latitude'], df_ais.loc[index + 1, 'longitude'])],
            color=color,
            weight=2,
            opacity=1,
            popup=popup_text
        )

        vessel_trajectory.add_to(fg_trip)  # Add the PolyLine to the FeatureGroup

    # Add the FeatureGroup for the trip to the dictionary
    trip_feature_groups[f'Trip {count + 1}'] = fg_trip

    count += 1

    # Add each FeatureGroup to the main map
for trip_name, fg_trip in trip_feature_groups.items():
    m.add_child(fg_trip)

    # Add LayerControl to the Map with all FeatureGroups
folium.LayerControl(collapsed=False, autoZIndex=False, overlay=True).add_to(m)

m.save(f'trip_test_plots/plot_{vessel_name}.html')

import folium
import pandas as pd
from plotting.plot import *

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.3f}'.format)

for year in [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]:
    path = fr"C:\Users\tokit\OneDrive\Desktop\Hvítfisk\norway_catch\ers\elektronisk-rapportering-ers-{year}-fangstmelding-dca.csv"
    # Current freezing trawlers on Fishfacts database (2024-06-03)
    radios = [
        "LMAC",
        "LDAL",
        "LDDG",
        "LHMF",
        "LLOP",
        "LLAJ",
        "LLAY",
        "LCMP",
        "LLDH",
        "LCLP",
        "LDDF",
        "3YHX",
        "3YYB",
        "LDCO",
        "LNKS",
        "LHXV",
        "LMBG",
        "LDBR",
        "LDBT",
        "LDSF",
        "LDNV",
        "LFGW",
        "LJWI",
        "LEBB",
        "LEGQ",
        "LJPH",
        "LFBW",
        "LLIA",
        "LIPZ",
        "LDAR",
        "LFOC",
        "JXRX",
        "LFNT",
        "LFRA",
        "LFNX",
        "LFPE",
        "LGJY",
        "LFVX",
        "JXNX",
    ]

    df = pd.read_csv(path, delimiter=';', decimal=',', low_memory=False)
    df['start_time'] = pd.to_datetime(df['Startdato'] + ' ' + df['Startklokkeslett'], dayfirst=True)
    df['stop_time'] = pd.to_datetime(df['Stoppdato'] + ' ' + df['Stoppklokkeslett'], dayfirst=True)

    df = df[
        (~df['start_time'].isna())
        & (df['Fartøynasjonalitet (kode)'] == 'NOR')
        & (df['Radiokallesignal (ERS)'].isin(radios))
    ]
    print(df.head())
    index_columns = [
        "Fartøynavn (ERS)",
        "start_time",
        "stop_time",
        "Startposisjon bredde",
        "Startposisjon lengde",
        "Stopposisjon bredde",
        "Stopposisjon lengde",
        "Varighet"
    ]
    pivot_df = df.pivot_table(index=index_columns, columns='Art - FDIR', values='Rundvekt', fill_value=0, aggfunc='sum').reset_index()
    species_columns = pivot_df.columns.difference(index_columns).tolist()
    filtered_df = pivot_df[
        (pivot_df['Dypvannsreke'] > pivot_df[species_columns].drop(columns=['Dypvannsreke']).max(axis=1))
        # & (pivot_df['Torsk'] > 10_000)
    ]

    m = initialize_map(lat=75, lon=25)

    for idx, row in filtered_df.iterrows():
        start, end = row['start_time'], row['stop_time']
        lat, lon = row['Startposisjon bredde'], row['Startposisjon lengde']
        catch = row['Torsk']
        vessel_name = row['Fartøynavn (ERS)']

        popup_text = f"<div style='width: 160px;'>" \
                     f"<b>Vessel name:</b>: {vessel_name}<br>" \
                     f"<b>Date</b>: {start} - {end}<br>" \
                     f"<b>Latitude</b>: {lat}<br>" \
                     f"<b>Longitude</b>: {lon}<br>" \
                     f"<b>Catch</b>: {catch} knots<br>"

        folium.Circle(
            location=(lat, lon),
            radius=catch*0.5,
            color='blue',
            fill=True,
            fill_color='blue',
            weight=0.01,
            fill_opacity=0.5,
            popup=popup_text
        ).add_to(m)

    m = plot_eez_zones(m)
    m = plot_other_zones(m)
    folium.LayerControl().add_to(m)
    m.save(f'freezing_trawl_hauls_{year}.html')

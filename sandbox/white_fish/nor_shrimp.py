from tqdm import tqdm
import matplotlib.pyplot as plt
from time import time
import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)

radios = pd.read_csv('ffnft24.csv')['radio'].values.tolist()
cols_to_select = ['Fartøynavn (ERS)', 'Radiokallesignal (ERS)', 'Art - FDIR', 'Startdato', 'Startklokkeslett', 'Hovedart FAO', 'Rundvekt', 'Fartøynasjonalitet (kode)']

dfs = []
years = [2020, 2021, 2022, 2023, 2024]
for year in years:
    path = fr"C:\Users\tokit\Desktop\Fishfacts\Friedata\elektronisk-rapportering-ers-{year}-fangstmelding-dca.csv"
    df = pd.read_csv(path, delimiter=';', decimal=',', usecols=cols_to_select)

    df = df[
        # (df['Radiokallesignal (ERS)'].isin(radios))
        (df['Fartøynasjonalitet (kode)'] == 'NOR')
    ]

    df['start'] = pd.to_datetime(df['Startdato'] + ' ' + df['Startklokkeslett'], format='%d.%m.%Y %H:%M')
    df['year'] = year
    df['day'] = df['start'].dt.dayofyear

    dfs.append(df)

res_df = pd.concat(dfs)

species = 'Makrell'

num_years = len(years)
fig, axes = plt.subplots(num_years, 1, figsize=(10, 6*num_years), sharex=True)
groups = res_df.groupby('year')
max_value = res_df[res_df['Art - FDIR'] == species].groupby('day')['Rundvekt'].sum().max()
print(max_value)
for ax, (year, group) in zip(axes, groups):
    pivot = group.pivot_table(index='day', columns='Art - FDIR', values='Rundvekt', fill_value=0, aggfunc='sum').reset_index()
    days = pivot['day'].unique()
    ax.bar(days, pivot[species])
    ax.set_ylim(0, max_value)
    ax.set_title(f'Year: {year}')
    ax.grid()

axes[-1].set_xlabel('Day of Year')
fig.tight_layout()
plt.show()


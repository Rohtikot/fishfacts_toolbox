from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from time import time
import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)

radios = pd.read_csv('ffnft24.csv')['radio'].values.tolist()
cols_to_select = ['Fartøynavn (ERS)', 'Radiokallesignal (ERS)', 'Art - FDIR', 'Startdato', 'Startklokkeslett', 'Hovedart FAO', 'Rundvekt', 'Fartøynasjonalitet (kode)']

dfs = []
years = [i for i in range(2020, 2025)]
for year in years:
    start = time()
    path = fr"C:\Program Files (x86)\Fishfacts\catch\norway\ers\elektronisk-rapportering-ers-{year}-fangstmelding-dca.csv"
    df = pd.read_csv(path, delimiter=';', decimal=',', usecols=cols_to_select)

    # for i in df['Art - FDIR'].unique():
    #     print(i)

    df = df[
        (df['Fartøynasjonalitet (kode)'] == 'NOR')
        # & (df['Radiokallesignal (ERS)'].isin(radios))
    ]
    df['Rundvekt'] = df['Rundvekt'] / 1000
    df['start'] = pd.to_datetime(df['Startdato'] + ' ' + df['Startklokkeslett'], format='%d.%m.%Y %H:%M')
    df['year'] = year
    df['day'] = df['start'].dt.dayofyear

    dfs.append(df)
    end = time()
    print(f"Time {end-start:.2f} s")
res_df = pd.concat(dfs)

species = 'Uer (vanlig)'

num_years = len(years)
fig, axes = plt.subplots(num_years, 1, figsize=(10, 6), sharex=True)
groups = res_df.groupby('year')
max_value = res_df[res_df['Art - FDIR'] == species].groupby(['year', 'day'])['Rundvekt'].sum().max()
print(max_value)

formatter = ticker.ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)

for ax, (year, group) in zip(axes, groups):
    pivot = group.pivot_table(index='day', columns='Art - FDIR', values='Rundvekt', fill_value=0, aggfunc='sum').reset_index()
    days = pivot['day'].unique()
    ax.bar(days, pivot[species])
    ax.set_ylim(0, max_value+max_value*0.05)
    ax.set_title(f'Year: {year}')
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    ax.grid()

axes[-1].set_xlabel('Day of Year')
plt.subplots_adjust(left=0.1, right=0.985, top=0.912, bottom=0.076, wspace=0.214, hspace=0.32)


fig.tight_layout()
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)

dfs = []
years = [2022]
for year in (pbar := tqdm(years, total=len(years))):
    pbar.set_description(f"Processing {year}")
    path = fr"C:\Users\tokit\OneDrive\Desktop\Hvítfisk\norway_catch\catch\fangstdata_{year}.csv"

    df = pd.read_csv(path, delimiter=';', decimal=',', low_memory=False, parse_dates=['Landingsdato'], dayfirst=True)

    _df = df[
        (df['Fartøynasjonalitet'] == 'NORGE')
        & (df['Største lengde'] >= 35)
        & (df['Fartøytype'].isin(['Fiskefartøy', 'Leiefartøy (Erstatningsfartøy)']))
    ]
    _df.loc[_df['Landingsmåned (kode)'] == 13, 'Landingsmåned (kode)'] = 12

    grouped = _df.groupby(['Art - FDIR', 'Landingsmåned (kode)'])['Produktvekt'].sum()
    monthly = grouped['Makrell']
    monthly.name = str(year)
    dfs.append(monthly)

res_df = pd.concat(dfs, axis=1).reset_index()
print(res_df)
print(res_df.sum())

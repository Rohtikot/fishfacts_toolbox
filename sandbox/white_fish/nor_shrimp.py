import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)

main_species = [
    'Sei',
    'Nordøstarktisk torsk',
    'Dypvannsreke',
    'Snabeluer',
    'Nordøstarktisk hyse',
    'Uspesifisert fisk',
    'Torsk',
    'Hyse',
    'Blåkveite',
    'Uer (vanlig)',
]

main_species_code = [
    1032,  # Sei
    102202,  # Nordøstarktisk torsk
    2524,  # Dypvannsreke
    2203,  # Snabeluer
    102701,  # Nordøstarktisk hyse
    2999,  # Uspesifisert fisk
    1022,  # Torsk
    1027,  # Hyse
    2313,  # Blåkveite
    2202,  # Uer (vanlig)
]


def find_vessels_fishing_main_species(year: int):
    path = fr"C:\Users\tokit\OneDrive\Desktop\Hvítfisk\norway_catch\catch\fangstdata_{year}.csv"

    df = pd.read_csv(path, delimiter=';', decimal=',', low_memory=False)

    # Filters
    df = df[
        (df['Fartøynasjonalitet'] == 'NORGE')
        & (df['Fartøytype'].isin(['Fiskefartøy', 'Leiefartøy (Erstatningsfartøy)']))
        & (df['Art - FDIR'].isin(main_species))
        & (df['Produktvekt'] > 1000)
        & (df['Største lengde'] >= 28)
        ]

    pivot_df = df.pivot_table(index=['Fartøynavn', 'Radiokallesignal (seddel)'], columns='Art - FDIR', values='Produktvekt',
                              fill_value=0, aggfunc='sum').reset_index()

    pivot_df['Total'] = pivot_df[main_species].sum(axis=1)
    pivot_df.sort_values(by='Total', ascending=False, inplace=True)

    return pivot_df


def ers_departures_norway(year: int) -> pd.DataFrame:
    path = fr"C:\Users\tokit\OneDrive\Desktop\Hvítfisk\norway_catch\ers\elektronisk-rapportering-ers-{year}-avgangsmelding-dep.csv"

    df = pd.read_csv(path, delimiter=';', decimal=',', encoding='utf-8')
    df = df[
        (df['Målart - FDIR (kode)'].isin(main_species_code))
        & (df['Fartøynasjonalitet (kode)'] == 'NOR')
    ]

    return df


if __name__ == '__main__':
    # res = find_vessels_fishing_main_species(2023)
    res = ers_departures_norway(2023)
    vessels = res['Fartøynavn (ERS)'].unique()
    for i in vessels:
        print(i)
    print(res.head(5))

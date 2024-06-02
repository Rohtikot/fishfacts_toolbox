import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)

dfs = []

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

for year in [2023]:
    print(year)
    path = fr"C:\Users\tokit\Desktop\Fishfacts\Friedata\fangst\fangstdata_{year}.csv"

    df = pd.read_csv(path, delimiter=';', decimal=',', low_memory=False)

    _df = df[
        (df['Radiokallesignal (seddel)'].isin(radios))
        # (df['Fartøynasjonalitet'] == 'NORGE')
        & (df['Største lengde'] >= 35)
        & (df['Fartøytype'].isin(['Fiskefartøy', 'Leiefartøy (Erstatningsfartøy)']))
        ]

    pivot = _df.pivot_table(index='Art - FDIR', columns='Fartøynavn', values='Produktvekt', fill_value=0, aggfunc='sum').reset_index()
    print(pivot)
    #
    # grouped = _df.groupby('Art - FDIR')['Produktvekt'].sum()
    # grouped.sort_values(inplace=True, ascending=False)
    # species = grouped.index.tolist()
    # pivot = pivot[['Fartøynavn'] + species]
    # print(pivot)

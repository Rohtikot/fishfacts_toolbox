import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)


year = 2023
path = fr"C:\Users\tokit\OneDrive\Desktop\Hvítfisk\norway_catch\catch\fangstdata_{year}.csv"

df = pd.read_csv(
    path,
    delimiter=';',
    decimal=',',
    low_memory=False,
    parse_dates=['Siste fangstdato', 'Landingsdato', 'Oppdateringstidspunkt'],
    date_format='%d.%m.%Y',
)

df = df[
    (df['Fartøynasjonalitet'] == 'NORGE')
    & (df['Fartøynavn'] == 'LANGENES')
]
print(df.head(20))
pivot = df.pivot_table(index=['Fartøynavn', 'Radiokallesignal (seddel)'], columns='Art - FDIR',
                       values='Produktvekt', fill_value=0, aggfunc='sum').reset_index()
pivot['Pelagic'] = pivot['Makrell'] + pivot['Norsk vårgytende sild'] + pivot['Kolmule']
pivot.sort_values(by='Sei', inplace=True, ascending=False)
pivot = pivot[['Fartøynavn', 'Radiokallesignal (seddel)', 'Sei', 'Dypvannsreke', 'Hyse', 'Nordøstarktisk hyse', 'Nordøstarktisk torsk', 'Snabeluer', 'Torsk', 'Uer (vanlig)', 'Makrell', 'Norsk vårgytende sild', 'Kolmule', 'Pelagic']]
pivot = pivot.head(200)
pivot.sort_values(by='Pelagic', inplace=True, ascending=False)
print(pivot)

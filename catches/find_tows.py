from nor_fdir_functions import *

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# vel ár
year = 2023

# má vera ein listi
vessel = [
    'GUNNAR LANGVA',

    # skriva fleiri skip her
]

vessel = [i.upper() for i in vessel]

path = fr"C:\Program Files (x86)\Fishfacts\catch\norway\ers\elektronisk-rapportering-ers-{year}-fangstmelding-dca.csv"
df = read_dca(path)
df['Fartøynavn (ERS)'] = df['Fartøynavn (ERS)'].str.upper()
df = df[df['Fartøynavn (ERS)'].isin(vessel)]

tows = isolate_tows(df)
print(tows)

# Um tað  goymast til excel
#tows.to_excel('tows.xlsx', index=False)

import pandas as pd
from zoning.zoning_oop import *
from vessels_meeting import find_close_encounters

pd.set_option('display.width', None)

df1 = pd.read_excel(r"C:\Users\tokit\OneDrive\Desktop\Sild_23_24\AIS\Faroe Islands\Raw\vessel_9_Finnur Fríði_20231015T0000-20240101T0000.xlsx")
df2 = pd.read_excel(r"C:\Users\tokit\OneDrive\Desktop\Sild_23_24\AIS\Faroe Islands\Raw\vessel_369_Gøtunes_20231015T0000-20240101T0000.xlsx")

result = find_close_encounters(df1, df2, 1)
print(result)

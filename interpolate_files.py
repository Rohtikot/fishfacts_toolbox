import pandas as pd
from interpolating.interpolate import interpolate_dataframe
from zoning.zoning_oop import *
import os

path = r"C:\Users\tokit\OneDrive\Desktop\Sild_23_24\AIS\Faroe Islands\Raw"
save_path = r"C:\Users\tokit\OneDrive\Desktop\Sild_23_24\AIS\Faroe Islands\Interpolated"

folder = os.listdir(path)
for file in folder:
    file_path = path + '\\' + file

    df = pd.read_excel(file_path)
    int_df = interpolate_dataframe(df, 15)
    int_df['eez zone'] = ZoneAssigner(int_df, r"C:\Users\tokit\PycharmProjects\fishfacts_toolbox\zones\eez_zones").assign_zones()

    save_name = save_path + '\\' + 'interpolated_' + file

    int_df.to_excel(save_name, index=False)

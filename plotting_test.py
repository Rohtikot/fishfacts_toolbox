from plotting.plot_track import *
import pandas as pd


def main():
    path = r"C:\Users\tokit\OneDrive\Desktop\Rapportir\Sæson rapportir\Makrelur 2023\AIS\Faroe Islands\Raw\vessel_8_Fagraberg_20230501T0000-20231001T0000.xlsx"
    df = pd.read_excel(path)

    plot = plot_vessel_track(df)
    plot.save('test2.html')


if __name__ == '__main__':
    main()

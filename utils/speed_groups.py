from math import ceil
from pandas import DataFrame, cut
import numpy as np


def speed_groups(dataframe: DataFrame, interval: float) -> DataFrame:
    """
    Return DataFrame containing speed groups and hours spent and percentage hereof in each speed group.

    :param dataframe:
    :param interval:
    :return:
    """

    dataframe.sort_values(by='timestamp', inplace=True)

    # Find top speed
    top_speed = ceil(dataframe['speed'].max())

    # Create bins
    speed_bins = np.arange(0.5, top_speed, interval)

    # Cut dataframe by speed bins and calculate the time spent in that speed
    dataframe['speed_group'] = cut(dataframe['speed'], bins=speed_bins, right=False)
    dataframe['time_diff'] = dataframe['timestamp'].diff().dt.total_seconds() / 3600
    dataframe = dataframe[dataframe['time_diff'] < 0.25]  # Filter out large time gaps (15 min)
    dataframe.dropna(subset=['time_diff'], inplace=True)

    # Sum time spent in each speed bin by grouping
    time_spent_in_each_group = dataframe.groupby('speed_group')['time_diff'].sum()

    return time_spent_in_each_group


r"""
# EXAMPLE WITH PLOT
if __name__ == '__main__':
    from pandas import read_excel
    import matplotlib.pyplot as plt
    path = r"C:\Users\tokit\OneDrive\Desktop\Rapportir\Sæson rapportir\Makrelur 2023\AIS\Iceland\Raw\vessel_313_Jón Kjartansson SU111_20230615T0000-20230915T0000.xlsx"
    df = read_excel(path)
    speed_group = speed_groups(df, 0.2)

    speed_group.plot(kind='bar', color='blue', edgecolor='black')
    plt.xticks(rotation=45, ha='right')

    plt.show()
"""
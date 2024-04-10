import pandas as pd
from interpolating.fn_interpolating import interpolate_dataframe
from utils.replace_missing_headings import replace_heading_error
from utils.calculate_distance import calculate_distance
from utils.calculate_timedelta import calculate_timedelta
from utils.calculate_mean_speed import calculate_mean_speed_between_points
from plotting.plot_track import plot_vessel_track
from plotting.utils import get_speed_color

pd.set_option('display.width', None)


def main():
    path = r"C:\Users\tokit\OneDrive\Desktop\Rapportir\Sæson rapportir\Makrelur 2023\AIS\Faroe Islands\Raw\vessel_9_Finnur Fríði_20230501T0000-20231001T0000.xlsx"
    df = pd.read_excel(path)

    # Correct headings
    df['heading'] = replace_heading_error(df['heading'])

    # Interpolate data frame
    int_df = interpolate_dataframe(df)

    # Calculate distance traveled, timedelta, and average_speed
    int_df['distance_traveled'] = calculate_distance(int_df)
    int_df['timedelta'] = calculate_timedelta(int_df)
    int_df['mean_speed'] = calculate_mean_speed_between_points(int_df)

    ms = plot_vessel_track(df)
    ms = plot_vessel_track(int_df)

    ms.save('test.html')


if __name__ == '__main__':
    main()
    print(f'Run {str(__file__).split('\\')[-1]}')

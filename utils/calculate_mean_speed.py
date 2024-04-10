from pandas import DataFrame, Series
from utils.calculate_distance import calculate_distance
from utils.calculate_timedelta import calculate_timedelta


def calculate_mean_speed_between_points(input_df: DataFrame) -> Series:
    """
    Calculate the mean speed between two datapoints based on "timedelta" and "distance"

    :param input_df: A pandas DataFrame containing columns "timedelta" and "distance"
    :return: A pandas Series as the mean_speed
    """

    input_df = input_df.copy()

    # Check if necessary columns are in input data frame
    if 'timedelta' not in input_df.columns:
        input_df['timedelta'] = calculate_timedelta(input_df)

    if 'distance' not in input_df.columns:
        input_df['distance'] = calculate_distance(input_df)

    input_df['timedelta'] = (input_df['timedelta'].dt.total_seconds() / 3600)
    input_df['mean_speed'] = input_df['distance'] / input_df['timedelta']

    return input_df['mean_speed']


if __name__ == '__main__':
    print(f'Run {str(__file__).split('\\')[-1]}')

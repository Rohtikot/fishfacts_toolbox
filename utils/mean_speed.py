from pandas import DataFrame, Series
from utils.distance import calculate_distance


def calculate_mean_speed_between_points(dataframe: DataFrame) -> Series:
    """
    Calculate the mean speed between two datapoints based on "timedelta" and "distance"

    :param dataframe: A pandas DataFrame containing columns "timedelta" and "distance"
    :return: A pandas Series with mean speed in knots
    """

    dataframe = dataframe.copy()

    # Check if necessary columns are in input data frame
    if 'timedelta' not in dataframe.columns:
        dataframe['timedelta'] = dataframe['timestamp'].diff()

    if 'distance' not in dataframe.columns:
        dataframe['distance'] = calculate_distance(dataframe)

    dataframe['timedelta'] = (dataframe['timedelta'].dt.total_seconds() / 3600)
    dataframe['mean_speed'] = dataframe['distance'] / dataframe['timedelta']

    return dataframe['mean_speed']


if __name__ == '__main__':
    print(f'Run {str(__file__).split('\\')[-1]}')

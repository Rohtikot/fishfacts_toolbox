from nautical_calculations.basic import get_distance
from pandas import DataFrame, Series


def calculate_distance(input_df: DataFrame) -> Series:
    """
    Calculate the distance between each row of an AIS data frame
    :param input_df: A pandas DataFrame containing columns "latitude" and "longitude"
    :return: A pandas Series containing the distances in nautical miles between each row of the input data frame
    """
    input_df = input_df.copy()

    input_df['previous_latitude'] = input_df['latitude'].shift()
    input_df['previous_longitude'] = input_df['longitude'].shift()

    return input_df.apply(
        lambda row: get_distance(row['latitude'],
                                 row['longitude'],
                                 row['previous_latitude'],
                                 row['previous_longitude']) * 0.539956803, axis=1)  # conversion from km to nm

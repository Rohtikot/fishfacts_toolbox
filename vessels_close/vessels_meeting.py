import pandas as pd
from nautical_calculations.basic import get_distance


def merge_df_on_timestamp(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame, time_tolerance_minutes: int = 5) -> pd.DataFrame:
    """
    Merge two dataframes by aligning their timestamps to the nearest rounded timestamp.

    :param dataframe1: pandas AIS dataframe
    :param dataframe2: pandas AIS dataframe
    :param time_tolerance_minutes: int for minute tolerance
    :return: merged dataframe from both vessels with common column "timestamp_rounded"
    """

    # Make a rounded timestamp on each dataframe
    dataframe1['timestamp_rounded'] = dataframe1['timestamp'].dt.round('5min')
    dataframe2['timestamp_rounded'] = dataframe2['timestamp'].dt.round('5min')

    # Merge dataframes on the rounded timestamp column
    merged_df = pd.merge_asof(dataframe1.sort_values('timestamp_rounded'),
                              dataframe2.sort_values('timestamp_rounded'),
                              on='timestamp_rounded',
                              direction='nearest',
                              tolerance=pd.Timedelta(f'{time_tolerance_minutes}min'))

    merged_df.dropna(inplace=True)

    return merged_df


def distance_between_vessels(dataframe: pd.DataFrame) -> pd.Series:
    # Calculate the distance between rows in data frame in meters
    distances = dataframe.apply(
        lambda row: get_distance(
            row['latitude_x'],
            row['longitude_x'],
            row['latitude_y'],
            row['longitude_y'],
        ) * 1000, axis=1
    )

    # Calculate the rolling minimum to smooth out spikes in distance
    rolling_avg_distances = distances.rolling(window=5).min()

    return rolling_avg_distances


def find_close_encounters(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame, time_tolerance_minutes: int = 5) -> pd.DataFrame:
    """
    Find the close encounters between two vessels

    :param dataframe1: DataFrame of one vessel's AIS data
    :param dataframe2: DataFrame of the other vessel's AIS data
    :param time_tolerance_minutes:  Time tolerance to align dataframes for
    :return:
    """

    # Merge both vessels' data frames on datetime column
    merged_df = merge_df_on_timestamp(dataframe1, dataframe2, time_tolerance_minutes)

    # Calculate the distance between each row of merged data frame
    merged_df['distance_m'] = distance_between_vessels(merged_df)

    # Create a boolean column indicating when distance_m is below 300 meters
    merged_df['below_threshold'] = merged_df['distance_m'] < 300

    # Assign a group identifier for consecutive below_threshold groups
    merged_df['group_id'] = (merged_df['below_threshold'] != merged_df['below_threshold'].shift()).cumsum()

    # Filter the dataframe to include only rows where distance_m is below 300 meters
    filtered_df = merged_df[merged_df['below_threshold']]

    # Group by group_id and find the start and stop times
    grouped = filtered_df.groupby('group_id').agg(
        start_time=('timestamp_rounded', 'min'),
        stop_time=('timestamp_rounded', 'max')
    ).reset_index(drop=True)

    return grouped

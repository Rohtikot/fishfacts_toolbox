from pandas import DataFrame, Timedelta


def find_stops(dataframe: DataFrame, min_stop_duration_minutes: int) -> DataFrame:
    """Find every stop a vessel makes that lasts longer than specified time in minutes."""

    # Speed and time threshold.
    speed_threshold = 0.1
    min_stop_duration = Timedelta(minutes=min_stop_duration_minutes)

    # Calculate mean rolling speed to avoid spikes in data
    dataframe['rolling_speed'] = dataframe['speed'].rolling(window=5).mean()

    # Find all rows that are below or equal to speed threshold.
    dataframe['is_stopped'] = dataframe['rolling_speed'] <= speed_threshold

    # Find starts and stops of port stops.
    dataframe['stop_start'] = (dataframe['is_stopped'] & ~dataframe['is_stopped'].shift(1).fillna(False))
    dataframe['stop_end'] = (~dataframe['is_stopped'] & dataframe['is_stopped'].shift(1).fillna(False))

    # Find index of every stop and start of port stops.
    stop_starts = dataframe[dataframe['stop_start']].index
    stop_ends = dataframe[dataframe['stop_end']].index

    stops = []

    for start, end in zip(stop_starts, stop_ends):
        # Calculate duration of the stop
        stop_duration = dataframe.loc[end, 'timestamp'] - dataframe.loc[start, 'timestamp']

        if stop_duration >= min_stop_duration:
            mean_lat = dataframe.loc[start:end, 'latitude'].mean()
            mean_lon = dataframe.loc[start:end, 'longitude'].mean()

            # Only keep stop that are longer than x minutes
            stops.append({
                'stop_start': dataframe.loc[start, 'timestamp'],
                'stop_end': dataframe.loc[end, 'timestamp'],
                'duration': stop_duration,
                'mean_latitude': mean_lat,
                'mean_longitude': mean_lon
            })

    stops_df = DataFrame(stops)

    return stops_df

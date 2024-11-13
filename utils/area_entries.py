import pandas as pd
from shapely.geometry import Point, Polygon


def get_entry_exit_times(dataframe: pd.DataFrame, area: pd.DataFrame) -> pd.DataFrame:
    """
    Returns entry and exit times along with the elapsed time for periods when a vessel is inside a given polygonal area.

    Parameters:
        dataframe (pd.DataFrame): Input DataFrame with 'latitude', 'longitude', and 'timestamp' columns.
        area (pd.DataFrame): DataFrame defining the polygon with 'latitude' and 'longitude' columns.

    Returns:
        pd.DataFrame: DataFrame with 'entry_time', 'exit_time', and 'elapsed_time' columns.
    """

    # Define the polygon from the 'area' DataFrame
    polygon = Polygon(area[['latitude', 'longitude']].values)

    # Determine which points are inside the polygon
    is_inside = dataframe[['latitude', 'longitude']].apply(lambda x: Point(x).within(polygon), axis=1)

    # Identify changes in the 'is_inside' status
    inside_change = is_inside.ne(is_inside.shift()).cumsum()

    # Filter only changes in the 'is_inside' status
    inside_periods = dataframe[is_inside].copy()
    inside_periods['inside_change'] = inside_change[is_inside]

    # Group by 'inside_change' and aggregate entry and exit times
    result_df = inside_periods.groupby('inside_change').agg(
        entry_time=('timestamp', 'first'),
        exit_time=('timestamp', 'last'),
    ).reset_index(drop=True)

    # Calculate elapsed time for each entry
    result_df['elapsed_time'] = result_df['exit_time'] - result_df['entry_time']

    return result_df

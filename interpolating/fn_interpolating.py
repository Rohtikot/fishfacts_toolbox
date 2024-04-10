import pandas as pd
from scipy.interpolate import interp1d


def interpolate_dataframe(input_df: pd.DataFrame, interval: int = 15) -> pd.DataFrame:
    # Create data range based on input data frame
    start_time = input_df['timestamp'].iloc[0].replace(minute=0, second=0, microsecond=0)
    end_time = input_df['timestamp'].iloc[-1]
    new_timestamp = pd.date_range(start=start_time, end=end_time, freq=f'{interval}T')

    # Create a function for interpolation
    interp_func = interp1d(input_df['timestamp'].astype('int64'), input_df['speed'], kind='linear', fill_value='extrapolate')

    # Create new data frame to merge with input data frame
    interpolated_data = {
        'timestamp': new_timestamp,
        'speed': interp_func(new_timestamp.astype('int64'))
    }

    # Merge the two data frames and remove the old speed column
    interpolated_df = pd.DataFrame(interpolated_data)
    interpolated_df = pd.merge_asof(interpolated_df, input_df.drop(columns=['speed']), on='timestamp', direction='nearest')

    return interpolated_df[['timestamp', 'latitude', 'longitude', 'speed', 'heading']]


if __name__ == '__main__':
    print(f'Run {str(__file__).split('\\')[-1]}')

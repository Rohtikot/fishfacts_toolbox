from pandas import DataFrame, Series


def calculate_timedelta(input_df: DataFrame) -> Series:
    """Calculate the difference of time between consecutive rows"""
    previous_time = input_df['timestamp'].shift()
    time_deltas = input_df['timestamp'] - previous_time

    return time_deltas


if __name__ == '__main__':
    print(f'Run {str(__file__).split('\\')[-1]}')

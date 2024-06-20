from pandas import DataFrame, Series


def calculate_timedelta(input_df: DataFrame) -> Series:
    """Calculate the difference of time between consecutive rows"""
    return input_df['timestamp'].diff()


if __name__ == '__main__':
    print(f'Run {str(__file__).split('\\')[-1]}')

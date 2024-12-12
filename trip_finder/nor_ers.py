import pandas as pd


# Find trip departures
def find_trip_departures(input_df: pd.DataFrame, vessel_name: str or list[str]) -> pd.DataFrame:
    if not isinstance(vessel_name, list):
        vessel_name = [vessel_name]
    vessel_name = [i.upper() for i in vessel_name]

    # cast vessels' names to lower case and create time column "departure_time"
    input_df = input_df.copy()
    input_df['Fartøynavn'] = input_df['Fartøynavn'].str.upper()
    input_df['departure_time'] = pd.to_datetime(input_df['Avgangsdato'] + ' ' + input_df['Avgangsklokkeslett'],
                                                format='%d.%m.%Y %H:%M')

    # filter out vessels based on name or radio call sign, and only select departures where there is no catch onboard
    input_df = input_df[
        (input_df['Fartøynavn'].isin(vessel_name) | (input_df['Radiokallesignal']).isin(vessel_name))
        & (input_df['Kvantum type'].isna())
        ]

    return input_df


# Find trip arrivals
def find_trip_arrivals(input_df: pd.DataFrame, vessel_name: str or list[str]) -> pd.DataFrame:
    if not isinstance(vessel_name, list):
        vessel_name = [vessel_name]
    vessel_name = [i.upper() for i in vessel_name]

    # cast vessels' names to lower case and create time column "arrival_time"
    input_df = input_df.copy()
    input_df['Fartøynavn'] = input_df['Fartøynavn'].str.upper()
    input_df['arrival_time'] = pd.to_datetime(input_df['Ankomstdato'] + ' ' + input_df['Ankomstklokkeslett'],
                                              format='%d.%m.%Y %H:%M')

    # filter out vessels based on name or radio call sign, and only select arrivals where catch is being landed
    input_df = input_df[
        ((input_df['Fartøynavn'].isin(vessel_name)) | (input_df['Radiokallesignal']).isin(vessel_name))
        & (input_df['Kvantum type'] == 'Fangst overført')
        ]

    return input_df


def find_trips_nor(year: int, vessel_name: str or list[str]) -> pd.DataFrame:
    path = [
        fr"C:\Program Files (x86)\Fishfacts\catch\norway\ers\elektronisk-rapportering-ers-{year}-ankomstmelding-por.csv",
        fr"C:\Program Files (x86)\Fishfacts\catch\norway\ers\elektronisk-rapportering-ers-{year}-avgangsmelding-dep.csv"
    ]

    # read departures and arrivals
    df_departures = pd.read_csv(path[1], delimiter=';', decimal=',')
    df_arrivals = pd.read_csv(path[0], delimiter=';', decimal=',')

    # drop identical rows within departure_time and arrival_time columns, and sort data frames based on these times
    departures = find_trip_departures(df_departures, vessel_name)
    arrivals = find_trip_arrivals(df_arrivals, vessel_name)
    departures.drop_duplicates('departure_time', inplace=True)
    arrivals.drop_duplicates('arrival_time', inplace=True)
    departures.sort_values(by='departure_time', inplace=True)
    arrivals.sort_values(by='arrival_time', inplace=True)

    # Align nearest prior departure to each arrival by vessel. Matches backward on time.
    result = pd.merge_asof(
        arrivals,
        departures,
        by='Fartøynavn',
        left_on='arrival_time',
        right_on='departure_time',
        direction='backward',
        suffixes=('', '_dep')
    ).reset_index(drop=True)

    # drop duplicate departure times and keep first
    result.drop_duplicates(subset='departure_time', keep='first', inplace=True)

    # sort data frame by vessel and departure time
    result.sort_values(by=['Fartøynavn', 'departure_time'], inplace=True, ascending=[True, False])

    return result[['Fartøynavn', 'Radiokallesignal', 'departure_time', 'arrival_time']]

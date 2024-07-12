import pandas as pd


def read_dca(path: str) -> pd.DataFrame:
    """
    Read ERS-DCA sheet and add time columns such as start and stop times for fishing activities.

    :param path: path to DCA CSV-file
    :return: Pandas data frame that contains columns "Start tid" and "Stopp tid" as datetime objects.
    """
    dataframe = pd.read_csv(path, delimiter=';', decimal=',')

    # Create necessary time columns from different time columns
    dataframe['start_time'] = dataframe['Startdato'] + ' ' + dataframe['Startklokkeslett']
    dataframe['stop_time'] = dataframe['Stoppdato'] + ' ' + dataframe['Stoppklokkeslett']
    dataframe['start_time'] = pd.to_datetime(dataframe['start_time'], format='%d.%m.%Y %H:%M')
    dataframe['stop_time'] = pd.to_datetime(dataframe['stop_time'], format='%d.%m.%Y %H:%M')
    dataframe['report_time'] = dataframe['Meldingsdato'] + ' ' + dataframe['Meldingsklokkeslett']
    dataframe['report_time'] = pd.to_datetime(dataframe['report_time'], format='%d.%m.%Y %H:%M')

    return dataframe


def read_arrivals(path: str) -> pd.DataFrame:
    dataframe = pd.read_csv(path, delimiter=';', decimal=',')

    # Create necessary time columns from different columns
    dataframe['arrival_time'] = dataframe['Ankomstdato'] + ' ' + dataframe['Ankomstklokkeslett']
    dataframe['arrival_time'] = pd.to_datetime(dataframe['arrival_time'], format='%d.%m.%Y %H:%M')

    return dataframe


def read_departures(path: str) -> pd.DataFrame:
    dataframe = pd.read_csv(path, delimiter=';', decimal=',')

    # Create necessary time columns from different columns
    dataframe['departure_time'] = dataframe['Avgangsdato'] + ' ' + dataframe['Avgangsklokkeslett']
    dataframe['departure_time'] = pd.to_datetime(dataframe['departure_time'], format='%d.%m.%Y %H:%M')

    return dataframe


# TODO: Add functions to read Fangstdata and overføringsmelding
#  add function to update latest (2024) files.

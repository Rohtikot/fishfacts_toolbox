import pandas as pd


def read_dca(path: str) -> pd.DataFrame:
    """
    Read ERS-DCA sheet and add time columns such as start and stop times for fishing activities.

    :param path: path to DCA CSV-file
    :return: Pandas data frame that contains columns "Start tid" and "Stopp tid" as datetime objects.
    """
    dataframe = pd.read_csv(path, delimiter=';', decimal=',')

    # Create necessary time columns from different time columns
    dataframe['Start time'] = dataframe['Startdato'] + ' ' + dataframe['Startklokkeslett']
    dataframe['Stop time'] = dataframe['Stoppdato'] + ' ' + dataframe['Stoppklokkeslett']
    dataframe['Start time'] = pd.to_datetime(dataframe['Start time'], format='%d.%m.%Y %H:%M')
    dataframe['Stop time'] = pd.to_datetime(dataframe['Stop time'], format='%d.%m.%Y %H:%M')
    dataframe['Reporting time'] = dataframe['Meldingsdato'] + ' ' + dataframe['Meldingsklokkeslett']
    dataframe['Reporting time'] = pd.to_datetime(dataframe['Reporting time'], format='%d.%m.%Y %H:%M')

    return dataframe


# TODO: Add functions to read Fangstadata, ankomstmelding, avgangsmelding and overføringsmelding
#  add function to update latest (2024) files.

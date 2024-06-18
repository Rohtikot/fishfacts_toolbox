import pandas as pd


def read_dca(path: str) -> pd.DataFrame:
    """
    Read ERS-DCA sheet and add time columns such as start and stop times for fishing activities.

    :param path: path to DCA CSV-file
    :return: Pandas data frame that contains columns "Start tid" and "Stopp tid" as datetime objects.
    """
    dataframe = pd.read_csv(path, delimiter=';', decimal=',')

    # Create necessary time columns from different time columns
    dataframe['Start tid'] = dataframe['Startdato'] + ' ' + dataframe['Startklokkeslett']
    dataframe['Stopp tid'] = dataframe['Stoppdato'] + ' ' + dataframe['Stoppklokkeslett']
    dataframe['Start tid'] = pd.to_datetime(dataframe['Start tid'], format='%d.%m.%Y %H:%M')
    dataframe['Stopp tid'] = pd.to_datetime(dataframe['Stopp tid'], format='%d.%m.%Y %H:%M')
    dataframe['Meldingstid'] = dataframe['Meldingsdato'] + ' ' + dataframe['Meldingsklokkeslett']
    dataframe['Meldingstid'] = pd.to_datetime(dataframe['Meldingstid'], format='%d.%m.%Y %H:%M')

    return dataframe




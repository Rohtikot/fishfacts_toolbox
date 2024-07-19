import os
import pandas as pd
from datetime import datetime
import requests
from zipfile import ZipFile
from io import BytesIO
from tqdm import tqdm


def read_fangstdata(path: str) -> pd.DataFrame:
    # TODO: Add "usecols" to pd.read_csv method to minimize memory usage
    input_df = pd.read_csv(path, delimiter=';', decimal=',')
    return input_df


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


def read_arrivals(year: int) -> pd.DataFrame:
    path = fr"C:\Program Files (x86)\Fishfacts\catch\norway\ers\elektronisk-rapportering-ers-{year}-ankomstmelding-por.csv"
    dataframe = pd.read_csv(path, delimiter=';', decimal=',')

    # Create necessary time columns from different columns
    dataframe['arrival_time'] = dataframe['Ankomstdato'] + ' ' + dataframe['Ankomstklokkeslett']
    dataframe['arrival_time'] = pd.to_datetime(dataframe['arrival_time'], format='%d.%m.%Y %H:%M')

    return dataframe


def read_departures(year: int) -> pd.DataFrame:
    path = fr"C:\Program Files (x86)\Fishfacts\catch\norway\ers\elektronisk-rapportering-ers-{year}-avgangsmelding-dep.csv"
    dataframe = pd.read_csv(path, delimiter=';', decimal=',')

    # Create necessary time columns from different columns
    dataframe['departure_time'] = dataframe['Avgangsdato'] + ' ' + dataframe['Avgangsklokkeslett']
    dataframe['departure_time'] = pd.to_datetime(dataframe['departure_time'], format='%d.%m.%Y %H:%M')

    return dataframe


def download_fangstdata(year: int = datetime.now().year) -> None:
    # Specify the URL of the ZIP file
    url = f"https://register.fiskeridir.no/uttrekk/fangstdata_{year}.csv.zip"

    # Send a GET request to the URL with stream=True to download in chunks
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure we notice bad responses

    # Get the total size of the file in bytes
    total_size = int(response.headers.get('content-length', 0))

    # Create a BytesIO object to store the downloaded content
    zip_file = BytesIO()

    # Download the file in chunks and update the progress bar
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading catch data file') as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            zip_file.write(chunk)
            progress_bar.update(len(chunk))

    # Go back to the beginning of the BytesIO object
    zip_file.seek(0)

    save_dir = r"C:\Program Files (x86)\Fishfacts\catch\norway\catch"

    # Open the ZIP file
    with ZipFile(zip_file) as z:
        # Extract and save the CSV file
        for filename in z.namelist():
            if filename.endswith('.csv'):
                # Extract and save the CSV file with its original name
                file_path = os.path.join(save_dir, filename)
                with z.open(filename) as source, open(file_path, 'wb') as target:
                    target.write(source.read())
                print(f"{filename} has been extracted and saved to {save_dir}.")


def download_ers(year: int = datetime.now().year) -> None:
    url = f"https://register.fiskeridir.no/vms-ers/ERS/elektronisk-rapportering-ers-{year}.zip"
    # Send a HEAD request to get the total file size
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Get the total size of the file in bytes
    total_size = int(response.headers.get('content-length', 0))

    # Create a BytesIO object to store the downloaded content
    zip_file = BytesIO()

    # Download the file in chunks and update the progress bar
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading ERS sheets') as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            zip_file.write(chunk)
            progress_bar.update(len(chunk))

    # Go back to the beginning of the BytesIO object
    zip_file.seek(0)

    save_dir = r"C:\Program Files (x86)\Fishfacts\catch\norway\ers"

    # Open the ZIP file
    with ZipFile(zip_file) as z:
        # Extract and save the CSV files
        for filename in z.namelist():
            if filename.endswith('.csv'):
                # Extract and save the CSV file with its original name
                file_path = os.path.join(save_dir, filename)
                with z.open(filename) as source, open(file_path, 'wb') as target:
                    target.write(source.read())
                print(f"{filename} has been extracted and saved to {save_dir}.")

# TODO: Add functions to read Fangstdata

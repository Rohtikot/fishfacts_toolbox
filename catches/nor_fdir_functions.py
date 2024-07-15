import pandas as pd
from datetime import datetime
import requests
from zipfile import ZipFile
from io import BytesIO
from tqdm import tqdm


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


def download_fangstdata(year: int = datetime.now().year):
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
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading ZIP file') as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            zip_file.write(chunk)
            progress_bar.update(len(chunk))

    # Go back to the beginning of the BytesIO object
    zip_file.seek(0)

    # Open the ZIP file
    with ZipFile(zip_file) as z:
        # Find the CSV file in the ZIP archive
        csv_filename = None
        for filename in z.namelist():
            if filename.endswith('.csv'):
                csv_filename = filename
                break

        if csv_filename is None:
            raise ValueError("No CSV file found in the ZIP archive")

        # Extract the CSV file content
        csv_content = z.read(csv_filename)

    # Generate a filename with year
    timestamp = datetime.now().year
    output_filename = rf'C:\Program Files (x86)\Fishfacts\catch\norway\catch\fangstdata_{timestamp}.csv'

    # Save the CSV content to a file
    with open(output_filename, 'wb') as file:
        file.write(csv_content)

    print(f"Downloaded and extracted the CSV file as {output_filename}")


# TODO: Add functions to read Fangstdata and overføringsmelding
#  add function to update latest (2024) files.

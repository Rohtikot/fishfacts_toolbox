import re
# warning module
import warnings
from tqdm import tqdm
from enum import IntEnum

# import datetime module
from datetime import datetime
from datetime import timedelta

# sleep from time module
from time import sleep

# data processing module
import pandas as pd
# web-scraping modules
import requests
from bs4 import BeautifulSoup

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)


class VesselGroup(IntEnum):
    LONGLINER = 7
    SHRIMP_TRAWLER = 8
    PELAGIC = 9
    TRAWLER = 13
    FREEZING_TRAWLER = 41


def read_vorn_table(url: str, remove_empty_rows: bool = False) -> pd.DataFrame | None:
    """
    Retrieve catch data from Vorn.fo using the provided URL.

    Args:
        - url (str) - the URL for the catch data. This URL contains start date, end date and Vørn's vessel ID for
         each vessel.
        - weight_unit (str) - 'kg' sets the weight units to kg, 'ton' set the weight unit to tonnes. Default: 'Ton'
            can be set to 'dkk' to see the value of the landing
        - remove_empty_rows (bool) - truthy value removes rows with 0 catch, falsy value keeps rows with 0 catch.

    Returns:
        - df_columns (pd.DataFrame): A pandas DataFrame with columns 'Species' and
          'Vessel name - Harbour No. (Call sign)'
            - Catch numbers can be in either kg or tonnes depending on 'weight_unit' argument. Default: 'Ton'

    Raises:
        ValueError: If the weight_unit argument is not 'kg' or 'ton'.
        TypeError: If the remove_empty_rows argument is not a boolean.

    Notes:
        The function fetches data from the specified URL, processes it, and returns a cleaned DataFrame.
        The weight_unit parameter allows conversion of weight to kilograms ('kg') or tonnes ('ton').
        If remove_empty_rows is True, rows with zero catch are removed from the resulting DataFrame.

    Example usage:
        data_url = "https://example.com/catch_data"
        catch_data = get_catch(data_url, remove_empty_rows=True, weight_unit='ton')
    """

    # Helper function to remove harbour number from header
    def remove_harbour_no(strings):
        # Create a pattern that matches the text between the first dash and the first left parenthesis
        pattern = re.compile(r' -\s*[^()]*\s*\(')

        # Remove the matched text from each string
        cleaned_strings = [pattern.sub(' (', s, count=1) for s in strings]

        return cleaned_strings

    # Handle errors

    # Check if remove_empty_rows is a boolean
    if not isinstance(remove_empty_rows, bool):
        raise TypeError("The 'remove_empty_rows' argument must be a boolean.")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Retrieve content from URL
    page = requests.get(url, headers=headers).content.decode('utf-8')

    # Read 'page' into soup
    soup = BeautifulSoup(page, features='html.parser')

    # Find table with class 'tableBoxBorder' and find all headers
    table = soup.find('table', class_='tableBoxBorder')

    # Check if there is any data for given URL
    try:
        header = table.find('tr')
    except AttributeError:
        return None

    # Find all <strong> tags within the first <tr> tag
    strong_tags = header.find_all('strong')

    # Name columns in the dataframe
    headers = [i.text + f' - (kg)' for i in strong_tags]
    headers = remove_harbour_no(headers)
    headers[0] = 'species'

    # Create empty pandas dataframe with columns from 'headers'
    df = pd.DataFrame(columns=headers)

    # Find all rows after header rows
    table_rows = table.find_all('tr')[2:]

    # Find all data for each row and add to pandas dataframe 'df'
    for tr_tag in table_rows:
        td_tags = tr_tag.find_all('td')
        info = [td_tag.get_text() for td_tag in td_tags]
        df.loc[len(df)] = info

    # Clean up dataframe
    df = df.replace(chr(160), '0', regex=True)  # replace no-break spaces with 0

    # Remove thousands separator and convert to integers
    for header in headers[1:]:
        df[header] = df[header].str.replace('.', '').astype(int)

    # Dataframe to return
    df_columns = df[headers]

    # Remove zero-filled if 'remove_empty_rows' argument is truthy
    if remove_empty_rows:
        return df_columns[(df_columns.iloc[:, 1:] != 0).any(axis=1)]
    else:
        return df_columns  # return full data frame


def scrape_vorn(vessel_group: VesselGroup or list[VesselGroup], start: datetime, end: datetime, mode: str) -> pd.DataFrame:
    vessel_group = generate_group(vessel_group)
    dates = generate_date_range(start, end)

    dfs = []

    for group in vessel_group:
        group_num = group
        group_name = group.name
        for date in (pbar := tqdm(dates, total=len(dates))):
            pbar.set_description(f'Processing: {date} - {group_name}')
            url = generate_vorn_url(group_num, date, mode)
            data = read_vorn_table(url, remove_empty_rows=True)
            if data is not None:
                data = data.drop('Tils. (kg)', axis=1)
                data = data[data['species'] != 'Tils.']
                data['date'] = date

                # Identify the vessel columns dynamically by excluding 'Species' and 'date'
                vessel_columns = data.columns.difference(['species', 'date'])

                # Melt the DataFrame to unpivot vessel columns to rows
                data_melted = pd.melt(
                    data,
                    id_vars=['species', 'date'],  # Columns to keep
                    value_vars=vessel_columns,    # Columns to unpivot
                    var_name='vessel_name',       # New column name for vessel
                    value_name='value (kg)'       # New column name for catch value
                )

                data_melted['vessel_type'] = group_name.lower()

                # Extract and clean the vessel name from the column names
                data_melted['vessel_name'] = data_melted['vessel_name'].str.extract(r'^(.*) -')[0]

                split_cols = data_melted['vessel_name'].str.split(r' \(', expand=True)
                data_melted['vessel_name'] = split_cols[0].str.strip()
                data_melted['radio_callsign'] = split_cols[1].str.replace(r'\)', '', regex=True).str.strip()

                data_melted = data_melted[['date', 'vessel_name', 'radio_callsign', 'vessel_type', 'species', 'value (kg)']]

                dfs.append(data_melted)

                sleep(1)

    dfs = pd.concat(dfs)
    return dfs



def generate_date_range(start: datetime, end: datetime) -> list[datetime]:
    """Generate list of datetimes in string format: dd-mm-yyyy excluding end date."""
    # Initialize an empty list to store the dates
    date_list = []

    # Generate all dates between the start and end date (inclusive)
    current_date = start
    while current_date < end:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    return date_list


def generate_vorn_url(vessel_group: int, date: datetime, mode: str) -> str:
    """Generate url depending on date and mode (Avreiðingar- or vektarseðil)."""
    date = date.strftime("%d-%m-%Y")

    # avreiðingar- or vektarseðil
    if mode == 'avr':
        url = fr"https://hagtol.vorn.fo/fvePortal.exe/ShowLandingRepShip?SHIPGROUPID={vessel_group}&PARAMTYPE=1&BEGIN={date}&END={date}&SUMCOLUMN=AMOUNT&REGIONS=1,2,3,4,5,6,7,9,10,8&OnlyFBK=0"
    elif mode == 'vekt':
        url = fr"https://hagtol.vorn.fo/fvePortal.exe/ShowWeightNoteRepShipgroup?SHIPGROUPID={vessel_group}&PARAMTYPE=1&BEGIN={date}&END={date}&ZONE_MUST_BE_REGISTERED=false&REGIONS_CHK=0&REGIONS="

    return url


def generate_group(vessel_group: VesselGroup or list[VesselGroup]) -> list[VesselGroup]:
    """Determine if vessel group is string or list and return list of tuples"""

    if isinstance(vessel_group, VesselGroup):
        return [vessel_group]
    elif isinstance(vessel_group, list):
        return vessel_group


if __name__ == '__main__':
    start, end = datetime(2023, 1, 1), datetime(2023, 2, 1)

    res = scrape_vorn(VesselGroup.PELAGIC, start, end, 'avr')
    print(res)
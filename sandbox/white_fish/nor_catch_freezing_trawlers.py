import datetime
from typing import Tuple
import matplotlib.dates as mdates

import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.0f}'.format)


def main():
    # Current Norwegian freezing trawlers on Fishfacts database
    year = 2023
    radio_callsigns = [
        "LMAC",
        "LDAL",
        "LDDG",
        "LHMF",
        "LLOP",
        "LLAJ",
        "LLAY",
        "LCMP",
        "LLDH",
        "LCLP",
        "LDDF",
        "3YHX",
        "3YYB",
        "LDCO",
        "LNKS",
        "LHXV",
        "LMBG",
        "LDBR",
        "LDBT",
        "LDSF",
        "LDNV",
        "LFGW",
        "LJWI",
        "LEBB",
        "LEGQ",
        "LJPH",
        "LFBW",
        "LLIA",
        "LIPZ",
        "LDAR",
        "LFOC",
        "JXRX",
        "LFNT",
        "LFRA",
        "LFNX",
        "LFPE",
        "LGJY",
        "LFVX",
        "JXNX",
        "JXJU"
    ]

    res = find_seasons_for_species_from_ffnft24(year, radio_callsigns)[2]
    start_date = datetime.date(year, 1, 1)
    days = res['day']
    dates = [start_date + datetime.timedelta(days=int(day)) for day in days]
    reke = res['Dypvannsreke']
    torsk = res['Torsk']
    redfish = res['Snabeluer']
    redfish_norvegicus = res['Uer (vanlig)']
    sei = res['Sei']
    hyse = res['Hyse']
    haddock = res['Blåkveite']

    # Create a figure with two subplots
    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(7, 1, 1)
    ax2 = fig.add_subplot(7, 1, 2, sharex=ax1)
    ax3 = fig.add_subplot(7, 1, 3, sharex=ax1)
    ax4 = fig.add_subplot(7, 1, 4, sharex=ax1)
    ax5 = fig.add_subplot(7, 1, 5, sharex=ax1)
    ax6 = fig.add_subplot(7, 1, 6, sharex=ax1)
    ax7 = fig.add_subplot(7, 1, 7, sharex=ax1)
    ax1.bar(dates, torsk)
    ax2.bar(dates, sei)
    ax3.bar(dates, hyse)
    ax4.bar(dates, reke)
    ax5.bar(dates, redfish)
    ax6.bar(dates, redfish_norvegicus)
    ax7.bar(dates, haddock)
    # Formatting the x-axis to show months
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7]:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.grid(True)
        # Hide x labels on all but the last plot
        if ax != ax7:
            plt.setp(ax.get_xticklabels(), visible=False)
        else:
            plt.setp(ax.get_xticklabels(), rotation=45)

    # Labeling the y-axes
    ax1.set_ylabel('Toskur')
    ax2.set_ylabel('Upsi')
    ax3.set_ylabel('Hýsa')
    ax4.set_ylabel('Rækjur')
    ax5.set_ylabel('Sebastestes mentella')
    ax6.set_ylabel('Sebastestes norvegicus')
    ax7.set_ylabel('Svartkalvi')

    # Labeling the x-axis for the last subplot
    ax6.set_xlabel('Month')

    # Adjust layout to make room for x labels
    plt.tight_layout()
    fig.suptitle(f'Tons fiskað hvønn dag í {year}. 40 norskir flakatrolarar úr Fishfacts databasa.')
    plt.subplots_adjust(left=0.1, right=0.6, top=0.8, bottom=0.1)

    # Showing the plot
    plt.show()


def find_biggest_species_groups_from_ffnft24(year: int, radios: list[str]) -> pd.DataFrame:
    """Find the biggest species groups that have been fished by FFNFT24"""

    path = fr"C:\Users\tokit\OneDrive\Desktop\Hvítfisk\norway_catch\catch\fangstdata_{year}.csv"

    df = pd.read_csv(path, delimiter=';', decimal=',', low_memory=False)

    _df = df[
        (df['Radiokallesignal (seddel)'].isin(radios))
    ]

    pivot = _df.pivot_table(index=['Fartøynavn', 'Radiokallesignal (seddel)'], columns='Art - FDIR',
                            values='Produktvekt', fill_value=0, aggfunc='sum').reset_index()

    # Sort column order
    grouped = _df.groupby('Art - FDIR')['Produktvekt'].sum()
    grouped.sort_values(inplace=True, ascending=False)
    species = grouped.index.tolist()
    pivot = pivot[['Fartøynavn', 'Radiokallesignal (seddel)'] + species]
    pivot.sort_values(by='Radiokallesignal (seddel)', inplace=True, ascending=False)

    total_row = pivot.sum()
    pivot.loc['Total'] = total_row

    return pivot


def find_seasons_for_species_from_ffnft24(year: int, radios: list[str]) -> pd.DataFrame:
    path = fr"C:\Users\tokit\OneDrive\Desktop\Hvítfisk\norway_catch\ers\elektronisk-rapportering-ers-{year}-fangstmelding-dca.csv"

    df = pd.read_csv(path, delimiter=';', decimal=',')
    df = create_time_columns(df)
    df = df[
        (df['Radiokallesignal (ERS)'].isin(radios))
    ]

    df['Rundvekt'] = df['Rundvekt'] / 1000
    df['month'] = df['center_time'].dt.month
    df['week'] = df['center_time'].dt.isocalendar().week
    df['day'] = df['center_time'].dt.dayofyear

    pivot_month = df.pivot_table(index='month', columns='Art - FDIR', values='Rundvekt', fill_value=0, aggfunc='sum').reset_index()
    pivot_week = df.pivot_table(index='week', columns='Art - FDIR', values='Rundvekt', fill_value=0, aggfunc='sum').reset_index()
    pivot_day = df.pivot_table(index='day', columns='Art - FDIR', values='Rundvekt', fill_value=0, aggfunc='sum').reset_index()

    return pivot_month, pivot_week, pivot_day


def create_time_columns(_df: pd.DataFrame) -> pd.DataFrame:
    new_df = _df.copy()

    # Create necessary time columns from different time columns
    new_df['start'] = new_df['Startdato'] + ' ' + new_df['Startklokkeslett']
    new_df['stop'] = new_df['Stoppdato'] + ' ' + new_df['Stoppklokkeslett']
    new_df['start'] = pd.to_datetime(new_df['start'], format='%d.%m.%Y %H:%M')
    new_df['stop'] = pd.to_datetime(new_df['stop'], format='%d.%m.%Y %H:%M')
    new_df['center_time'] = new_df['start'] + (new_df['stop'] - new_df['start']) / 2
    new_df['Meldingstid'] = new_df['Meldingsdato'] + ' ' + new_df['Meldingsklokkeslett']
    new_df['Meldingstid'] = pd.to_datetime(new_df['Meldingstid'], format='%d.%m.%Y %H:%M')

    # Drop unnecessary columns
    new_df = new_df.drop(columns=['Stoppklokkeslett', 'Startklokkeslett', 'Startdato', 'Stoppdato', 'Meldingsdato',
                                  'Meldingsklokkeslett'])

    return new_df


if __name__ == '__main__':
    main()

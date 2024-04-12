import pandas as pd
import numpy as np
from get_exponents import get_exponents

pd.set_option('display.width', None)


def main():
    path = '../Arctic_Voyager_oil_testing_locally.xlsx'
    df = pd.read_excel(path)
    df = wind_index(df).dropna()
    ship_dims = {
        "gr_ton": 2250,
        "build_year": 1997,
        "me_pwr": 7380,
        "len_overall": 71
    }

    vessel_name = 'Arctic Voyager'
    exp = get_exponents(vessel_name)

    df = calculate_oil_consumption(df, ship_dims, exp)
    print(df)


def wind_index(wi_df: pd.DataFrame) -> pd.DataFrame:
    # calculate head on factor
    wi_df['head_on_factor'] = np.arccos(
        np.cos(np.radians(wi_df['heading'])) * np.cos(np.radians(wi_df['wind_dir'])) +
        np.sin(np.radians(wi_df['heading'])) * np.sin(np.radians(wi_df['wind_dir']))) \
                              / np.pi

    # calculate wind index (head on factor*wind_speed)
    wi_df['wind_index'] = wi_df['wind_speed'] * wi_df['head_on_factor']

    return wi_df


def calculate_oil_consumption(input_df: pd.DataFrame, ship_dimensions: dict, c_exponents: list) -> pd.DataFrame:
    # Exponents
    m, n, o, p, q, r, boost, lf = c_exponents

    gr_ton = ship_dimensions['gr_ton']
    build_year = ship_dimensions['build_year']
    me_pwr = ship_dimensions['me_pwr']
    len_overall = ship_dimensions['len_overall']

    # find constants c1 or c2 based on ship dimensions
    c1 = (((gr_ton / 2538) ** m) * ((2014 / build_year) ** n) * ((me_pwr / (4000 + boost)) ** o) * (
            (gr_ton * (4000 + boost) / (me_pwr * 2538)) ** p)) * lf
    c2 = (((gr_ton * 70 / (len_overall * 2538)) ** q) * ((2014 / build_year) ** n) * (
            (me_pwr / (4000 + boost)) ** r)) * lf

    formulas = {
        'f1': lambda v, wi: 152.148641822216 * v + 34.9100089057054 * wi + 86.1234932728002,
        'f2': lambda v: 156.23 + 120.77 * v,
        'f3': lambda v, u, hf: 2.76103347155361 * v + 57.7767237861278 * u + 104.711251206601 * hf + 114.922736669769,
        'f4': lambda v, wi: 63.9672412288041 * v + 10.689266333751 * wi + 340.738581364124,
        'f5': lambda v: 198.4 + 135.43 * v,
        'f6': lambda v, wi: -155.341163478944 * v ** 2 - 24.2969886960548 * wi * v + 1583.44666304855 * v + 1.62359341206797 * wi ** 2 + 80.7101007829525 * wi - 2937.34177867731,
        'f7': lambda v: 622.04 + 70.59 * v,
        'f8': lambda v, wi: 2.68851515895423 * v ** 3 - 6.33754710698395 * wi * v ** 2 - 82.0934140487749 * v ** 2 + 13.1835243251615 * wi ** 2 * v + 75.4987641439067 * wi * v + 902.097506066174 * v + 0.390636638455049 * wi ** 3 - 173.4547124061 * wi ** 2 + 49.9828397981443 * wi - 3006.74441010485,
        'f9': lambda v, wi: 2.68851515895423 * v ** 3 - 6.33754710698395 * wi * v ** 2 - 82.0934140487749 * v ** 2 + 13.1835243251615 * wi ** 2 * v + 75.4987641439067 * wi * v + 902.097506066174 * v + 0.390636638455049 * wi ** 3 - 173.4547124061 * wi ** 2 + 49.9828397981443 * wi - 3006.74441010485,
        'f10': lambda v, u, hf: 60.16707947782 * v + 21.878464140581 * u - 135.68751476082 * hf - 250.326709876776,
        'f11': lambda v: 273.56 + 11.29 * v,
        'f12': lambda v: 426.52 + 12.17 * v,
    }

    for index, row in input_df.iterrows():
        v = row['speed']
        wi = row['wind_index']
        u = row['wind_speed']
        hf = row['head_on_factor']

        if v < 0.3:
            c = 67.71
        elif 0.3 <= v < 1.1:
            f1 = formulas['f1'](v, wi)
            c = f1 if 50 < f1 < 500 else formulas['f2'](v)
        elif 1.1 <= v < 3.5:
            f3 = formulas['f3'](v, u, hf)
            f4 = formulas['f4'](v, wi)
            c = f3 if 250 < f3 < 800 else (f4 if 250 < f4 < 800 else formulas['f5'](v))
        elif 3.5 <= v < 6:
            f6 = formulas['f6'](v, wi)
            c = f6 if 500 < f6 < 1400 else formulas['f7'](v)
        else:
            if v < 11:
                f8 = formulas['f8'](v, wi)
                f10 = formulas['f10'](v, u, hf)
                c = f8 if 250 < f8 < 950 else (
                    f10 if 250 < f10 < 950 else formulas['f11'](v) if v < 10 else formulas['f12'](v))
            else:
                f9 = formulas['f9'](v, wi)
                f10 = formulas['f10'](v, u, hf)
                c = f9 if 250 < f9 < 950 else (f10 if 250 < f10 < 950 else formulas['f12'](v))

        # multiply by constant c1 or c2 depending on vessel speed
        if v <= 6:
            c = c * c1
        else:
            c = c * c2

        # convert hourly consumption to quarterly (15 min) (if dataframe is in 15 minute intervals)
        c /= 4

        # multiply by 0.25 (4 data points per hour)
        input_df.at[index, 'consumption l'] = c

    return input_df


if __name__ == '__main__':
    main()

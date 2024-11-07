import matplotlib.pyplot as plt
import pandas as pd
from oil_calculation import *
from datetime import datetime
from wind_index import *
import numpy as np
from instantaneous_consumption import plot_scenarios


def main():
    data = {'speed': np.arange(0, 14, 0.1)}
    df = pd.DataFrame(data)

    for index, row in df.iterrows():
        v = row['speed']
        wi = 0  #row['wind_index']
        u = 0  #row['wind_speed']
        hf = 0  #row['head_on_factor']

        if v < 0.3:
            c = 67.71
        elif 0.3 <= v < 1.1:
            f1 = formulas['f1'](v, wi)
            c = f1 if 50 < f1 < 500 else formulas['f2'](v)
        elif 1.1 <= v < 3.5:
            f3 = formulas['f3'](v, u, hf)
            f4 = formulas['f4'](v, wi)
            c = f3 if 250 < f3 < 800 else (f4 if 250 < f4 < 800 else formulas['f5'](v))

            # c = c * 0.85  # TODO: testing by lowering consumption
        elif 3.5 <= v < 6:
            f6 = formulas['f6'](v, wi)
            c = f6 if 500 < f6 < 1400 else formulas['f7'](v)

            # c = c * 0.75  # TODO: testing by lowering consumption
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

        df.at[index, 'consumption l'] = c

    plt.figure(figsize=(10, 6))
    x = df['speed']
    y = df['consumption l']
    plt.plot(x, y, color='red')
    plt.title('Oil Consumption in no Wind')
    plt.xlabel('Speed [knots]')
    plt.ylabel('Consumption [l/h]')

    # plot scatter dots
    plot_scenarios()

    plt.show()


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


main()

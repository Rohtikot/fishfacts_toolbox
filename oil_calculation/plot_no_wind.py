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
    'f1': lambda v, wi: 152.15 * v + 34.91 * wi + 86.12,
    'f2': lambda v: 156.23 + 120.77 * v,
    'f3': lambda v, u, hf: 89.00 * hf + 49.11 * u + 2.35 * v + 97.68,
    'f4': lambda v, wi: 54.37 * v + 9.09 * wi + 289.63,
    'f5': lambda v: 198.4 + 135.43 * v,
    'f6': lambda v, wi: -116.51 * v**2 - 18.22 * v * wi + 1187.58 * v + 1.22 * wi**2 + 60.53 * wi - 2203.01,
    'f7': lambda v: 52.94 * v + 466.53,
    'f8': lambda v, wi: 2.69 * v ** 3 - 6.34 * wi * v ** 2 - 82.09 * v ** 2 + 13.18 * wi ** 2 * v + 75.5 * wi * v + 902.1 * v + 0.39 * wi ** 3 - 173.45 * wi ** 2 + 49.98 * wi - 3006.74,
    'f9': lambda v, wi: 2.69 * v ** 3 - 6.34 * wi * v ** 2 - 82.09 * v ** 2 + 13.18 * wi ** 2 * v + 75.5 * wi * v + 902.1 * v + 0.39 * wi ** 3 - 173.45 * wi ** 2 + 49.98 * wi - 3006.74,
    'f10': lambda v, u, hf: 60.17 * v + 21.88 * u - 135.69 * hf - 250.33,
    'f11': lambda v: 273.56 + 11.29 * v,
    'f12': lambda v: 426.52 + 12.17 * v,
}


main()

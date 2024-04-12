import os
import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)


def get_exponents(vessel_name: str) -> list[float]:
    cluster = get_cluster(vessel_name)

    exp = {
        0: [0.583, 42.2, 0.1334, 0.5498, 0.4, 0.12, 0, 0.96],
        1: [0.583, 42.2, 0.1334, 0.5498, 0.4, 0.12, 0, 0.96],
        2: [-0.127, 41.49, -0.5966, -0.1702, -0.31, -0.61, 5000, 1.0],
        3: [0.174, 42.09, 0.0234, 0.30, 0.29, 0.01, 0, 1.0],
        4: [0.574, 40.09, 0.0234, 0.3198, 0.29, 0.001, 0, 1.02]
    }

    return exp[cluster]


def get_cluster(vessel_name: str) -> int or None:
    path = f"{os.path.dirname(__file__)}/vessel_clusters.csv"
    df = pd.read_csv(path)

    if vessel_name in df['name'].values:
        cluster = df[df['name'] == vessel_name]['cluster'].iloc[0]
    else:
        return 0

    return cluster

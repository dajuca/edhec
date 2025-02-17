import numpy as np
import pandas as pd
#import pygeohash as gh

from luxury.utils import simple_time_and_memory_tracker

def transform_nan_features(X: pd.DataFrame) -> np.ndarray:
    assert isinstance(X, pd.DataFrame)

    mask = ~np.isnan(y) & ~np.isinf(y)
    X = X[mask]
    y = y[mask]

    return X, y



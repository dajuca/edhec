import numpy as np
import pandas as pd
import joblib

from google.cloud import bigquery
from pathlib import Path
from colorama import Fore, Style
from dateutil.parser import parse

from luxury.params import *
from luxury.ml_logic.data import clean_data, get_data, load_data_to_bq
from luxury.ml_logic.preprocessor import preprocess_features
from luxury.ml_logic.registry import save_model, save_results, load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

def preprocess() -> None:
    """
    - Query the raw dataset from BigQuery
    - Process query data
    - Store processed data on BigQuery
    """

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess" + Style.RESET_ALL)

    query = f"""
        SELECT {"","".join(COLUMN_NAMES_RAW)}
        FROM `{GCP_PROJECT_EDHEC}`.{BQ_DATASET}.{PROJECT_TABLE}
        WHERE brand = '{BRAND}' AND life_span = {LIFE_SPAN}
        ORDER BY life_span_date DESC
        """

    data_path = Path(LOCAL_DATA_PATH).joinpath("raw", f"query_{BRAND}_{LIFE_SPAN}.csv")
    data_query = get_data(
        query=query,
        gcp_project=GCP_PROJECT_EDHEC,
        path=data_path,
        data_has_header=True
    )

    data_clean = clean_data(data_query)
    X = data_clean.drop("price", axis=1)
    y = data_clean[["price"]]
    X_processed = preprocess_features(X)

    data_processed_with_timestamp = pd.DataFrame(np.concatenate((
        data_clean[["life_span_date"]],
        X_processed,
        y,
    ), axis=1))

    load_data_to_bq(
        data_processed_with_timestamp,
        gcp_project=GCP_PROJECT_EDHEC,
        bq_dataset=BQ_DATASET,
        table=f'processed_{PROJECT_TABLE}',
        truncate=True
    )
    
    print("✅ preprocess() done")

def train() -> None:
    """
    - Download processed data from BigQuery
    - Train a KNeighborsRegressor model on it
    - Save the model
    - Compute & save a validation performance metric
    """
    
    print(Fore.MAGENTA + "\n ⭐️ Use case: train" + Style.RESET_ALL)
    query = f"""
        SELECT * EXCEPT(_0)
        FROM `{GCP_PROJECT_EDHEC}`.{BQ_DATASET}.processed_{PROJECT_TABLE}
        ORDER BY life_span_date DESC
    """
    
    data_processed_cache_path = Path(LOCAL_DATA_PATH).joinpath("processed", f"processed_{PROJECT_TABLE}.csv")
    data_processed = get_data(
        gcp_project=GCP_PROJECT_EDHEC,
        query=query,
        cache_path=data_processed_cache_path,
        data_has_header=False
    )
    
    X = data_processed['brand', 'currency', 'collection']
    y = data_processed.price
    
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    X_processed = encoder.fit_transform(X)
    joblib.dump(encoder, LOCAL_DATA_PATH + "/encoder.pkl")
    
    X_train, X_val, y_train, y_val = train_test_split(X_processed, y, test_size=0.2, random_state=0)
    
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)
    
    print(f"📊 Mean Squared Error: {mse:.4f}")
    print(f"📈 R-squared: {r2:.4f}")
    
    save_model(model=model)
    save_results(params={"model": "KNeighborsRegressor"}, metrics={"mse": mse, "r2": r2})
    print("✅ train() done")

def predict(X_pred: pd.DataFrame) -> np.ndarray:
    print(Fore.MAGENTA + "\n ⭐️ Use case: predict" + Style.RESET_ALL)
    
    model = load_model()
    encoder = joblib.load(LOCAL_DATA_PATH + "/encoder.pkl")
    
    X_processed = encoder.transform(X_pred)
    y_pred = model.predict(X_processed)
    
    print(f"✅ Prediction done: {y_pred}")
    return y_pred

if __name__ == '__main__':
    try:
        preprocess()
        train()
        X_sample = pd.DataFrame({"brand": ["Rolex"], "currency": ["USD"], "collection": ["Daytona"]})  # Replace with actual features
        predict(X_sample)
    except Exception as e:
        import traceback
        traceback.print_exc()

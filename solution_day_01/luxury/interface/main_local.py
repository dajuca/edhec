import numpy as np
import pandas as pd
import joblib
from google.cloud import bigquery
from pathlib import Path
from colorama import Fore, Style
from luxury.params import *
from luxury.ml_logic.data import clean_data
from luxury.ml_logic.registry import save_model, save_results, load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score



def preprocess_and_train() -> None:
    """
    - Query the raw dataset from BigQuery
    - Clean and preprocess data
    - Train a KNeighborsRegressor model on it
    - Save the model
    - Compute & save a validation performance metric
    """

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess_and_train" + Style.RESET_ALL)

    query = f"""
    SELECT {", ".join(COLUMN_NAMES_RAW)}
    FROM `{GCP_PROJECT_EDHEC}.{BQ_DATASET}.{PROJECT_TABLE}`
    WHERE brand = '{BRAND}' AND life_span = '{LIFE_SPAN}'
    ORDER BY life_span_date DESC
    """

    data_path = Path(LOCAL_DATA_PATH).joinpath("raw", f"query_{BRAND}_{LIFE_SPAN}.csv")
    data_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    data_exists = data_path.is_file()

    if data_exists:
        print("Loading data from local CSV...")
        data = pd.read_csv(data_path)
    else:
        print("Loading data from Querying Big Query server...")
        client = bigquery.Client(project=GCP_PROJECT_EDHEC)
        print(query)
        query_job = client.query(query)
        result = query_job.result()
        data = result.to_dataframe()
        data.to_csv(data_path, header=True, index=False)

    data = clean_data(data)
    
    X = data.drop(columns=["price"])
    y = data["price"]
    
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    X_processed = encoder.fit_transform(X)
    
    joblib.dump(encoder, Path(LOCAL_DATA_PATH).joinpath("encoder.pkl"))

    X_train, X_val, y_train, y_val = train_test_split(X_processed, y, test_size=0.2, random_state=0)
    
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)

    print(f"📊 Mean Squared Error: {mse:.4f}")
    print(f"📈 R-squared: {r2:.4f}")
    
    model_path = Path(LOCAL_DATA_PATH).joinpath("training_outputs", "models")
    model_path.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    save_model(model=model)

    save_results(params={"model": "KNeighborsRegressor"}, metrics={"mse": mse, "r2": r2})
    print("✅ preprocess_and_train() done")



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
        preprocess_and_train()
        X_sample = pd.DataFrame({"brand": ["Rolex"], "currency": ["USD"], "collection": ["Daytona"]})  # Replace with actual features
        predict(X_sample)
    except Exception as e:
        import traceback
        traceback.print_exc()

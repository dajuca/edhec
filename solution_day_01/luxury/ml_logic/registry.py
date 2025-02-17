import glob
import os
import time
import pickle
from pathlib import Path
import joblib
from sklearn.neighbors import KNeighborsRegressor
from sklearn.base import BaseEstimator 
from typing import Any
from google.cloud import storage
from luxury.params import *

def save_results(params: dict, metrics: dict) -> None:

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Ensure directories exist before saving
    params_dir = Path(LOCAL_REGISTRY_PATH).joinpath("params")
    metrics_dir = Path(LOCAL_REGISTRY_PATH).joinpath("metrics")
    params_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    # Save params locally
    if params is not None:
        params_path = params_dir.joinpath(f"{timestamp}.pickle")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # Save metrics locally
    if metrics is not None:
        metrics_path = metrics_dir.joinpath(f"{timestamp}.pickle")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    print("✅ Results saved locally")



def save_model(model: BaseEstimator = None) -> None:

    if model is None:
        print("⚠️ No model provided to save.")
        return

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Ensure the directory exists before saving or else create it !! 
    model_dir = Path(LOCAL_REGISTRY_PATH).joinpath("models")
    model_dir.mkdir(parents=True, exist_ok=True)  

    model_path = model_dir.joinpath(f"{timestamp}.pkl")
    
    joblib.dump(model, model_path) 
    print(f"✅ Model saved locally at {model_path}")

    # if MODEL_TARGET == "gcs":
    #     print("\nUploading model to Google Cloud Storage...")

    #     client = storage.Client()
    #     bucket = client.bucket(BUCKET_NAME)
    #     blob = bucket.blob(f"models/{timestamp}.pkl")
    #     blob.upload_from_filename(model_path)

    #     print("✅ Model saved to GCS")

    return None



def load_model(stage="Production") -> KNeighborsRegressor:


    if MODEL_TARGET == "local":
        print("\nLoad latest KNeighborsRegressor model from local registry...")

        # Get the latest model version name by the timestamp on disk
        local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
        local_model_paths = glob.glob(f"{local_model_directory}/*.pkl")  

        if not local_model_paths:
            print("⚠️ No saved models found locally.")
            return None

        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

        print(f"\nLoading latest model from disk: {most_recent_model_path_on_disk}")

        latest_model = joblib.load(most_recent_model_path_on_disk) 

        print("✅ KNeighborsRegressor model loaded from local disk")
        return latest_model


    # elif MODEL_TARGET == "gcs":
    #     print("\nLoad latest KNeighborsRegressor model from Google Cloud Storage...")

    #     client = storage.Client()
    #     blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="models/"))

    #     if not blobs:
    #         print("⚠️ No models found in GCS.")
    #         return None

    #     # Sort files by name (assuming timestamp in filename helps order)
    #     latest_blob = sorted(blobs, key=lambda x: x.name)[-1]

    #     # Download the model
    #     local_model_temp_directory = os.path.join(LOCAL_REGISTRY_PATH, "models", "temp")

    #     latest_blob.download_to_filename(local_model_temp_directory)

    #     print(f"\nModel downloaded from GCS: {latest_blob.name}")

    #     latest_model = joblib.load(local_model_temp_directory)  # ✅ Correctly loading joblib model

    #     print("✅ KNeighborsRegressor model loaded from GCS")
    #     return latest_model

    else:
        print("⚠️ MODEL_TARGET not recognized. No model loaded.")
        return None

if __name__ == "__main__":
    if MODEL_TARGET == "gcs":
        print("saving to cloud")
    else:
        print("saving locally")
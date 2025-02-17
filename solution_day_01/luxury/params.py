import os
import numpy as np
##################  VARIABLES  ##################

MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_PROJECT_EDHEC = os.environ.get("GCP_PROJECT_EDHEC")
GCP_REGION = os.environ.get("GCP_REGION")
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
PROJECT_TABLE = os.environ.get("PROJECT_TABLE")
BRAND = os.environ.get("BRAND")
LIFE_SPAN = os.environ.get("LIFE_SPAN")
##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), ".luxury", "mlops", "data")
LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".luxury", "mlops", "training_outputs")
COLUMN_NAMES_RAW = ['uid', 'brand', 'url', 'price', 'currency', 'image_url', 'collection', 'reference_code', 'life_span_date', 'life_span', 
                    'price_before', 'price_difference', 'price_percent_change', 'price_changed']
DTYPES_RAW = {
    "uid": "int32",
    "brand": "string",
    "url": "string",
    "price": "Int32",
    "currency": "string",
    "image_url": "string",
    "collection": "string",
    "reference_code": "string",
    "country": "string",
    "life_span_date": "datetime64[ns, UTC]",
    "life_span": "string",
    "price_before": "float32",
    "price_difference": "Int32",
    "price_percent_change": "float32",
    "price_changed": "float32",
    "is_new": "float32"
}
DTYPES_PROCESSED = np.float32

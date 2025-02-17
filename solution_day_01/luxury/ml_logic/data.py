import pandas as pd

from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path

from luxury.params import *

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data by:
    - Assigning correct dtypes to each column that exists in the dataframe
    - Removing buggy or irrelevant transactions
    """

    # Apply dtypes only to columns that exist in `df`
    available_columns = {col: dtype for col, dtype in DTYPES_RAW.items() if col in df.columns}
    df = df.astype(available_columns)

    # Remove duplicates and NaNs
    df = df.drop_duplicates().dropna(how="any", axis=0)

    # Ensure key columns do not contain zero or missing values
    key_columns = ["reference_code", "price", "collection", "brand"]
    for col in key_columns:
        if col in df.columns:
            df = df[df[col] != 0]

    print("✅ Data cleaned")

    return df


def get_data(
        gcp_project:str,
        query:str,
        path:Path,
        data_has_header=True
    ) -> pd.DataFrame:
    """
    Retrieve `query` data from BigQuery
    """
    if path.is_file():
        print(Fore.BLUE + "\nLoad data from local CSV..." + Style.RESET_ALL)

        df = pd.read_csv(path, header='infer' if data_has_header else None)
    else:
        print(Fore.BLUE + "\nLoad data from BigQuery server..." + Style.RESET_ALL)

        client = bigquery.Client(project=gcp_project)
        query_job = client.query(query)
        result = query_job.result()
        df = result.to_dataframe()

        # Store as CSV if the BQ query returned at least one valid line
        if df.shape[0] > 1:
            df.to_csv(path, header=data_has_header, index=False)

    print(f"✅ Data loaded, with shape {df.shape}")

    return df

def load_data_to_bq(
        data: pd.DataFrame,
        gcp_project:str,
        bq_dataset:str,
        table: str,
        truncate: bool
    ) -> None:
    """
    - Save the DataFrame to BigQuery
    - Empty the table beforehand if `truncate` is True, append otherwise
    """

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{gcp_project}.{bq_dataset}.{table}"
    print(Fore.BLUE + f"\nSave data to BigQuery @ {full_table_name}...:" + Style.RESET_ALL)

    
    client = bigquery.Client()

    # Define write mode and schema
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    print(f"\n{'Write' if truncate else 'Append'} {full_table_name} ({data.shape[0]} rows)")

    # Load data
    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  

    print(f"✅ Data saved to bigquery, with shape {data.shape}")

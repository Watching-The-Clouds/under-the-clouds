import boto3
import pandas as pd
import io
import os

data_bucket = os.environ.get("INGESTION_BUCKET")

def create_s3_client():
    """
    Creates an S3 client using boto3.

    Returns:
        An S3 client
    """
    return boto3.client("s3")

def fetch_csv_from_s3(s3_client, data_bucket, key):
    """Fetches data in .csv format from ingested S3 bucket.
    
    Parameters:
        s3_client: S3 client
        data_bucket: name of the ingested bucket (stored in .env)
        key: reference to the file in the S3 bucket

    Returns:
        a string containing .csv data    
    """
    try:
        obj = s3_client.get_object(Bucket=data_bucket, Key=key)
        csv_data = obj['Body'].read().decode('utf-8')
        return csv_data
    
    except Exception as e:
        print(f"Error fetching file from S3 for key '{key}': {e}")
        return None
    
def convert_csv_to_dataframe(csv_data):
    """Converts data from .csv format into a Pandas dataframe.
    
    Parameters:
        a string containing .csv data    

    Returns:
        a Pandas dataframe  
    """
    try:
        file_stream = io.StringIO(csv_data)
        return pd.read_csv(file_stream)
    
    except Exception as e:
        print(f"Error converting CSV data to DataFrame: {e}")
        return None

def update_dataframe(df):
    pass

def calculate_time_increase():
    # Still 'per mile' and then multuiply by user input as required for final output
    pass

def calculate_cost_increase():
    # Still 'per mile' and then multuiply by user input as required for final output
    pass

def convert_to_parquet():
    pass

def store_in_s3(s3_client, parquet_file, bucket_name, file_name):
    """
    Uploads parquet file to a named AWS S3 bucket.

    Parameters:
        s3_client: boto3 S3 client
        parquet_file: transformed data in parquet format
        bucket_name (str): S3 bucket name
        file_name (str): S3 file directory and file name
    """
    
    s3_client.put_object(Body=parquet_file, Bucket=bucket_name, Key=file_name)
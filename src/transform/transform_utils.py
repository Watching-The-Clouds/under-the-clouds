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

def get_data_frame(s3_client, data_bucket, key):
    """Fetches and returns a DataFrame from ingested S3 bucket.
    
    Parameters:
        s3_client: S3 client
        data_bucket: name of the ingested bucket (stored in .env)
        key: reference to the file in the S3 bucket     
    """
    try:
        obj = s3_client.get_object(Bucket=data_bucket, Key=key)
        file_stream = io.StringIO(obj['Body'].read().decode('utf-8'))
        return pd.read_csv(file_stream)
    
    except Exception as e:
        print(f"Error loading DataFrame for key '{key}': {e}")
        return None
    
def update_data_frame():
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
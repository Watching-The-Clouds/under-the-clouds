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
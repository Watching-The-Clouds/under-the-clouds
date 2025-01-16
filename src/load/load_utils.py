from pprint import pprint
from io import BytesIO
from sqlalchemy import create_engine
import boto3
import pandas as pd
import logging

def create_s3_client():
    """
    Creates an S3 client using boto3.

    Returns:
        An S3 client
    """
    return boto3.client("s3")

def fetch_parquet_from_s3(s3_client, processed_bucket, file_directory):
    """Fetches data in .parquet format from processed S3 bucket.

    Parameters:
        s3_client: S3 client
        data_bucket: name of the processed bucket (stored in .env)
        key: reference to the file in the S3 bucket

    Returns:
        a BytesIO buffer containing binary data of the Parquet file
    """

    obj = s3_client.get_object(Bucket=processed_bucket, Key=file_directory)
    
    parquet_buffer = BytesIO(obj["Body"].read())

    return parquet_buffer

def convert_parquet_to_dataframe(parquet_buffer):
    """
    Converts binary Parquet data into a Pandas dataframe.

    Parameters:
        parquet_buffer: BytesIO buffer containing the binary data of the Parquet file

    Returns:
        a Pandas dataframe
    """

    df = pd.read_parquet(parquet_buffer)

    return df

def write_dataframe_to_rds(df, table_name, db_config):
    """
    Writes a pandas DataFrame to a PostgreSQL table.
    """
    logging.info(f"Writing to RDS with config:")
    logging.info(f"Host: {db_config['host']}")
    logging.info(f"Port: {db_config['port']}")
    
    # Split host if it contains port
    host = db_config['host'].split(':')[0] if ':' in db_config['host'] else db_config['host']
    
    db_url = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{host}:{db_config['port']}/{db_config['dbname']}"
    
    logging.info(f"DB URL (without credentials): postgresql+psycopg2://user:***@{host}:{db_config['port']}/{db_config['dbname']}")

    if "id" not in df.columns:
            df = df.reset_index(drop=True)
            df.insert(0, "id", range(1, len(df) + 1))    
    
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="append", index=False)
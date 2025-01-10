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

    Parameters:
        df: The DataFrame to write.
        table_name: Name of the target table in the PostgreSQL database.
        db_config: A dictionary containing database configuration:

    Returns:
        None
    """

    # https://www.learnaws.org/2022/08/30/aws-rds-sqlalchemy/#postgres
    logging.info(f"DB Host: {db_config['host']}")
    logging.info(f"DB Port: {db_config['port']}")
    db_url = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    
    engine = create_engine(db_url)

    # Set index = True to include a new index column    
    df.to_sql(table_name, engine,if_exists="append", index=True)

    return None
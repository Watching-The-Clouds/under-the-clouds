import logging
import urllib.parse
import os
from load_utils import (
    create_s3_client,
    fetch_parquet_from_s3,
    convert_parquet_to_dataframe,
    write_dataframe_to_rds
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

processed_bucket = "watching-the-clouds-processing"

db_config = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"]
}

table_name = "weather_forecasts"

def lambda_handler(event, context):    
    """
    Function loads Parquet binary data into RDS database

    - Create S3 client
    - Collect Parquet data from processed S3 bucket
    - Convert Parquet data to Pandas dataframe
    - Store dataframe in RDS

        Parameters:
            event: JSON-formatted document passed when handler invoked
            context (optional): methods/properties related to handler

        Returns:
            string declaring success or failure
    """

    try:
        file_directory = urllib.parse.unquote_plus(
            event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
        )
    except Exception as e:
        logging.error("Failed to read file_directory: %s", e)
        return "Failed to read file directory."

    try:
        s3_client = create_s3_client()
    except Exception as e:
        logging.error("Failed to create S3 client: %s", e)
        return "Failed to create S3 client."
    
    try:
        parquet_buffer = fetch_parquet_from_s3(s3_client, processed_bucket, file_directory)
    except Exception as e:
        logging.error("Failed to fetch .parquet data from S3: %s", e)
        return "Failed to fetch .parquet data."
    
    try:
        df = convert_parquet_to_dataframe(parquet_buffer)
        logging.info("Successfully converted Parquet to DataFrame")
    except Exception as e:
        logging.error("Failed to convert Parquet to Dataframe: %s", e)
        return "Failed to convert Parquet to Dataframe"

    try:
        write_dataframe_to_rds(df, table_name, db_config)
    except Exception as e:
        logging.error("Failed to store data in RDS: %s", e)
        return "Failed to store data in RDS"

    return "Success!"

if __name__ == "__main__":
    lambda_handler([], [])

from transform_utils import (
    create_s3_client,
    fetch_csv_from_s3,
    convert_csv_to_dataframe,
    generate_new_column,
    drop_and_rename_columns,
    update_wind_direction,
    update_visibility,
    calculate_time_increase,
    calculate_fuel_usage_increase,
    convert_to_parquet,
    store_in_s3,
)
import urllib.parse
import logging

ingested_bucket = "watching-the-clouds-ingestion"
processed_bucket = "watching-the-clouds-processing"


def lambda_handler(event, context):
    """
    Function transforms data in csv format from S3 bucke

    - Create S3 client
    - Collect csv data from ingested S3 bucket
    - Convert csv data to Pandas dataframe
    - Update dataframe: remove unnecessary columns and create new ones
    - Calculate time increase based on weather type (min/max estimates based on % speed change)
    - Calculate cost increase based on weather type (min/max estimates based on % speed change)
    - Convert dataframe to parquet format
    - Store parquet file in processed S3 bucket

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
        csv_data = fetch_csv_from_s3(s3_client, ingested_bucket, file_directory)
    except Exception as e:
        logging.error("Failed to fetch .csv data from S3: %s", e)
        return "Failed to fetch .csv data."

    try:
        df = convert_csv_to_dataframe(csv_data)
        logging.info("Successfully converted CSV to DataFrame")
    except Exception as e:
        logging.error("Failed to convert .csv to dataframe: %s", e)
        return "Failed to convert .csv to dataframe"

    try:
        df_with_precip = generate_new_column(df)
        logging.info("Added precipitation column")
    except Exception as e:
        logging.error("Failed to generate precipitation column: %s", e)
        return "Failed to generate precipitation column"

    try:
        df_dropped = drop_and_rename_columns(df_with_precip)
        logging.info("Dropped and renamed columns")
    except Exception as e:
        logging.error("Failed to drop and rename columns: %s", e)
        return "Failed to drop and rename columns"

    try:
        df_wind = update_wind_direction(df_dropped)
        logging.info("Updated wind direction descriptions")
    except Exception as e:
        logging.error("Failed to update wind directions: %s", e)
        return "Failed to update wind directions"

    try:
        df_visibility = update_visibility(df_wind)
        logging.info("Updated visibility descriptions")
    except Exception as e:
        logging.error("Failed to update visibility descriptions: %s", e)
        return "Failed to update visibility"

    try:
        df_time = calculate_time_increase(df_visibility)
        logging.info("Calculated time increase coefficients")
    except Exception as e:
        logging.error("Failed to calculate time increase: %s", e)
        return "Failed to calculate time increase"

    try:
        ready_basic_endpoint = calculate_fuel_usage_increase(df_time)
        logging.info(f"Calculated fuel usage coefficients.")
    except Exception as e:
        logging.error("Failed to calculate fuel usage: %s", e)
        return "Failed to calculate fuel usage"

    try:
        parquet_body = convert_to_parquet(ready_basic_endpoint)
        logging.info("Successfully converted DataFrame to parquet format")
    except Exception as e:
        logging.error("Failed to convert to parquet format: %s", e)
        return "Failed to convert to parquet format"

    try:
        store_in_s3(s3_client, parquet_body, processed_bucket, file_directory)
    except Exception as e:
        logging.error("Failed to store file in S3: %s", e)
        return "Failed to store file in S3"

    logging.info("Data successfully processed and uploaded!", file_directory)
    print("Success!")
    return "Success!"


if __name__ == "__main__":
    lambda_handler([], [])

import logging
from extract_utils import (
    create_s3_client,
    make_api_get_request,
    flatten_json,
    convert_json_to_csv,
    create_directory_structure_and_file_name,
    store_in_s3
)

data_bucket = "ingested_bucket_name"
code_bucket = "code_bucket_name"

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

def lambda_handler(event, context):
    """
    Function extracts data from OpenWeatherMap '5 Day / 3 Hour Weather Forecast' API Endpoint: https://openweathermap.org/forecast5
     
    - Create S3 client
    - Make API request
    - Convert JSON to .csv format
    - Create file name & directory for storage in S3 bucket
    - Create report for successful / unsuccessful run
    - Store .csv file in S3 bucket

        Parameters:
            event: JSON-formatted document passed when handler invoked
            context (optional): methods/properties related to handler

        Returns: 
            string declaring success or failure
    """

    data = make_api_get_request()

    flattened_data = flatten_json(data)

    converted_data = convert_json_to_csv(flattened_data)

    file_name = create_directory_structure_and_file_name()

    s3_client = create_s3_client()

    store_in_s3(s3_client, converted_data, data_bucket, file_name)

    return "Success!"
import logging
import os
from extract_utils import (
    create_s3_client,
    make_api_get_request,
    format_data,
    convert_to_csv,
    create_directory_structure_and_file_name,
    store_in_s3
)
from dotenv import load_dotenv

load_dotenv()

data_bucket = os.environ.get("INGESTION_BUCKET")
code_bucket = os.environ.get("CODE_BUCKET")

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

def lambda_handler(event, context):
    """
    Function extracts data from OpenWeatherMap '5 Day / 3 Hour Weather Forecast' API Endpoint: https://openweathermap.org/forecast5
     
    - Make API request
    - Format data from nested dict to list of flattened dicts
    - Convert data to .csv format
    - Create file name & directory for storage in S3 bucket
    - Create S3 client
    - Store .csv file in S3 bucket

        Parameters:
            event: JSON-formatted document passed when handler invoked
            context (optional): methods/properties related to handler

        Returns: 
            string declaring success or failure
    """

    try:

        try:
            data = make_api_get_request()
        except Exception as e:
            logging.error("Failed to make API request: %s", e)
            return "Failed to make API request."
        
        try:
            flattened_data = format_data(data)
        except Exception as e:
            logging.error("Failed to flatten JSON: %s", e)
            return "Failed to flatten JSON."

        try:
            converted_data = convert_to_csv(flattened_data)
        except Exception as e:
            logging.error("Failed to convert JSON to CSV: %s", e)
            return "Failed to convert JSON to CSV."
        
        try:
            file_name = create_directory_structure_and_file_name()
        except Exception as e:
            logging.error("Failed to create directory and file name: %s", e)
            return "Failed to create directory and file name."

        try:
            s3_client = create_s3_client()
        except Exception as e:
            logging.error("Failed to create S3 client: %s", e)
            return "Failed to create S3 client."
        
        try:
            store_in_s3(s3_client, converted_data, data_bucket, file_name)
        except Exception as e:
            logging.error("Failed to store file in S3: %s", e)
            return "Failed to store file in S3."
        
        logging.info("Data successfully processed and uploaded!", file_name)
        print("Success!")
        return "Success!"
    
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        return "An unexpected error occurred. Check logs for details."
    
if __name__ == "__main__":
    lambda_handler([],[])
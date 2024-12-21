from transform_utils import create_s3_client, fetch_csv_from_s3, convert_csv_to_dataframe, update_dataframe, convert_to_parquet, store_in_s3
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
        file_directory = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    except Exception as e:
        logging.error("Failed to read file_directory: %s", e)
        return "Failed to read file directory."

    try:     
        s3_client = create_s3_client()
    except Exception as e:
        logging.error("Failed to create S3 client: %s", e)
        return "Failed to create S3 client."
    
    try:    
        csv_data = fetch_csv_from_s3(s3_client,ingested_bucket,file_directory)
    except Exception as e:
        logging.error("Failed to fetch .csv data from S3: %s", e)
        return "Failed to fetch .csv data."
    
    try:
        df = convert_csv_to_dataframe(csv_data)
    except Exception as e:
        logging.error("Failed to convert .csv to dataframe: %s", e)
        return "Failed to convert .csv to dataframe"
    
    try:
        ready_basic_endpoint = update_dataframe(df)
    except Exception as e:
        logging.error("Failed to create endpoint dataframe: %s", e)
        return "Failed to create endpoint dataframe"
    
    try:
        parquet_body = convert_to_parquet(ready_basic_endpoint)
    except Exception as e:
        logging.error("Failed to convert to parquet format: %s", e)
        return "Failed to convert to parquet format"

    try:
        store_in_s3(s3_client,parquet_body,processed_bucket,file_directory)
    except Exception as e:
        logging.error("Failed to store file in S3: %s", e)
        return "Failed to store file in S3"

    logging.info("Data successfully processed and uploaded!", file_directory)
    print("Success!")
    return "Success!"
    
if __name__ == "__main__":
    lambda_handler([],[])
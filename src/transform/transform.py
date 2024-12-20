from transform_utils import create_s3_client, fetch_csv_from_s3, convert_csv_to_dataframe, update_dataframe, convert_to_parquet, store_in_s3
import urllib.parse

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

    ingested_bucket = "watching-the-clouds-ingestion"
    processed_bucket = "watching-the-clouds-processing"
    file_directory = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    s3_client = create_s3_client()

    csv_data = fetch_csv_from_s3(s3_client,ingested_bucket,file_directory)

    df = convert_csv_to_dataframe(csv_data)

    ready_basic_endpoint = update_dataframe(df)

    parquet_body = convert_to_parquet(ready_basic_endpoint)

    store_in_s3(s3_client,parquet_body,processed_bucket,file_directory)

    return "Success!"
from transform_utils import create_s3_client, fetch_csv_from_s3, convert_csv_to_dataframe, update_dataframe

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

    create_s3_client()

    fetch_csv_from_s3()

    convert_csv_to_dataframe()

    update_dataframe()

    return "Success!"
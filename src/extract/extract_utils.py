from pprint import pprint
from datetime import datetime
import boto3
import requests
import os
import csv
import io

# from dotenv import load_dotenv
# load_dotenv()

def make_api_get_request():
    """
    Makes API get request to OpenWeatherMap API.

    Returns:
        JSON object
    """

    api_key = os.environ.get('API_KEY')
    endpoint_url = "api.openweathermap.org/data/2.5/weather"
    location = "London"

    response = requests.get(f'https://{endpoint_url}?q={location}&units=metric&appid={api_key}')

    data = response.json()

    return data

def flatten_json(data):
    """
    Function uses recursion to take a JSON object and flatten it to create key:value pairs that can later be used for column titles.
    
    Parameters:
        raw data from API endpoint

    Returns:
        flattened data from API endpoint
    """

    flattened_data = {}

    # 'x' represents object passed to flatten - initially the entire JSON string, but on subsequent calls can be a dict, a list, or a primitive value (base case)

    def flatten(x, name=''):

        if isinstance(x, dict):
            for key in x:
                flatten(x[key], name + key + '.')

        elif isinstance(x, list):
            for _, item in enumerate(x):
                flatten(item, name)

        else:
            flattened_data[name[:-1]] = x

    flatten(data)

    return flattened_data

def convert_json_to_csv(flattened_data):
    """
    Takes a flattened data structure and converts it into .csv format.

    Parameters:
        raw data from API endpoint in JSON format

    Returns:
        .csv file
    """

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(flattened_data.keys())
    writer.writerow(flattened_data.values())

    converted_data = output.getvalue()

    output.close()

    return converted_data

def create_directory_structure_and_file_name():
    """
    Produces directory structure and file name for storage in S3 bucket.

    Returns:
        string representing directory structure and file name in format "YYYY/MM/DD/00:00.00/GB/London.csv"
    """

    date_time_now = datetime.today().isoformat(timespec="seconds")

    year = date_time_now[0:4]
    month = date_time_now[5:7]
    day = date_time_now[8:10]
    time = date_time_now[11:]

    file_name = f"{year}/{month}/{day}/{time}/GB/London.csv"

    return file_name

def create_s3_client():
    """
    Creates an S3 client using boto3.

    Returns:
        An S3 client
    """

    return boto3.client("s3")

def store_in_s3(s3_client, converted_data, bucket_name, file_name):
    """
    Uploads .csv file to a named AWS S3 bucket.

    Parameters:
        s3_client: boto3 S3 client
        csv_output: endpoint data in flattened .csv format
     put_object   bucket_name (str): S3 bucket name
        file_name (str): S3 file directory and file name
    """
    
    s3_client.put_object(Body=converted_data, Bucket=bucket_name, Key=file_name)
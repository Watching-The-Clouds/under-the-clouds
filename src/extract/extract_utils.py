from pprint import pprint
from datetime import datetime
import boto3
import requests
import os
import csv
import io

# from dotenv import load_dotenv
# load_dotenv()

def create_s3_client():
    """
    Creates an S3 client using boto3.

    Returns:
        An S3 client
    """

    return boto3.client("s3")

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

    flattened_data = flatten_json(data)

    return flattened_data

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

    csv_output = output.getvalue()

    output.close()

    return csv_output

def create_directory_structure_and_file_name():
    """
    Produces directory structure and file 
    Parameters:
        raw data from API endpoint in JSON format

    Returns:
        .csv file
    """

    date_time_now = datetime.today().isoformat(timespec="seconds")

    year = date_time_now[0:4]
    month = date_time_now[5:7]
    day = date_time_now[8:10]
    time = date_time_now[11:]

    file_name = f"{year}/{month}/{day}/{time}/GB/London.csv"

    return file_name

# make_api_get_request()
# flatten_json(make_api_get_request())
# convert_json_to_csv(flatten_json())
# create_directory_structure_and_file_name()
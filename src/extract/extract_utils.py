from pprint import pprint
from datetime import datetime
import boto3
import requests
import os
import csv
import io

from dotenv import load_dotenv
load_dotenv()

def make_api_get_request():
    """
    Makes API get request to OpenWeatherMap API.

    Returns:
        JSON object
    """

    api_key = os.environ.get('API_KEY')
    endpoint_url = "api.openweathermap.org/data/2.5/forecast"
    location = "London"

    response = requests.get(f'https://{endpoint_url}?q={location}&units=metric&appid={api_key}')

    data = response.json()

    # pprint(data)

    return data

def flatten(x, name=''):
    """
    Parameters:
        x: represents object passed to flatten - initially the entire JSON string, but on subsequent calls can be a dict, a list, or a primitive value (base case)
        name: name of object passed into function

    Returns:
        flattened dictionary
    """
    flattened_list = []
    
    if isinstance(x, dict):  # Process dictionaries
        for key, value in x.items():
            new_key = f"{name}.{key}" if name else key
            flattened_list.extend(flatten(value, new_key).items())
    
    elif isinstance(x, list):  # Process lists
        for i, value in enumerate(x):
            new_key = f"{name}.{i}" if name else str(i)
            flattened_list.extend(flatten(value, new_key).items())
    
    else:  
        flattened_list.append((name, x))
    
    return dict(flattened_list)

def flatten_json(data):
    """
    Function uses recursion to take a JSON object and flatten it to create key:value pairs that can later be used for column titles.
    
    Parameters:
        raw data from API endpoint

    Returns:
        flattened data from API endpoint
    """

    flattened_data = []

    for x in data["list"]:

        city_dict = flatten(data["city"])
        forecast_dict = flatten(x)

        flatten_dict = city_dict|forecast_dict

        flattened_data.append(flatten_dict)
    

    return flattened_data

def convert_json_to_csv(flattened_data):
    """
    Takes a flattened data structure and converts it into .csv format.

    Parameters:
        flattened data from API endpoint in JSON format

    Returns:
        .csv file
    """

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(flattened_data.keys())
    writer.writerow(flattened_data.values())

    converted_data = output.getvalue()

    output.close()

    print(converted_data)

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

    file_name = f"GB/London/{year}/{month}/{day}/{time}.csv"

    print(file_name)
    
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
        bucket_name (str): S3 bucket name
        file_name (str): S3 file directory and file name
    """
    
    s3_client.put_object(Body=converted_data, Bucket=bucket_name, Key=file_name)

pprint(flatten_json(make_api_get_request()))
from pprint import pprint
import boto3
import requests
import os

api_key = os.environ.get('API_KEY')

def create_s3_client():
    """
    Creates an S3 client using boto3
    """

    return boto3.client("s3")

def make_api_get_request():
    """
    Creates an S3 client using boto3
    """
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}')

    data = response.json()

    pprint(data)

    print(type(data))

    # for key in data:
    #     print(key, ":", data[key])

make_api_get_request()
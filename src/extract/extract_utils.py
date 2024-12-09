from pprint import pprint
import boto3
import requests

API_KEY = "3db59dd5504605020ae6021efd52b288"

def create_s3_client():
    """
    Creates an S3 client using boto3
    """

    return boto3.client("s3")


def make_api_get_request():
    """
    Creates an S3 client using boto3
    """
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=London&appid=3db59dd5504605020ae6021efd52b288')

    data = response.json()

    pprint(data)

    # for key in data:
    #     print(key, ":", data[key])

make_api_get_request()
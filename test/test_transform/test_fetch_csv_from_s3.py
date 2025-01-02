from transform_utils import fetch_csv_from_s3
from moto import mock_aws
from unittest.mock import patch
import pytest
import boto3

@mock_aws
def test_fetch_csv_from_s3():

    # Mocked S3 client and file set up
    test_s3_client = boto3.client("s3", region_name = "eu-west-2")
    test_bucket = "test_bucket"
    test_file_directory = "test_data/sample.csv"
    test_csv_content = "clouds,coord,country\n99,[0,0],IT\n100,[1,1],UK"

    # Create mock S3 and put test data
    test_s3_client.create_bucket(Bucket=test_bucket,CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
    test_s3_client.put_object(Bucket=test_bucket, Key=test_file_directory, Body=test_csv_content)

    # Invoke fetch_csv to get test_csv_content
    result = fetch_csv_from_s3(test_s3_client, test_bucket,test_file_directory)

    assert result == test_csv_content


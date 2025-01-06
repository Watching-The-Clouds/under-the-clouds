from extract_utils import store_in_s3
from moto import mock_aws
from io import StringIO
import boto3
from botocore.exceptions import ClientError
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def s3_client():
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        s3.create_bucket(
            Bucket="test-bucket",
            # defaults to us-east-1, need to set LocationConstraint
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        yield s3


def test_store_in_s3_success(s3_client):
    bucket_name = "test-bucket"
    file_name = "test-data/test.csv"
    converted_data = "id,name\n2643743,London"

    store_in_s3(s3_client, converted_data, bucket_name, file_name)

    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)

    # Need to decode from bytes to string as response['Body'].read() returns contents as bytes
    assert response["Body"].read().decode() == converted_data


def test_store_in_s3_failure_invalid_bucket(s3_client):
    bucket_name = "nonexistent-bucket"
    file_name = "test-data/test.csv"
    converted_data = "id,name\n2643743,London"

    with pytest.raises(s3_client.exceptions.NoSuchBucket):
        store_in_s3(s3_client, converted_data, bucket_name, file_name)

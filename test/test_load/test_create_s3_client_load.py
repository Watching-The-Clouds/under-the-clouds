from load_utils import create_s3_client
from moto import mock_aws
from unittest.mock import patch
from botocore.exceptions import NoCredentialsError
import pytest
import boto3

@mock_aws
def test_create_s3_client_success():
    s3_client = create_s3_client()

    assert hasattr(s3_client, "list_buckets")


@patch("load_utils.boto3.client")
def test_create_s3_no_credentials(mock_boto_client):
    mock_boto_client.side_effect = NoCredentialsError()

    with pytest.raises(NoCredentialsError):
        create_s3_client()

@patch("load_utils.boto3.client")
def test_create_s3_client_calls_boto3_with_s3(mock_boto_client):
    mock_s3_client = mock_boto_client.return_value 

    s3_client = create_s3_client()

    assert s3_client is mock_s3_client
    mock_boto_client.assert_called_once_with("s3")
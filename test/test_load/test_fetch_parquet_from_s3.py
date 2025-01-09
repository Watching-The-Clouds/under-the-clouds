from load_utils import fetch_parquet_from_s3
from moto import mock_aws
from unittest.mock import patch
from botocore.exceptions import NoCredentialsError
import pytest
from io import BytesIO
from unittest.mock import MagicMock

def test_fetch_parquet_from_s3():

    mock_s3_client = MagicMock()

    dummy_parquet_data = b"dummy_parquet_data"
    mock_s3_client.get_object.return_value = {
        "Body": BytesIO(dummy_parquet_data)
    }

    processed_bucket = "test-bucket"
    file_directory = "test-directory/file.parquet"

    result = fetch_parquet_from_s3(mock_s3_client, processed_bucket, file_directory)

    assert isinstance(result, BytesIO)
    assert result.read() == dummy_parquet_data

    mock_s3_client.get_object.assert_called_once_with(
        Bucket=processed_bucket,
        Key=file_directory
    )
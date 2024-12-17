import pytest
from unittest.mock import patch, MagicMock
import os
import extract
from extract import lambda_handler
import logging
from importlib import reload


@patch("extract.make_api_get_request", side_effect=Exception("API error"))
def test_make_api_get_request_failure(mock_make_api_request, caplog):
    
    with caplog.at_level(logging.ERROR):
        response = lambda_handler({}, {})
    
    assert response == "Failed to make API request."
    assert "Failed to make API request: API error" in caplog.text


@patch("extract.format_data", side_effect=Exception("Formatting error"))
def test_format_data_failure(mock_format_data, caplog):
    
    with patch("extract.make_api_get_request") as mock_make_api_request:
        mock_make_api_request.return_value = {"mock": "data"}

    
    with caplog.at_level(logging.ERROR):
        response = lambda_handler({}, {})
    
    assert response == "Failed to flatten JSON."
    assert "Failed to flatten JSON: Formatting error" in caplog.text


@patch("extract.convert_to_csv", side_effect=Exception("Conversion error"))
def test_convert_to_csv_failure(mock_convert_to_csv, caplog):
    # Arrange
    with patch("extract.make_api_get_request") as mock_make_api_request, \
         patch("extract.format_data") as mock_format_data, \
         caplog.at_level(logging.ERROR):
        
        mock_make_api_request.return_value = {"mock": "data"}
        mock_format_data.return_value = [{"key": "value"}]

        response = lambda_handler({}, {})
    
    assert response == "Failed to convert JSON to CSV."
    assert "Failed to convert JSON to CSV: Conversion error" in caplog.text


@patch("extract.create_directory_structure_and_file_name", side_effect=Exception("File name error"))
def test_create_file_name_failure(mock_create_file_name, caplog):
    # Combine all context managers into a single with statement
    with patch("extract.make_api_get_request") as mock_make_api_request, \
         patch("extract.format_data") as mock_format_data, \
         patch("extract.convert_to_csv") as mock_convert_to_csv, \
         caplog.at_level(logging.ERROR):
        
        mock_make_api_request.return_value = {"mock": "data"}
        mock_format_data.return_value = [{"key": "value"}]
        mock_convert_to_csv.return_value = "csv_data"

        response = lambda_handler({}, {})
    
    assert response == "Failed to create directory and file name."
    assert "Failed to create directory and file name: File name error" in caplog.text


@patch("extract.create_s3_client", side_effect=Exception("S3 client error"))
def test_create_s3_client_failure(mock_create_s3_client, caplog):

    with patch("extract.make_api_get_request") as mock_make_api_request, \
         patch("extract.format_data") as mock_format_data, \
         patch("extract.convert_to_csv") as mock_convert_to_csv, \
         patch("extract.create_directory_structure_and_file_name") as mock_create_file_name:
        mock_make_api_request.return_value = {"mock": "data"}
        mock_format_data.return_value = [{"key": "value"}]
        mock_convert_to_csv.return_value = "csv_data"
        mock_create_file_name.return_value = "GB/London/2024/12/11/mock.csv"

    with caplog.at_level(logging.ERROR):
        response = lambda_handler({}, {})
    
    assert response == "Failed to create S3 client."
    assert "Failed to create S3 client: S3 client error" in caplog.text


@patch("extract.store_in_s3", side_effect=Exception("S3 storage error"))
def test_store_in_s3_failure(mock_store_in_s3, caplog):
    
    with patch("extract.make_api_get_request") as mock_make_api_request, \
         patch("extract.format_data") as mock_format_data, \
         patch("extract.convert_to_csv") as mock_convert_to_csv, \
         patch("extract.create_directory_structure_and_file_name") as mock_create_file_name, \
         patch("extract.create_s3_client") as mock_create_s3_client:
        mock_make_api_request.return_value = {"mock": "data"}
        mock_format_data.return_value = [{"key": "value"}]
        mock_convert_to_csv.return_value = "csv_data"
        mock_create_file_name.return_value = "GB/London/2024/12/11/mock.csv"
        mock_create_s3_client.return_value = MagicMock()

    with caplog.at_level(logging.ERROR):
        response = lambda_handler({}, {})
    
    assert response == "Failed to store file in S3."
    assert "Failed to store file in S3: S3 storage error" in caplog.text


os.environ["INGESTION_BUCKET"] = "mock-data-bucket"
os.environ["CODE_BUCKET"] = "mock-code-bucket"


def test_lambda_handler_success():
    reload(extract)
    
    with patch('extract.make_api_get_request') as mock_api_request, \
         patch('extract.format_data') as mock_format_data, \
         patch('extract.convert_to_csv') as mock_convert_to_csv, \
         patch('extract.create_directory_structure_and_file_name') as mock_create_file, \
         patch('extract.create_s3_client') as mock_s3_client, \
         patch('extract.store_in_s3', return_value=None) as mock_store_in_s3, \
         patch.dict('os.environ', {'INGESTION_BUCKET': 'mock-data-bucket'}):

            mock_api_request.return_value = {"list": [{"city": "London", "temp": 20}]}
            mock_format_data.return_value = [{"city": "London", "temp": 20}]
            mock_convert_to_csv.return_value = "city,temp\nLondon,20"
            mock_create_file.return_value = "GB/London/2024/12/11/10:30.00.csv"

            mock_s3 = MagicMock()
            mock_s3_client.return_value = mock_s3

            response = lambda_handler([], [])
            print(f"store_in_s3 called: {mock_store_in_s3.call_count}")
            assert response == "Success!"
            
            mock_store_in_s3.assert_called_once_with(
                mock_s3, "city,temp\nLondon,20", "mock-data-bucket", "GB/London/2024/12/11/10:30.00.csv"
            )

            mock_s3_client.assert_called_once()


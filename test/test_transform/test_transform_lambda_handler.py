import unittest
from unittest.mock import patch, MagicMock
from transform import lambda_handler
import logging

class TestLambdaHandler(unittest.TestCase):
    @patch("transform.create_s3_client")
    @patch("transform.fetch_csv_from_s3")
    @patch("transform.convert_csv_to_dataframe")
    @patch("transform.generate_new_column")
    @patch("transform.drop_and_rename_columns")
    @patch("transform.update_wind_direction")
    @patch("transform.update_visibility")
    @patch("transform.calculate_time_increase")
    @patch("transform.calculate_fuel_usage_increase")
    @patch("transform.convert_to_parquet")
    @patch("transform.store_in_s3")
    def test_lambda_handler_success(
        self,
        mock_store_in_s3,
        mock_convert_to_parquet,
        mock_calculate_fuel_usage_increase,
        mock_calculate_time_increase,
        mock_update_visibility,
        mock_update_wind_direction,
        mock_drop_and_rename_columns,
        mock_generate_new_column,
        mock_convert_csv_to_dataframe,
        mock_fetch_csv_from_s3,
        mock_create_s3_client,
    ):
        # Arrange
        event = {
            "Records": [
                {
                    "s3": {
                        "object": {
                            "key": "test_file.csv"
                        }
                    }
                }
            ]
        }

        # Mock behaviors
        mock_create_s3_client.return_value = MagicMock()
        mock_fetch_csv_from_s3.return_value = "mock_csv_data"
        mock_convert_csv_to_dataframe.return_value = MagicMock()
        mock_generate_new_column.return_value = MagicMock()
        mock_drop_and_rename_columns.return_value = MagicMock()
        mock_update_wind_direction.return_value = MagicMock()
        mock_update_visibility.return_value = MagicMock()
        mock_calculate_time_increase.return_value = MagicMock()
        mock_calculate_fuel_usage_increase.return_value = MagicMock()
        mock_convert_to_parquet.return_value = b"mock_parquet_data"
        mock_store_in_s3.return_value = None

        # Act
        result = lambda_handler(event, {})

        # Assert
        self.assertEqual(result, "Success!")
        mock_create_s3_client.assert_called_once()
        mock_fetch_csv_from_s3.assert_called_once()
        mock_convert_csv_to_dataframe.assert_called_once()
        mock_generate_new_column.assert_called_once()
        mock_drop_and_rename_columns.assert_called_once()
        mock_update_wind_direction.assert_called_once()
        mock_update_visibility.assert_called_once()
        mock_calculate_time_increase.assert_called_once()
        mock_calculate_fuel_usage_increase.assert_called_once()
        mock_convert_to_parquet.assert_called_once()
        mock_store_in_s3.assert_called_once()

@patch("urllib.parse.unquote_plus", side_effect=Exception("Decoding error"))
def test_file_directory_extraction_failure(mock_unquote, caplog):

    event = {"Records": [{"s3": {"object": {"key": "test_file.csv"}}}]}

    with caplog.at_level(logging.ERROR):
        response = lambda_handler(event, {})

    assert response == "Failed to read file directory."
    assert "Failed to read file_directory: Decoding error" in caplog.text

@patch("transform.create_s3_client", side_effect=Exception("S3 client error"))
def test_create_s3_client_failure(mock_create_s3_client, caplog):
    
    event = {"Records": [{"s3": {"object": {"key": "test_file.csv"}}}]}

    with caplog.at_level(logging.ERROR):  
        response = lambda_handler(event, {})

    assert response == "Failed to create S3 client."
    assert "Failed to create S3 client: S3 client error" in caplog.text

@patch("transform.convert_csv_to_dataframe", side_effect=Exception("DataFrame conversion error"))
def test_convert_csv_to_dataframe_failure(mock_convert_csv_to_dataframe, caplog):

    event = {"Records": [{"s3": {"object": {"key": "test_file.csv"}}}]}

    with patch("transform.fetch_csv_from_s3", return_value="mock_csv_data"):
        with caplog.at_level(logging.ERROR):  
            response = lambda_handler(event, {})

    assert response == "Failed to convert .csv to dataframe"
    assert "Failed to convert .csv to dataframe: DataFrame conversion error" in caplog.text

@patch("transform.generate_new_column", side_effect=Exception("Generate new column error"))
def test_generate_new_column_failure(mock_generate_new_column, caplog):

    event = {"Records": [{"s3": {"object": {"key": "test_file.csv"}}}]}

    with patch("transform.fetch_csv_from_s3", return_value="mock_csv_data"), \
         patch("transform.convert_csv_to_dataframe", return_value="mock_dataframe"):
        
        with caplog.at_level(logging.ERROR):
            response = lambda_handler(event, {})

    assert response == "Failed to generate precipitation column"
    assert "Failed to generate precipitation column: Generate new column error" in caplog.text

@patch("transform.drop_and_rename_columns", side_effect=Exception("Drop and rename columns error"))
def test_drop_and_rename_columns_failure(mock_drop_and_rename_columns, caplog):

    event = {"Records": [{"s3": {"object": {"key": "test_file.csv"}}}]}

    with patch("transform.fetch_csv_from_s3", return_value="mock_csv_data"), \
         patch("transform.convert_csv_to_dataframe", return_value="mock_dataframe"), \
         patch("transform.generate_new_column", return_value="mock_dataframe_with_precip"):
        
        with caplog.at_level(logging.ERROR):
            response = lambda_handler(event, {})

    assert response == "Failed to drop and rename columns"
    assert "Failed to drop and rename columns: Drop and rename columns error" in caplog.text

@patch("transform.update_wind_direction", side_effect=Exception("Update wind direction error"))
def test_update_wind_direction_failure(mock_update_wind_direction, caplog):

    event = {"Records": [{"s3": {"object": {"key": "test_file.csv"}}}]}

    with patch("transform.fetch_csv_from_s3", return_value="mock_csv_data"), \
         patch("transform.convert_csv_to_dataframe", return_value="mock_dataframe"), \
         patch("transform.generate_new_column", return_value="mock_dataframe_with_precip"), \
         patch("transform.drop_and_rename_columns", return_value="mock_dataframe_dropped"):
        
        with caplog.at_level(logging.ERROR):
            response = lambda_handler(event, {})

    assert response == "Failed to update wind directions"
    assert "Failed to update wind directions: Update wind direction error" in caplog.text

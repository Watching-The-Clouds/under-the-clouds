from transform_utils import fetch_csv_from_s3
import unittest
from unittest.mock import MagicMock, patch

class TestFetchCsvFromS3(unittest.TestCase):
    def setUp(self):
        self.mock_s3_client = MagicMock()
        self.data_bucket = "test-bucket"
        self.valid_key = "valid.csv"
        self.invalid_key = "invalid.csv"

    def test_fetch_csv_success(self):
        mock_csv_data = "id,name\n1,Brad\n2,Irina\n3,Liam"
        self.mock_s3_client.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=mock_csv_data.encode('utf-8')))
        }

        result = fetch_csv_from_s3(self.mock_s3_client, self.data_bucket, self.valid_key)
        
        self.assertEqual(result, mock_csv_data)
        self.mock_s3_client.get_object.assert_called_once_with(
            Bucket=self.data_bucket, Key=self.valid_key
        )

    def test_fetch_csv_key_not_found(self):
        self.mock_s3_client.get_object.side_effect = Exception("Key not found")
        result = fetch_csv_from_s3(self.mock_s3_client, self.data_bucket, self.invalid_key)
        
        self.assertIsNone(result)
        self.mock_s3_client.get_object.assert_called_once_with(
            Bucket=self.data_bucket, Key=self.invalid_key
        )

    def test_fetch_csv_decode_error(self):
        self.mock_s3_client.get_object.return_value = {
            "Body": MagicMock(read=MagicMock(return_value=b"\x80\x81"))
        }

        result = fetch_csv_from_s3(self.mock_s3_client, self.data_bucket, self.valid_key)
        
        self.assertIsNone(result)
        self.mock_s3_client.get_object.assert_called_once_with(
            Bucket=self.data_bucket, Key=self.valid_key
        )

    def test_fetch_csv_general_error(self):
        self.mock_s3_client.get_object.side_effect = Exception("Something went wrong")

        result = fetch_csv_from_s3(self.mock_s3_client, self.data_bucket, self.valid_key)
        
        self.assertIsNone(result)
        self.mock_s3_client.get_object.assert_called_once_with(
            Bucket=self.data_bucket, Key=self.valid_key
        )
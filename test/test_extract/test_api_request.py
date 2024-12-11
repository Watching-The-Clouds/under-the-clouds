from extract_utils import make_api_get_request
import os
import pytest
from unittest.mock import patch, Mock

class TestGetApiRequest:

    def test_make_api_get_request_return_type(self):
        """Test that the function returns a dictionary."""
        mock_api_key = "test_key"
        mock_response_data = {"weather": "sunny"}  
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data

        with patch.dict(os.environ, {"API_KEY": mock_api_key}):
            with patch("requests.get", return_value=mock_response):
                data = make_api_get_request()
                assert isinstance(data, dict) 

    def test_make_api_get_request_reads_api_key(self):
        """Test that the function correctly reads the API key from the environment."""
        mock_api_key = "test_key"
        with patch.dict(os.environ, {"API_KEY": mock_api_key}):
            with patch("requests.get") as mock_get:
                make_api_get_request()
                mock_get.assert_called_once()
                assert "appid=test_key" in mock_get.call_args[0][0] 


    def test_make_api_get_request_success(self):
        """Test that the function successfully returns the API response."""
        mock_api_key = "test_key"
        mock_response_data = {"weather": "sunny"}
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data

        with patch.dict(os.environ, {"API_KEY": mock_api_key}):
            with patch("requests.get", return_value=mock_response) as mock_get:
                data = make_api_get_request()
                assert data == mock_response_data
                mock_get.assert_called_once_with(
                    "https://api.openweathermap.org/data/2.5/forecast"
                    "?q=London&units=metric&appid=test_key"
                )


     

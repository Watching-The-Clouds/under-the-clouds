import pytest
from unittest.mock import patch
from datetime import datetime
from extract_utils import create_directory_structure_and_file_name


@pytest.mark.parametrize(
    "mock_datetime, expected_file_name",
    [
        (datetime(2024, 12, 11, 15, 30, 45), "GB/London/2024/12/11/15:30:45.csv"),
        (datetime(2023, 6, 20, 10, 5, 30), "GB/London/2023/06/20/10:05:30.csv"),
        (datetime(2024, 1, 2, 1, 3, 4), "GB/London/2024/01/02/01:03:04.csv"),
    ],
)
def test_create_directory_structure_and_file_name(mock_datetime, expected_file_name):
    """Tests the function generates the correct file name for various dates and times."""
    with patch("extract_utils.datetime") as mock_datetime_module:
        mock_datetime_module.today.return_value = mock_datetime

        result = create_directory_structure_and_file_name()
        assert result == expected_file_name

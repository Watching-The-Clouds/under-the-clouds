import io
import csv
import pytest
from extract_utils import convert_to_csv


def test_convert_to_csv_basic_functionality():
    """Test that the function correctly converts a list of dictionaries to CSV."""
    sample_data = [
        {"temperature": 20, "humidity": 50},
        {"temperature": 25, "humidity": 60},
    ]
    expected_csv = (
        "humidity,rain.3h,snow.3h,temperature\r\n" "50,0,0,20\r\n" "60,0,0,25\r\n"
    )

    result = convert_to_csv(sample_data)
    assert result == expected_csv

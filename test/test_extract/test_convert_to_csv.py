import io
import csv
import pytest
from src.extract.extract_utils import convert_to_csv 

def test_convert_to_csv_basic_functionality():
    """Test that the function correctly converts a list of dictionaries to CSV."""
    sample_data = [
        {"temperature": 20, "humidity": 50},
        {"temperature": 25, "humidity": 60},
    ]
    expected_csv = (
        "temperature,humidity\r\n"
        "20,50\r\n"
        "25,60\r\n"
    )

    result = convert_to_csv(sample_data)
    assert result == expected_csv
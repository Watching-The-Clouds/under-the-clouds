from transform_utils import convert_csv_to_dataframe
import pytest   
import pandas as pd

def test_convert_csv_to_dataframe_valid_data():
    csv_data = "main.temp,main.feels_like,main.temp_min,main.temp_max\n1,1,1,1\n2,2,2,2"

    expected_data = pd.DataFrame({
        "main.temp": [1, 2],
        "main.feels_like": [1, 2],
        "main.temp_min": [1, 2],
        "main.temp_max": [1, 2]
    })

    result = convert_csv_to_dataframe(csv_data)

    pd.testing.assert_frame_equal(result, expected_data)

def test_convert_csv_to_dataframe_empty_data():
    csv_data = ""
    result = convert_csv_to_dataframe(csv_data)
    assert result == None
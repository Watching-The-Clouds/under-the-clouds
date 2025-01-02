from transform_utils import convert_csv_to_dataframe
import pandas as pd
import pytest

def test_convert_csv_to_dataframe():

    test_csv_content = "clouds,lat,lon,country\n100,1.1, 1.2,IT\n100,1.3,1.4,UK"

    expected_output = pd.DataFrame({
        "clouds": [100, 100],
        "lat": [1.1,1.3],
        "lon": [1.2,1.4],
        "country": ["IT", "UK"]
    })   

    result = convert_csv_to_dataframe(test_csv_content)

    pd.testing.assert_frame_equal(result, expected_output)
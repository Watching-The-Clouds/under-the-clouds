from transform_utils import update_visibility
import pandas as pd
from unittest.mock import patch
import pytest

@patch("transform_utils.update_visibility")
def test_update_wind_direction(mock_get_visibility_description):

    mock_get_visibility_description.return_value = "low"

    test_input = pd.DataFrame({
        "city": ["a"],
        "date_time": ["b"],
        "temp_max": [1],
        "temp_min": [2],
        "feels_like": [3],
        "weather_description": ["cloudy"],
        "weather_id": [500],
        "wind_direction": ["North"],
        "wind_speed": [100],
        "visibility": [0],
        "precipitation": [5]
    })

    expected_output = pd.DataFrame({
        "city": ["a"],
        "date_time": ["b"],
        "temp_max": [1],
        "temp_min": [2],
        "feels_like": [3],
        "weather_description": ["cloudy"],
        "weather_id": [500],
        "wind_direction": ["North"],
        "wind_speed": [100],
        "visibility": [0],
        "precipitation": [5],
        "visibility_description": ["low"]
    })    

    result = update_visibility(test_input)

    pd.testing.assert_frame_equal(result, expected_output)

def test_original_dataframe_unchanged():
    test_input = pd.DataFrame({
        "visibility": [0]
    })

    original_input = test_input.copy()

    _ = update_visibility(test_input)

    pd.testing.assert_frame_equal(test_input, original_input)
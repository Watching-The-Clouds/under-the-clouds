from transform_utils import update_wind_direction
import pandas as pd
from unittest.mock import patch
import pytest

@patch("transform_utils.update_wind_direction")
def test_update_wind_direction(mock_get_direction):

    mock_get_direction.return_value = "North"

    test_input = pd.DataFrame({
        "city": ["a"],
        "date_time": ["b"],
        "temp_max": [1],
        "temp_min": [2],
        "feels_like": [3],
        "weather_description": ["cloudy"],
        "weather_id": [500],
        "wind_direction": [360],
        "wind_speed": [100],
        "visibility": [100],
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
        "visibility": [100],
        "precipitation": [5]
    })    

    result = update_wind_direction(test_input)

    pd.testing.assert_frame_equal(result, expected_output)

def test_original_dataframe_unchanged():
    test_input = pd.DataFrame({
        "wind_direction": [360]
    })

    original_input = test_input.copy()

    _ = update_wind_direction(test_input)

    pd.testing.assert_frame_equal(test_input, original_input)
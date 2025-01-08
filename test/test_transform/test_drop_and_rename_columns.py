from transform_utils import drop_and_rename_columns
import pandas as pd
import pytest

def test_renames_columns():

    test_input = pd.DataFrame({
        "name": ["a"],
        "dt_txt": ["b"],
        "main.temp_max": [1],
        "main.temp_min": [2],
        "main.feels_like": [3],
        "weather.0.description": ["cloudy"],
        "weather.0.id": [500],
        "wind.deg": [360],
        "wind.speed": [100],
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
        "wind_direction": [360],
        "wind_speed": [100],
        "visibility": [100],
        "precipitation": [5]
    })   

    result = drop_and_rename_columns(test_input)

    pd.testing.assert_frame_equal(result, expected_output)

def test_drops_columns():

    test_input = pd.DataFrame({
        "name": ["a"],
        "dt_txt": ["b"],
        "main.temp_max": [1],
        "main.temp_min": [2],
        "main.feels_like": [3],
        "weather.0.description": ["cloudy"],
        "weather.0.id": [500],
        "wind.deg": [360],
        "wind.speed": [100],
        "visibility": [100],
        "precipitation": [5],
        "column_to_drop": ["DROP ME!!!"]
    })

    expected_output = pd.DataFrame({
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

    result = drop_and_rename_columns(test_input)

    pd.testing.assert_frame_equal(result, expected_output)

def test_original_dataframe_unchanged():

    test_input = pd.DataFrame({
        "name": ["a"],
        "dt_txt": ["b"],
        "main.temp_max": [1],
        "main.temp_min": [2],
        "main.feels_like": [3],
        "weather.0.description": ["cloudy"],
        "weather.0.id": [500],
        "wind.deg": [360],
        "wind.speed": [100],
        "visibility": [100],
        "precipitation": [5]
    })

    original_input = test_input.copy()

    _ = drop_and_rename_columns(test_input)

    pd.testing.assert_frame_equal(test_input, original_input)
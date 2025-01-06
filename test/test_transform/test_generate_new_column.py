from transform_utils import generate_new_column
import pandas as pd
import pytest

def test_creates_new_column():

    test_input = pd.DataFrame({
        "rain.3h": [1],
        "snow.3h": [2]
    })

    expected_output = pd.DataFrame({
        "rain.3h": [1],
        "snow.3h": [2],
        "precipitation": [3]
    })   

    result = generate_new_column(test_input)

    pd.testing.assert_frame_equal(result, expected_output)

def test_other_columns_preserved():

    test_input = pd.DataFrame({
        "rain.3h": [1],
        "snow.3h": [2],
        "temperature": [3]
    })

    expected_output = pd.DataFrame({
        "rain.3h": [1],
        "snow.3h": [2],
        "temperature": [3],
        "precipitation": [3]
    })   

    result = generate_new_column(test_input)

    pd.testing.assert_frame_equal(result, expected_output)

def test_original_dataframe_unchanged():
    test_input = pd.DataFrame({
        "rain.3h": [1],
        "snow.3h": [2]
    })

    original_input = test_input.copy()

    _ = generate_new_column(test_input)

    pd.testing.assert_frame_equal(test_input, original_input)
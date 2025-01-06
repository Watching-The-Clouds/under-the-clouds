from transform_utils import get_visibility_description
import pytest

def test_returns_string():

    test_input = 0

    result = get_visibility_description(test_input)

    assert type(result) == str

def test_returns_correct_string():

    test_input = 5000

    expected_output = "moderate"  

    result = get_visibility_description(test_input)

    assert result == expected_output

def test_returns_none_for_invalid_input():

    test_input = -1

    expected_output = None  

    result = get_visibility_description(test_input)

    assert result == expected_output

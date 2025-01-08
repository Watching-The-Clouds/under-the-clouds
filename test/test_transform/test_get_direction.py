from transform_utils import get_direction
import pytest

def test_returns_string():

    test_input = 350

    result = get_direction(test_input)

    assert type(result) == str

def test_returns_correct_string():

    test_input = 350

    expected_output = "North"  

    result = get_direction(test_input)

    assert result == expected_output

def test_returns_none_for_invalid_input():

    test_input = 361

    expected_output = None  

    result = get_direction(test_input)

    assert result == expected_output

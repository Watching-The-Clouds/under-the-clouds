from extract_utils import format_data
import pytest

def test_returns_list():
    test_input = {'city': {}, 'list': []}

    assert type(format_data(test_input)) == list

def test_empty_data():
    test_input = {'city': {}, 'list': []}

    result = format_data(test_input)

    assert result == []

def test_combines_dicts_correctly_for_single_forecast():
    test_input = {'city': {'lat': 1, 'lon':2}, 
                  'list': [{'pressure': 3, 'temp':4}]}

    result = format_data(test_input)

    expected = [{'lat': 1, 'lon': 2, 'pressure': 3, 'temp': 4}]

    assert result == expected

def test_combines_dicts_correctly_for_multiple_forecasts():
    test_input = {'city': {'lat': 1, 'lon': 2}, 
                  'list': [{'pressure': 3, 'temp': 4},
                           {'pressure': 5, 'temp': 6}]}

    result = format_data(test_input)

    expected = [{'lat': 1, 'lon': 2, 'pressure': 3, 'temp': 4},
                {'lat': 1, 'lon': 2, 'pressure': 5, 'temp': 6}]

    assert result == expected

def test_for_more_nested_levels():
    test_input = {'city': {'lat': 1, 'lon': 2}, 
                  'list': [{'pressure': 3, 'temp': 4, 'clouds': {'all': 100}},
                           {'pressure': 5, 'temp': 6, 'clouds': {'all': 100}}]}

    result = format_data(test_input)

    expected = [{'lat': 1, 'lon': 2, 'pressure': 3, 'temp': 4, 'clouds.all': 100},
                {'lat': 1, 'lon': 2, 'pressure': 5, 'temp': 6, 'clouds.all': 100}]

    assert result == expected
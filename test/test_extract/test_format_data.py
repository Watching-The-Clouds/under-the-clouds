from extract_utils import format_data
import pytest

test_input = {'city': {'coord': {'lat': 51.5085, 'lon': -0.1257},
          'country': 'GB',
          'id': 2643743,
          'name': 'London',
          'population': 1000000,
          'sunrise': 1733817329,
          'sunset': 1733845900,
          'timezone': 0},
 'cnt': 40,
 'cod': '200',
 'list': [{'clouds': {'all': 100},
           'dt': 1733842800,
           'dt_txt': '2024-12-10 15:00:00',
           'main': {'feels_like': 3.82,
                    'grnd_level': 1027,
                    'humidity': 79,
                    'pressure': 1032,
                    'sea_level': 1032,
                    'temp': 7.2,
                    'temp_kf': 0.03,
                    'temp_max': 7.2,
                    'temp_min': 7.17},
           'pop': 0,
           'sys': {'pod': 'd'},
           'visibility': 10000,
           'weather': [{'description': 'overcast clouds',
                        'icon': '04d',
                        'id': 804,
                        'main': 'Clouds'}],
           'wind': {'deg': 32, 'gust': 10.73, 'speed': 5.64}}]}

def test_returns_list():
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
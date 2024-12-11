from src.extract.extract_utils import format_data
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

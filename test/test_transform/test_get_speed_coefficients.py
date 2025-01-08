import pandas as pd
import pytest
from transform_utils import get_speed_coefficients

@pytest.fixture
def sample_row():
    return pd.Series({
        'weather_impact_code': 'clear',
        'visibility_description': 'high'
    })

def test_clear_weather_high_visibility(sample_row):
    result = get_speed_coefficients(sample_row)
    assert result[0] == 1.0 
    assert result[1] == 1.0  

def test_light_rain_normal_visibility():
    row = pd.Series({
        'weather_impact_code': 'light_rain',
        'visibility_description': 'moderate'
    })
    result = get_speed_coefficients(row)
    assert result[0] == 0.97  
    assert result[1] == 0.87  

def test_snow_low_visibility():
    row = pd.Series({
        'weather_impact_code': 'snow',
        'visibility_description': 'low'
    })
    result = get_speed_coefficients(row)
    assert result[0] == 0.85  
    assert result[1] == 0.48  

def test_unknown_weather():
    row = pd.Series({
        'weather_impact_code': 'unknown',
        'visibility_description': 'high'
    })
    result = get_speed_coefficients(row)
    assert result[0] == 1.0
    assert result[1] == 1.0
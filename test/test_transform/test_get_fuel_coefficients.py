import pandas as pd
import pytest
from transform_utils import get_fuel_usage_coefficients

@pytest.fixture
def sample_row():
    return pd.Series({
        'weather_impact_code': 'clear'
    })

def test_clear_weather(sample_row):
    result = get_fuel_usage_coefficients(sample_row)
    assert result[0] == 1.00 
    assert result[1] == 1.00  

def test_light_rain():
    row = pd.Series({'weather_impact_code': 'light_rain'})
    result = get_fuel_usage_coefficients(row)
    assert result[0] == 1.10 
    assert result[1] == 1.15 

def test_heavy_rain():
    row = pd.Series({'weather_impact_code': 'heavy_rain'})
    result = get_fuel_usage_coefficients(row)
    assert result[0] == 1.10  
    assert result[1] == 1.15  

def test_snow():
    row = pd.Series({'weather_impact_code': 'snow'})
    result = get_fuel_usage_coefficients(row)
    assert result[0] == 1.07  
    assert result[1] == 1.35  

def test_unknown_weather():
    row = pd.Series({'weather_impact_code': 'unknown'})
    result = get_fuel_usage_coefficients(row)
    assert result[0] == 1.00  
    assert result[1] == 1.00  

def test_rounding():
    row = pd.Series({'weather_impact_code': 'light_rain'})
    result = get_fuel_usage_coefficients(row)
    assert isinstance(result[0], float)
    assert isinstance(result[1], float)
    assert str(result[1])[:4] == '1.15'  
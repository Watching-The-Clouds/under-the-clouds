import pytest
import pandas as pd
from transform_utils import calculate_time_increase

def test_clear_weather_high_visibility():
    df = pd.DataFrame({
        'weather_id': [800],
        'visibility': [10000],
        'visibility_description': ['high']
    })

    result = calculate_time_increase(df)

    assert 'weather_impact_code' in result.columns
    assert result['weather_impact_code'].iloc[0] == 'clear'
    assert result['speed_coefficient_low'].iloc[0] == 1.0
    assert result['speed_coefficient_high'].iloc[0] == 1.0

def test_light_rain_moderate_visibility():
    df = pd.DataFrame({
        'weather_id': [501],
        'visibility': [8000],
        'visibility_description': ['moderate']
    })

    result = calculate_time_increase(df)

    assert result['weather_impact_code'].iloc[0] == 'light_rain'
    assert result['speed_coefficient_low'].iloc[0] == 0.97
    assert result['speed_coefficient_high'].iloc[0] == 0.87

def test_heavy_rain_low_visibility():
    df = pd.DataFrame({
        'weather_id': [522],
        'visibility': [3000],
        'visibility_description': ['low']
    })

    result = calculate_time_increase(df)

    assert result['weather_impact_code'].iloc[0] == 'heavy_rain'
    assert result['speed_coefficient_low'].iloc[0] == 0.87
    assert result['speed_coefficient_high'].iloc[0] == 0.72

def test_snow_high_visibility():
    df = pd.DataFrame({
        'weather_id': [600],
        'visibility': [10000],
        'visibility_description': ['high']
    })

    result = calculate_time_increase(df)

    assert result['weather_impact_code'].iloc[0] == 'snow'
    assert result['speed_coefficient_low'].iloc[0] == 0.95
    assert result['speed_coefficient_high'].iloc[0] == 0.60

def test_unknown_weather_code():
    df = pd.DataFrame({
        'weather_id': [999],
        'visibility': [10000],
        'visibility_description': ['high']
    })
    
    result = calculate_time_increase(df)
    
    assert result['weather_impact_code'].iloc[0] == 'Unknown weather code'
    assert result['speed_coefficient_low'].iloc[0] == 1.0
    assert result['speed_coefficient_high'].iloc[0] == 1.0

def test_multiple_weather_conditions():
    df = pd.DataFrame({
        'weather_id': [800, 500, 502, 601],
        'visibility': [10000, 7000, 3000, 10000],
        'visibility_description': ['high', 'moderate', 'low', 'high']
    })
    
    result = calculate_time_increase(df)
    
    assert len(result) == 4
    assert list(result['weather_impact_code']) == ['clear', 'light_rain', 'heavy_rain', 'snow']
    
    # Check if all coefficient columns exist and have valid values
    assert all(0 <= result['speed_coefficient_low']) and all(result['speed_coefficient_low'] <= 1)
    assert all(0 <= result['speed_coefficient_high']) and all(result['speed_coefficient_high'] <= 1)

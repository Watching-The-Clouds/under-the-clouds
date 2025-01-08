import pandas as pd
import pytest
from transform_utils import calculate_fuel_usage_increase

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'weather_impact_code': ['clear', 'light_rain', 'snow', 'heavy_rain', 'unknown']
    })

def test_returns_new_columns(sample_dataframe):
    result = calculate_fuel_usage_increase(sample_dataframe)
    
    expected_columns = [
        'weather_impact_code',
        'fuel_usage_coefficient_low',
        'fuel_usage_coefficient_high'
    ]
    
    for col in expected_columns:
        assert col in result.columns

def test_dataframe_immutability(sample_dataframe):
    original_df = sample_dataframe.copy()
    _ = calculate_fuel_usage_increase(sample_dataframe)
    
    pd.testing.assert_frame_equal(sample_dataframe, original_df)
    

def test_returns_correctfuel_coefficients(sample_dataframe):
    result = calculate_fuel_usage_increase(sample_dataframe)
    
    # Clear weather
    assert result.loc[0, 'fuel_usage_coefficient_low'] == 1.00
    assert result.loc[0, 'fuel_usage_coefficient_high'] == 1.00
    
    # Light rain
    assert result.loc[1, 'fuel_usage_coefficient_low'] == 1.10
    assert result.loc[1, 'fuel_usage_coefficient_high'] == 1.15
    
    # Snow
    assert result.loc[2, 'fuel_usage_coefficient_low'] == 1.07
    assert result.loc[2, 'fuel_usage_coefficient_high'] == 1.35



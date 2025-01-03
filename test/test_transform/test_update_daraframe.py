from transform_utils import update_dataframe
import pytest
from unittest.mock import patch
import pandas as pd
from io import StringIO

# CSV data as a string
test_csv_data = """clouds.all,coord.lat,coord.lon,country,dt,dt_txt,id,main.feels_like,main.grnd_level,main.humidity,main.pressure,main.sea_level,main.temp,main.temp_kf,main.temp_max,main.temp_min,name,pop,population,rain.3h,snow.3h,sunrise,sunset,sys.pod,timezone,visibility,weather.0.description,weather.0.icon,weather.0.id,weather.0.main,wind.deg,wind.gust,wind.speed
100,44.34,10.99,IT,1661871600,2022-08-30 15:00:00,3163858,296.98,933,69,1015,1015,296.76,-1.11,297.87,296.76,Zocca,0.32,4593,0.26,0,1661834187,1661882248,d,7200,10000,light rain,10d,500,Rain,349,1.18,0.62
96,44.34,10.99,IT,1661882400,2022-08-30 18:00:00,3163858,295.59,931,71,1015,1015,295.45,2.61,295.45,292.84,Zocca,0.33,4593,0.57,0,1661834187,1661882248,n,7200,10000,light rain,10n,500,Rain,157,3.39,1.97"""

# Use StringIO to simulate a file object
test_csv_file = StringIO(test_csv_data)

# Load into a pandas DataFrame
test_df = pd.read_csv(test_csv_file)

def test_column_renaming():

    # Mock utility functions
    with (
        patch("transform_utils.update_wind_direction", side_effect=lambda x: f"{x}_updated"),
        patch("transform_utils.update_visibility_description", side_effect=lambda x: f"visibility_{x}"),
        patch("transform_utils.calculate_time_increase", return_value=test_df),
        patch("transform_utils.calculate_fuel_usage_increase", return_value=test_df)
    ):
        # Execute the function being tested
        result = update_dataframe(test_df)

    # Expected columns after renaming and transformations
    expected_columns = [
        "city", "date_time", "temp_max", "temp_min", "feels_like", "weather_description",
        "weather_id", "precipitation", "wind_direction", "wind_speed", "visibility",
        "visibility_description"
    ]

    # Validate the column names
    assert list(result.columns) == expected_columns

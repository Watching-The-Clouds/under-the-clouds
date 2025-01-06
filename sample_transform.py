from pprint import pprint
import pandas as pd
import csv
import io
import json

# Code to produce samples of outputs from each function, using sample data from OpenWeatherMap API converted into .csv format (in sample_csv.csv)

with open('sample_csv.csv', 'r') as data:
    csv_data = data.read()

def convert_csv_to_dataframe(csv_data):
    """
    Converts data from .csv format into a Pandas dataframe.
    
    Parameters:
        a string containing .csv data    

    Returns:
        a Pandas dataframe  
    """

    file_stream = io.StringIO(csv_data)

    df = pd.read_csv(file_stream)
    
    return df

def generate_new_columns(df):
    """
    Combines rain.3h and snow.3h into a single 'precipitation' column
    
    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """

    df_copy = df.copy()

    df_copy["rain.3h"] = df_copy.get("rain.3h", 0)
    df_copy["snow.3h"] = df_copy.get("snow.3h", 0)
    df_copy["precipitation"] = df_copy["rain.3h"] + df_copy["snow.3h"]

    return df_copy

def drop_and_rename_column(df):
    """
    Drops unnecessary columns and renames columns to have more suitable titles.
    
    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """
    df_copy = df.copy()

    columns_to_keep = {
        "name": "city",
        "dt_txt": "date_time",
        "main.temp_max": "temp_max",
        "main.temp_min": "temp_min",
        "main.feels_like": "feels_like",
        "weather.0.description": "weather_description",
        "weather.0.id": "weather_id",
        "wind.deg": "wind_direction",
        "wind.speed": "wind_speed",
        "visibility": "visibility",
        "precipitation": "precipitation"

    }

    df_copy = df_copy[columns_to_keep.keys()].rename(columns=columns_to_keep)

    return df_copy

def update_wind_direction(df):
    """
    Updates wind_direction column to have descriptive values instead of degrees (ie 350 --> "North")
    
    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """
    df_copy = df.copy()

    directions = {
        (348.75, 360): "North", 
        (0, 11.25): "North",
        (11.25, 33.75): "North-Northeast",
        (33.75, 56.25): "Northeast",
        (56.25, 78.75): "East-Northeast",
        (78.75, 101.25): "East",
        (101.25, 123.75): "East-Southeast",
        (123.75, 146.25): "Southeast",
        (146.25, 168.75): "South-Southeast",
        (168.75, 191.25): "South",
        (191.25, 213.75): "South-Southwest",
        (213.75, 236.25): "Southwest",
        (236.25, 258.75): "West-Southwest",
        (258.75, 281.25): "West",
        (281.25, 303.75): "West-Northwest",
        (303.75, 326.25): "Northwest",
        (326.25, 348.75): "North-Northwest"
    }

    def get_direction(degrees):
        """Helper function to map degrees to cardinal directions."""
        for (start, end), direction in directions.items():
            if start <= degrees < end or (start > end and (start <= degrees or degrees < end)):
                return direction
        return None
    
    df_copy["wind_direction"] = df_copy["wind_direction"].apply(get_direction)

    return df_copy

def update_visibility(df):
    """
    Updates visibility column to have descriptive values instead of metres (ie 2000 --> "low")
    
    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """
    df_copy = df.copy()

    visibility_categories = {
        (10000, float('inf')): "high",
        (5000, 9999): "moderate",
        (0, 4999): "low"
    }

    def get_visibility_description(visibility):
        for (start, end), category in visibility_categories.items():
            if start <= visibility < end:
                return category
        return None

    df_copy["visibility_description"] = df_copy["visibility"].apply(get_visibility_description)

    pprint(df_copy)
    return df_copy

update_visibility(update_wind_direction(drop_and_rename_column(generate_new_columns(convert_csv_to_dataframe(csv_data)))))
import boto3
import pandas as pd
import io
import os
import csv
from pprint import pprint

data_bucket = os.environ.get("INGESTION_BUCKET")
processed_data_bucket = os.environ.get("PROCESSED_BUCKET") # Not defined yet - what name?

def create_s3_client():
    """
    Creates an S3 client using boto3.

    Returns:
        An S3 client
    """
    return boto3.client("s3")

def fetch_csv_from_s3(s3_client, data_bucket, key):
    """Fetches data in .csv format from ingested S3 bucket.
    
    Parameters:
        s3_client: S3 client
        data_bucket: name of the ingested bucket (stored in .env)
        key: reference to the file in the S3 bucket

    Returns:
        a string containing .csv data    
    """
    try:
        obj = s3_client.get_object(Bucket=data_bucket, Key=key)
        csv_data = obj['Body'].read().decode('utf-8')
        return csv_data
    
    except Exception as e:
        print(f"Error fetching file from S3 for key '{key}': {e}")
        return None
    
def convert_csv_to_dataframe(csv_data):
    """Converts data from .csv format into a Pandas dataframe.
    
    Parameters:
        a string containing .csv data    

    Returns:
        a Pandas dataframe  
    """
    try:
        file_stream = io.StringIO(csv_data)
        return pd.read_csv(file_stream)
    
    except Exception as e:
        print(f"Error converting CSV data to DataFrame: {e}")
        return None

def update_dataframe():
    """
    Write docstring :)
    """

    df = convert_csv_to_dataframe(csv_data)

    new_df=df.rename(columns={
        "name": "city",
        "dt_txt": "date_time",
        "main.temp_max": "temp_max",
        "main.temp_min": "temp_min",
        "main.feels_like": "feels_like",
        "weather.0.description": "weather_description",
        "weather.0.id": "weather_id",
        "wind.deg": "wind_direction",
        "wind.speed": "wind_speed"
    })

    # Combines rain.3h and snow.3h into a single 'precipitation' column
    df["rain.3h"] = df.get("rain.3h", 0)
    df["snow.3h"] = df.get("snow.3h", 0)
    new_df["precipitation"] = df["rain.3h"] + df["snow.3h"]

    # https://saturncloud.io/blog/pandas-how-to-change-all-the-values-of-a-column/
    # Update wind_direction from degrees --> cardinal directions
    wind_column = new_df["wind_direction"]
    new_wind_column = wind_column.apply(update_wind_direction)
    new_df["wind_direction"] = new_wind_column

    # Create new column 'visibility_description' based on the visibility column
    new_df["visibility_description"] = new_df["visibility"].apply(update_visibility_description)

    basic_endpoint = new_df[[
            "city", 
            "date_time", 
            "temp_max", 
            "temp_min", 
            "feels_like", 
            "weather_description", 
            "precipitation", 
            "wind_direction", 
            "wind_speed", 
            "visibility",
            "visibility_description"
        ]]
    
    # Uncomment this, invoke update_dataframe to see the basic_endpoint output
    # basic_endpoint.to_csv('proper_test_output.csv')        

    return basic_endpoint

def calculate_time_increase():
    # Still 'per mile' and then multuiply by user input as required for final output
    
    base_speed_mph = 20 # miles per hour
    base_speed_mps = 20/(60*60) # miles per second
    base_time_spm = 1/base_speed_mps # seconds per mile
    fuel_efficiency = 8.5 # litres per 100 km

    # Match weather_id from dataframe to weather descriptor in this dict:
    weather_id = {
        "light_rain":[200,201,230,231,232,300,301,302,310,311,500,501,520],
        "heavy_rain":[202,312,313,314,321,502,503,504,511,521,522,531],
        "snow":[600,601,602,611,612,613,615,616,620,621,622],
        "clear":[800,801,802,803,804]
    }

    # Use weather description from above dict to match with (low, high) % impact on speed
    # For 'low_visibility'
    weather_impact = {
        "clear": (0,0),
        "light_rain":(3,13),
        "heavy_rain":(3,16),
        "snow":(5,40),
        "low_visibility":(10,12) # Based on visibility, NOT weather_description
    }

    pass

def calculate_cost_increase():
    # Still 'per mile' and then multuiply by user input as required for final output
    pass

def convert_to_parquet():
    pass

def store_in_s3(s3_client, parquet_file, bucket_name, file_name):
    """
    Uploads parquet file to a named AWS S3 bucket.

    Parameters:
        s3_client: boto3 S3 client
        parquet_file: transformed data in parquet format
        bucket_name (str): S3 bucket name
        file_name (str): S3 file directory and file name
    """
    
    s3_client.put_object(Body=parquet_file, Bucket=bucket_name, Key=file_name)

def update_wind_direction(degrees):

    # Mapping table as a dictionary
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
    
    # Match the degree to the correct direction
    for (start, end), direction in directions.items():
        if start <= degrees < end:
            return direction
    
    return "Invalid"  # Fallback for unexpected inputs

def update_visibility_description(visibility):
    
    visibility_categories = {
        (10000, 10001):"high",
        (5000,9999):"moderate",
        (0,4999):"low"
        }
    
    for (start, end), category in visibility_categories.items():
        if start <= visibility < end:
            return category 

calculate_time_increase()
# update_dataframe()
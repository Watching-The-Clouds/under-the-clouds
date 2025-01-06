import boto3
import pandas as pd
import io


def create_s3_client():
    """
    Creates an S3 client using boto3.

    Returns:
        An S3 client
    """
    return boto3.client("s3")


def fetch_csv_from_s3(s3_client, ingested_bucket, file_directory):
    """Fetches data in .csv format from ingested S3 bucket.

    Parameters:
        s3_client: S3 client
        data_bucket: name of the ingested bucket (stored in .env)
        key: reference to the file in the S3 bucket

    Returns:
        a string containing .csv data
    """

    obj = s3_client.get_object(Bucket=ingested_bucket, Key=file_directory)
    csv_data = obj["Body"].read().decode("utf-8")

    return csv_data


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


def generate_new_column(df):
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


def drop_and_rename_columns(df):
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
        "precipitation": "precipitation",
    }

    df_copy = df_copy[columns_to_keep.keys()].rename(columns=columns_to_keep)

    return df_copy


def get_direction(degrees):
    """
    Helper function to map degrees to cardinal directions.
    """

    if degrees == 360:
        degrees = 0

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
        (326.25, 348.75): "North-Northwest",
    }

    for (start, end), direction in directions.items():
        if start <= degrees < end or (
            start > end and (start <= degrees or degrees < end)
        ):
            return direction
    return None


def update_wind_direction(df):
    """
    Updates wind_direction column to have descriptive values instead of degrees (ie 350 --> "North")

    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """
    
    df_copy = df.copy()
    df_copy["wind_direction"] = df_copy["wind_direction"].apply(get_direction)

    return df_copy


def get_visibility_description(visibility):
    visibility_categories = {
        (10000, float("inf")): "high",
        (5000, 9999): "moderate",
        (0, 4999): "low",
    }

    for (start, end), category in visibility_categories.items():
        if start <= visibility < end:
            return category
    return None


def update_visibility(df):
    """
    Updates visibility column to have descriptive values instead of metres (ie 2000 --> "low")

    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """
    df_copy = df.copy()

    df_copy["visibility_description"] = df_copy["visibility"].apply(
        get_visibility_description
    )

    return df_copy


def get_weather_impact(weather_id):
    """
    Matches OpenWeatherMap API weather codes to general weather descriptions (eg light_rain, snow ...)
    """

    weather_id_dict = {
        "light_rain": [200, 201, 230, 231, 232, 300, 301, 302, 310, 311, 500, 501, 520],
        "heavy_rain": [202, 312, 313, 314, 321, 502, 503, 504, 511, 521, 522, 531],
        "snow": [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622],
        "clear": [
            800,
            801,
            802,
            803,
            804,
            701,
            711,
            721,
            731,
            741,
            751,
            761,
            762,
            771,
            781,
        ],
    }
    for description, id_list in weather_id_dict.items():
        if weather_id in id_list:
            return description
    return "Unknown weather code"


def get_speed_coefficients(row):
    """
    Calculates the % impact on base_speed based on the weather description (eg light_rain reduces speed by 3-13%)
    Data for calculations coming from US Dept. for Transportation Federal Highway Administration
    """

    weather_impact = {
        "clear": (0, 0),
        "light_rain": (3, 13),
        "heavy_rain": (3, 16),
        "snow": (5, 40),
        "low_visibility": (10, 12),
    }
    impact_values = weather_impact.get(row["weather_impact_code"], (0, 0))

    if row["visibility_description"] == "low":
        vis_impact = weather_impact["low_visibility"]
        low_impact = impact_values[0] + vis_impact[0]
        high_impact = impact_values[1] + vis_impact[1]
    else:
        low_impact = impact_values[0]
        high_impact = impact_values[1]

    low_coef = 1 - (low_impact / 100)
    high_coef = 1 - (high_impact / 100)

    return pd.Series([low_coef, high_coef])


def calculate_time_increase(basic_endpoint):
    """
    Applies speed and fuel efficiency coefficients to dataframe. The coefficients are calculated
    in get_speed_coefficients() and get_weather_impact(). Later, the coefficients are applied
    to the user-provided input to calculate the time and fuel usage.

    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """

    base_speed_mph = 20  # miles per hour
    base_speed_mps = 20 / (60 * 60)  # miles per second
    base_time_spm = 1 / base_speed_mps  # seconds per mile
    fuel_efficiency = 8.5  # litres per 100 km

    df = basic_endpoint.copy()
    df["weather_impact_code"] = df["weather_id"].apply(get_weather_impact)
    df[["speed_coefficient_low", "speed_coefficient_high"]] = df.apply(
        get_speed_coefficients, axis=1
    )

    return df


def get_fuel_usage_coefficients(row):
    weather_impact = {
        "clear": (0, 0),
        "light_rain": (10, 14.5),
        "heavy_rain": (10, 14.5),
        "snow": (7, 35),
    }
    impact_values = weather_impact.get(row["weather_impact_code"], (0, 0))
    low_coef = round(1 + (impact_values[0] / 100), 2)
    high_coef = round(1 + (impact_values[1] / 100), 2)
    return pd.Series([low_coef, high_coef])


def calculate_fuel_usage_increase(basic_endpoint):
    """
    Adds fuel usage coefficients to dataframe. The coefficients are calculated
    in get_fuel_usage_coefficients(). Later, the coefficients
    are applied to the user-provided input to calculate the fuel usage.

    Parameters:
        a Pandas dataframe

    Returns:
        an updated Pandas dataframe
    """

    df = basic_endpoint.copy()
    df[["fuel_usage_coefficient_low", "fuel_usage_coefficient_high"]] = df.apply(
        get_fuel_usage_coefficients, axis=1
    )

    return df


def convert_to_parquet(ready_basic_endpoint):
    """
    Converts pandas dataframe into a binary file-like object

    Parameters:
        a Pandas dataframe

    Returns:
        returns binary content of parquet file
    """

    parquet_buffer = io.BytesIO()
    ready_basic_endpoint.to_parquet(parquet_buffer, index=False)

    parquet_body = parquet_buffer.getvalue()

    return parquet_body


def store_in_s3(s3_client, parquet_body, processed_bucket, file_directory):
    """
    Updates directory from .csv to .parquet
    Uploads binary of parquet file to a named AWS S3 bucket in .parquet format

    Parameters:
        s3_client: boto3 S3 client
        parquet_body: transformed binary data of parquet file
        processed_bucket (str): S3 bucket name
        file_directory (str): S3 file directory and file name
    """

    file_directory = file_directory.rsplit('.', 1)[0] + '.parquet'

    s3_client.put_object(Body=parquet_body, Bucket=processed_bucket, Key=file_directory)

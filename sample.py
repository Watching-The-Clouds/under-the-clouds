from pprint import pprint
from datetime import datetime
import boto3
import requests
import os
import csv
import io
import json

# Code to produce samples of outputs from each function, using sample data from OpenWeatherMap API.

data = {
    "cod": "200",
    "message": 0,
    "cnt": 40,
    "list": [
      {
        "dt": 1661871600,
        "main": {
          "temp": 296.76,
          "feels_like": 296.98,
          "temp_min": 296.76,
          "temp_max": 297.87,
          "pressure": 1015,
          "sea_level": 1015,
          "grnd_level": 933,
          "humidity": 69,
          "temp_kf": -1.11
        },
        "weather": [
          {
            "id": 500,
            "main": "Rain",
            "description": "light rain",
            "icon": "10d"
          }
        ],
        "clouds": {
          "all": 100
        },
        "wind": {
          "speed": 0.62,
          "deg": 349,
          "gust": 1.18
        },
        "visibility": 10000,
        "pop": 0.32,
        "rain": {
          "3h": 0.26
        },
        "sys": {
          "pod": "d"
        },
        "dt_txt": "2022-08-30 15:00:00"
      },
      {
        "dt": 1661882400,
        "main": {
          "temp": 295.45,
          "feels_like": 295.59,
          "temp_min": 292.84,
          "temp_max": 295.45,
          "pressure": 1015,
          "sea_level": 1015,
          "grnd_level": 931,
          "humidity": 71,
          "temp_kf": 2.61
        },
        "weather": [
          {
            "id": 500,
            "main": "Rain",
            "description": "light rain",
            "icon": "10n"
          }
        ],
        "clouds": {
          "all": 96
        },
        "wind": {
          "speed": 1.97,
          "deg": 157,
          "gust": 3.39
        },
        "visibility": 10000,
        "pop": 0.33,
        "rain": {
          "3h": 0.57
        },
        "sys": {
          "pod": "n"
        },
        "dt_txt": "2022-08-30 18:00:00"
      },
      {
        "dt": 1661893200,
        "main": {
          "temp": 292.46,
          "feels_like": 292.54,
          "temp_min": 290.31,
          "temp_max": 292.46,
          "pressure": 1015,
          "sea_level": 1015,
          "grnd_level": 931,
          "humidity": 80,
          "temp_kf": 2.15
        },
        "weather": [
          {
            "id": 500,
            "main": "Rain",
            "description": "light rain",
            "icon": "10n"
          }
        ],
        "clouds": {
          "all": 68
        },
        "wind": {
          "speed": 2.66,
          "deg": 210,
          "gust": 3.58
        },
        "visibility": 10000,
        "pop": 0.7,
        "rain": {
          "3h": 0.49
        },
        "sys": {
          "pod": "n"
        },
        "dt_txt": "2022-08-30 21:00:00"
      },
      {
        "dt": 1662292800,
        "main": {
          "temp": 294.93,
          "feels_like": 294.83,
          "temp_min": 294.93,
          "temp_max": 294.93,
          "pressure": 1018,
          "sea_level": 1018,
          "grnd_level": 935,
          "humidity": 64,
          "temp_kf": 0
        },
        "weather": [
          {
            "id": 804,
            "main": "Clouds",
            "description": "overcast clouds",
            "icon": "04d"
          }
        ],
        "clouds": {
          "all": 88
        },
        "wind": {
          "speed": 1.14,
          "deg": 17,
          "gust": 1.57
        },
        "visibility": 10000,
        "pop": 0,
        "sys": {
          "pod": "d"
        },
        "dt_txt": "2022-09-04 12:00:00"
      }
    ],
    "city": {
      "id": 3163858,
      "name": "Zocca",
      "coord": {
        "lat": 44.34,
        "lon": 10.99
      },
      "country": "IT",
      "population": 4593,
      "timezone": 7200,
      "sunrise": 1661834187,
      "sunset": 1661882248
    }
  }

def flatten(x, name=''):
    """
    Uses recursion to flatten object to create key:value pairs that can later be used for column titles.

    Parameters:
        x: represents object passed to flatten - can be a dict, a list, or a primitive value (base case)
        name: name of object passed into function

    Returns:
        list of flattened dictionaries
    """
    
    flattened_list = []
    
    if isinstance(x, dict):  # Process dictionaries
        for key, value in x.items():
            new_key = f"{name}.{key}" if name else key
            flattened_list.extend(flatten(value, new_key).items())
    
    elif isinstance(x, list):  # Process lists
        for i, value in enumerate(x):
            new_key = f"{name}.{i}" if name else str(i)
            flattened_list.extend(flatten(value, new_key).items())
    
    else:  
        flattened_list.append((name, x))
    
    return dict(flattened_list)

def format_data(data):
    """
    Takes nested data in Python dictionary format and returns list of flattened dictionaries

    Parameters:
        Python dictionary containing forecast data for 5 days in 3 hour intervals (8 forecasts per day for 5 days = 40 forecasts)

    Returns:
        List containing 40 dictionaries (1 per forecast)
    """

    flattened_data = []

    for x in data["list"]:

        city_dict = flatten(data["city"])
        forecast_dict = flatten(x)

        flatten_dict = city_dict|forecast_dict

        flattened_data.append(flatten_dict)    

    with open('sample_flattened_data.txt', 'w') as f:
        json.dump(flattened_data, f)

    return flattened_data

def convert_to_csv(flattened_data):
    """
    Takes a list of flattened dictionaries and converts it into .csv format.

    Parameters:
        List containing 40 dictionaries (1 per forecast)

    Returns:
        .csv file
    """

    additional_keys = ["rain.3h", "snow.3h"]

    all_keys = set()
    for dict in flattened_data:
        all_keys.update(dict.keys())

    all_keys.update(set(additional_keys))

    all_keys = sorted(all_keys)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=all_keys)
    writer.writeheader()

    for dict in flattened_data:
        writer.writerow({key: dict.get(key, 0) for key in all_keys})

    converted_data = output.getvalue()  
    output.close()

    with open('sample_csv.csv', 'w') as f:
        f.write(converted_data)

    return converted_data

convert_to_csv(format_data(data))
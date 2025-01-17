from fastapi import FastAPI, Query
from pydantic import BaseModel
from src.API.connect import connect_to_db
import psycopg
from mangum import Mangum

app = FastAPI()

columns_to_include = "index, city, date_time, feels_like, weather_description, speed_coefficient_high, speed_coefficient_low"

@app.get("/healthcheck")
def healthcheck():
    return {"status": "all okay :)"}

@app.get("/get_all")
def get_weather_impact():
    conn = connect_to_db()
    query = "SELECT * FROM weather_forecasts"
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        cursor.execute(query)
        weather_impact = cursor.fetchall()
    conn.close()
    return weather_impact

@app.get("/get_weather_impact")
def get_weather_impact():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_forecasts ORDER BY index DESC LIMIT 10")
    weather_impact = cursor.fetchall()
    cursor.close()
    conn.close()
    return weather_impact

# Add ability for user to input values for speed and distance of journey (defaults: speed = 20 mph, distance = 1 mile)

@app.get("/trimmed")
def get_weather_impact():
    conn = connect_to_db()
    query = "SELECT city, date_time, feels_like, weather_description, visibility_description, speed_coefficient_low, speed_coefficient_high, fuel_usage_coefficient_low, fuel_usage_coefficient_high FROM weather_forecasts ORDER BY index DESC LIMIT 40"
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        cursor.execute(query)
        weather_impact = cursor.fetchall()
    conn.close()
    return weather_impact

# Call with /get_impact_on_time?speed=30&distance=5 for custom values
@app.get("/get_time_impact")
def get_impact_on_time(
    speed: float = Query(20.0, description="Speed in mph (default: 20 mph)"),
    distance: float = Query(1.0, description="Distance in miles (default: 1 mile)")
):
    conn = connect_to_db()
    query = f"SELECT {columns_to_include} FROM weather_forecasts ORDER BY index DESC LIMIT 40"

    with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    conn.close()

    for record in results:
        base_time = (distance / speed) * 60  # Base time in minutes
        high_time_estimate = base_time * record["speed_coefficient_high"]
        low_time_estimate = base_time * record["speed_coefficient_low"]
        
        record["journey_time_estimate"] = f"{round(low_time_estimate, 2)} - {round(high_time_estimate, 2)} minutes"

        del record["speed_coefficient_high"]
        del record["speed_coefficient_low"]

    return results

handler = Mangum(app)
from fastapi import FastAPI
from pydantic import BaseModel
from src.API.connect import connect_to_db
import psycopg
# from psycopg2.extras import DictCursor

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.get("/get_weather_impact")
def get_weather_impact():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_forecasts")
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

@app.get("/trimmed2")
def get_weather_impact():
    conn = connect_to_db()
    query = "SELECT index, city, date_time FROM weather_forecasts ORDER BY index ASC LIMIT 40"
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        cursor.execute(query)
        weather_impact = cursor.fetchall()

    conn.close()
    return weather_impact
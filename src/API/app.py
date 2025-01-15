from fastapi import FastAPI
from pydantic import BaseModel
from src.API.connect import connect_to_db

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "all okay :)"}

@app.get("/get_weather_impact")
def get_weather_impact():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_forecasts")
    weather_impact = cursor.fetchall()
    cursor.close()
    conn.close()
    return weather_impact
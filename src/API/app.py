from fastapi import FastAPI
from pydantic import BaseModel
from src.API.connect import connect_to_db
from mangum import Mangum


app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.get("/get_weather_impact")
def get_weather_impact():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_forecasts ORDER BY index DESC LIMIT 10")
    weather_impact = cursor.fetchall()
    cursor.close()
    conn.close()
    return weather_impact

handler = Mangum(app)



import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    return psycopg2.connect(
    host= os.environ["DB_HOST"],
    port= os.environ["DB_PORT"],
    dbname= os.environ["DB_NAME"],
    user= os.environ["DB_USER"],
    password= os.environ["DB_PASSWORD"]
    )
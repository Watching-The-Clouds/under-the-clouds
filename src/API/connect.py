import psycopg
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def connect_to_db():
    # Add logging to debug connection issues
    logging.info(f"Attempting to connect to: {os.environ['DB_HOST']}:{os.environ['DB_PORT']}")
    
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=10  
    )
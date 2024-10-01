import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
def connect_to_database():
# Establish a connection to the MySQL database
    conn = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password= os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
    )
    return conn


import mysql.connector
import os
from dotenv import load_dotenv
import logging

load_dotenv(dotenv_path='.env')


# Establish a connection to the MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password= os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
        )
        logging.info("Database connection established ")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error Connecting to MYSQL : {err}")




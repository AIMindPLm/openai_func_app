import mysql.connector

def connect_to_database():
# Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host="database-1.czjbva8mjsze.ap-south-1.rds.amazonaws.com",
    user="RZCvH6mU954tK",
    password="hDxBO2q08qWrHJRf",
    database="MRP_PROD"
    )
    return conn
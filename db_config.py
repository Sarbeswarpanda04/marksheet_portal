# db_config.py

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # your MySQL username
        password="Sarbeswar@123",            # your MySQL password
        database="marksheet_portal"
    )

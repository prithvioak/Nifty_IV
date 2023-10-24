import mysql.connector
import requests

def db_connect(pw): # how to make this universal - pass a parameter?
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        # password="akshay4455",
        password=pw,
        database="nse_fetch_data"
    )
    cursor = db.cursor()
    return cursor, db

def insert_into_db(insert_query, data, pw):
    cursor, connection = db_connect(pw)
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
    except requests.RequestException as re:
        print(f"Request error occurred: {re}")
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
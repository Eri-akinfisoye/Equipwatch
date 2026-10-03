import psycopg2
import os
from dotenv import load_dotenv


""" 
This is resposnisble for connecting the simulator.py file to the database (postgres). It pushes the CSV file 
"""
#load the env variables 
load_dotenv()

def get_connection():
    
    #load the env variables 
    

    try:

        #creates the connection line to the database
        conn = psycopg2.connect(
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT")
        )

    except  Exception as error:
        print(f'This is the error {error}')

        return None
    
    return conn


def create_table():

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:

                table_script = (
                    """ CREATE TABLE IF NOT EXISTS sensor_readings(
                            id SERIAL PRIMARY KEY,
                            timestamp TIMESTAMP,
                            equipment VARCHAR(50),
                            section VARCHAR(10),
                            current FLOAT,
                            temp FLOAT,
                            vibration FLOAT,
                            inserted_at TIMESTAMP DEFAULT NOW()
                            );
                    """
                )
                cursor.execute(table_script)

                print("------Table ready-----")
    finally:
        conn.close()

import psycopg2
from psycopg2.extras import execute_values


def insert_readings(df):
    conn = None
    try:
        conn = get_connection()

        # 1. Collect all row tuples into a list
        rows = []
        for _, row in df.iterrows():
            value = (
                row["timestamp"],
                row["equipment"],
                row["section"],
                row["current"],
                row["temp"],
                row["vibration"],
            )
            rows.append(value)

        # 2. Define the SQL query outside the loop
        insert_script = """
            INSERT INTO sensor_readings (timestamp, equipment, section, current, temp, vibration)
            VALUES %s;
        """

        # 3. Execute the batch insert
        with conn:
            with conn.cursor() as cursor:
                execute_values(cursor, insert_script, rows)

        print(f"{len(df)} rows inserted.")

    finally:
        # Safely close connection if it was successfully opened
        if conn:
            conn.close()


        







    


    
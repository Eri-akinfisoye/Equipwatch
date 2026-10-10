import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_values


""" 
This is responsible for connecting to the database (postgres) and inserting sensor readings.
"""
# Load the env variables
load_dotenv()


def get_connection():
    try:
        # Creates the connection line to the database
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
    except Exception as error:
        print(f'This is the error: {error}')
        return None
    return conn


def create_table():
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cursor:
                table_script = """
                    CREATE TABLE IF NOT EXISTS sensor_readings(
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP,
                        equipment VARCHAR(50),
                        section VARCHAR(20),
                        current FLOAT,
                        temp FLOAT,
                        vibration FLOAT,
                        current_baseline FLOAT,
                        temp_baseline FLOAT,
                        current_deviation_pct FLOAT,
                        temp_deviation_pct FLOAT,
                        power_kw FLOAT,
                        anomaly VARCHAR(20),
                        status VARCHAR(20),
                        inserted_at TIMESTAMP DEFAULT NOW()
                    );
                """
                cursor.execute(table_script)
                print("------Table ready (14 columns)-----")
    finally:
        conn.close()


def insert_readings(df):
    conn = None
    try:
        conn = get_connection()

        rows = []
        for _, row in df.iterrows():
            value = (
                row["timestamp"],
                row["equipment"],
                row["section"],
                row["current"],
                row["temp"],
                row["vibration"],
                row.get("current_baseline"),      # NEW
                row.get("temp_baseline"),         # NEW
                row.get("current_deviation_pct"), # NEW
                row.get("temp_deviation_pct"),    # NEW
                row.get("power_kw"),              # NEW
                row.get("anomaly"),               # NEW
                row.get("status"),                # NEW
            )
            rows.append(value)

        insert_script = """
            INSERT INTO sensor_readings (
                timestamp, equipment, section, current, temp, vibration,
                current_baseline, temp_baseline,
                current_deviation_pct, temp_deviation_pct,
                power_kw, anomaly, status
            )
            VALUES %s;
        """

        with conn:
            with conn.cursor() as cursor:
                execute_values(cursor, insert_script, rows)

        print(f"{len(df)} rows inserted with all engineered features.")

    finally:
        if conn:
            conn.close()


        







    


    
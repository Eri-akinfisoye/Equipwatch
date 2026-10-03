import os
import pandas as pd
import numpy as np

src_dir = os.path.dirname(os.path.abspath(__file__))  
project_root = os.path.dirname(src_dir)               
data_dir = os.path.join(project_root, 'data')         
csv_path = os.path.join(data_dir, 'simulated_readings.csv')

df = pd.read_csv(csv_path)

#Calculates curent_baseline
df['current_baseline'] = df['current'].rolling(window= 10).mean()

#Calculates curent_deviation_pct
df['current_deviation_pct'] = ((df['current'] - df['current_baseline']) / df['current_baseline']) * 100

#Calculates status
df['status'] = np.where(df['current_deviation_pct'] > 15, "Anomaly","Normal")

if __name__  == '__main__':
    from db import create_table, insert_readings
    create_table()
    insert_readings(df)



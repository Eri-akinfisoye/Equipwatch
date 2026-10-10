import os
import pandas as pd
import numpy as np

src_dir = os.path.dirname(os.path.abspath(__file__))  
project_root = os.path.dirname(src_dir)               
data_dir = os.path.join(project_root, 'data')         
csv_path = os.path.join(data_dir, 'simulated_readings.csv')

df = pd.read_csv(csv_path)

# Calculate current baseline (10-reading rolling average)
df['current_baseline'] = df['current'].rolling(window=10).mean()

# Calculate current deviation percentage
df['current_deviation_pct'] = ((df['current'] - df['current_baseline']) / df['current_baseline']) * 100

# Calculate temp baseline (10-reading rolling average)
df['temp_baseline'] = df['temp'].rolling(window=10).mean()

# Calculate temp deviation percentage
df['temp_deviation_pct'] = ((df['temp'] - df['temp_baseline']) / df['temp_baseline']) * 100

# Calculate power_kW (3-phase AC approximation: P = sqrt(3) * V * I * PF / 1000)
# Assume 400V line-to-line, power factor 0.85
df['power_kw'] = (np.sqrt(3) * 400 * df['current'] * 0.85) / 1000

# Anomaly flag: current deviation > 15% OR temp deviation > 10%
df['anomaly'] = np.where(
    (df['current_deviation_pct'].abs() > 15) | (df['temp_deviation_pct'].abs() > 10),
    "Anomaly", "Normal"
)

# Status classification: Critical > Warning > Normal
df['status'] = np.where(
    (df['current_deviation_pct'].abs() > 25) | (df['temp_deviation_pct'].abs() > 20),
    "Critical",
    np.where(df['anomaly'] == "Anomaly", "Warning", "Normal")
)

if __name__ == '__main__':
    from db import create_table, insert_readings
    create_table()
    insert_readings(df)



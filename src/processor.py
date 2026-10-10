import os
import pandas as pd
import numpy as np

# Import the detector module
from detector import run_detection

src_dir = os.path.dirname(os.path.abspath(__file__))  
project_root = os.path.dirname(src_dir)               
data_dir = os.path.join(project_root, 'data')         
csv_path = os.path.join(data_dir, 'simulated_readings.csv')

df = pd.read_csv(csv_path)

# Run the anomaly detection pipeline (Phase 3)
# This computes stable baselines, deviations, anomaly flags, blocks, and severity
df, baselines = run_detection(df)

# Map detector outputs to database schema columns
# Detector uses stable baselines (single value per machine) - broadcast to all rows
for equipment, baseline in baselines.items():
    mask = df['equipment'] == equipment
    df.loc[mask, 'current_baseline'] = baseline['current']
    df.loc[mask, 'temp_baseline'] = baseline['temp']

# Detector already computed current_deviation_pct and temp_deviation_pct

# Calculate power_kW (3-phase AC approximation: P = sqrt(3) * V * I * PF / 1000)
# Assume 400V line-to-line, power factor 0.85
df['power_kw'] = (np.sqrt(3) * 400 * df['current'] * 0.85) / 1000

# Map detector's is_anomaly (bool) to anomaly (VARCHAR)
df['anomaly'] = np.where(df['is_anomaly'], "Anomaly", "Normal")

# Map detector's severity to status (VARCHAR)
# severity is already 'Normal', 'Warning', 'Critical' per block
df['status'] = df['severity']

if __name__ == '__main__':
    from db import create_table, insert_readings
    create_table()
    insert_readings(df)



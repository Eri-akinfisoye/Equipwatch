import numpy as np      # For numerical operations and random number generation
import pandas as pd     # For creating and manipulating DataFrames
import os               # For building file paths that work across operating systems

# ─────────────────────────────────────────────
# EQUIPMENT PROFILES
# A dictionary storing the normal operating parameters for each machine.
# Each key is a machine name. Each value is another dictionary holding:
#   - section: the plant area the machine belongs to
#   - current_mean / current_std: average and spread of current draw in Amps
#   - temp_mean / temp_std: average and spread of temperature in °C
#   - vibration_mean / vibration_std: average and spread of vibration in mm/s
# These values define what "normal" looks like for each machine.
# Any reading that deviates significantly from these values is a candidate anomaly.
# ─────────────────────────────────────────────
equipment_profiles = {
    "MOTOR_1": {
        "section": "Electrical",
        "current_mean": 4.5,
        "current_std": 0.2,
        "temp_mean": 67.0,
        "temp_std": 1.5,
        "vibration_mean": 2.3,
        "vibration_std": 0.15
    },
    "MOTOR_2": {
        "section": "Electrical",
        "current_mean": 5.1,
        "current_std": 0.3,
        "temp_mean": 72.0,
        "temp_std": 2.0,
        "vibration_mean": 2.8,
        "vibration_std": 0.20
    },
    "PUMP_1": {
        "section": "Mechanical",
        "current_mean": 3.8,
        "current_std": 0.15,
        "temp_mean": 58.0,
        "temp_std": 1.0,
        "vibration_mean": 1.9,
        "vibration_std": 0.10
    },
    "PUMP_2": {
        "section": "Mechanical",
        "current_mean": 4.2,
        "current_std": 0.25,
        "temp_mean": 63.0,
        "temp_std": 1.5,
        "vibration_mean": 2.1,
        "vibration_std": 0.12
    },
    "COMPRESSOR_1": {
        "section": "Mechanical",
        "current_mean": 6.3,
        "current_std": 0.4,
        "temp_mean": 81.0,
        "temp_std": 2.5,
        "vibration_mean": 3.5,
        "vibration_std": 0.25
    }
}


def generate_readings(equipment_name, n_readings):
    """
    Generates normally distributed sensor readings for a single machine.

    Normal distribution is used because real industrial sensor readings
    naturally cluster around a mean value with small random variation.
    This mirrors real-world behaviour without requiring actual hardware.

    Parameters:
        equipment_name (str): Must match a key in equipment_profiles
        n_readings (int): Number of sensor readings to generate

    Returns:
        pd.DataFrame: One row per reading, with timestamp, equipment identity,
                      and sensor values for current, temperature, and vibration
    """
    # Look up this machine's operating parameters from the profiles dictionary
    machine = equipment_profiles[equipment_name]

    # Generate sensor readings using normal distribution:
    # np.random.normal(mean, std_deviation, number_of_readings)
    # Most values will cluster around the mean; a few will be higher or lower
    current = np.random.normal(machine['current_mean'], machine['current_std'], n_readings)
    temp = np.random.normal(machine['temp_mean'], machine['temp_std'], n_readings)
    vibration = np.random.normal(machine['vibration_mean'], machine['vibration_std'], n_readings)

    # Add a random offset (0–59 seconds) to simulate sensors not starting simultaneously
    # This simulates a sensor reporting at a fixed interval — common in industrial systems
    offset_seconds = np.random.randint(0, 60)
    start_time = pd.Timestamp('2026-01-01') + pd.Timedelta(seconds=offset_seconds)
    timestamp = pd.date_range(start=start_time, periods=n_readings, freq='5min')

    # Combine all arrays into a single DataFrame and return it
    return pd.DataFrame({
        'timestamp': timestamp,
        'equipment': equipment_name,       # Machine identifier
        'section': machine['section'],     # Plant section (Electrical or Mechanical)
        'current': current,                # Current draw in Amps
        'temp': temp,                      # Temperature in °C
        'vibration': vibration             # Vibration in mm/s
    })


def inject_fault(df, fault_fraction=0.2):
    """
    Simulates progressive equipment degradation by ramping sensor values
    upward in the last portion of readings.

    Real equipment rarely fails suddenly. It degrades gradually —
    current creeps up as a motor works harder, temperature rises as
    cooling efficiency drops, vibration increases as bearings wear.
    This function replicates that pattern using a linear ramp (linspace).

    Parameters:
        df (pd.DataFrame): Output from generate_readings() for one machine
        fault_fraction (float): Fraction of rows to affect. Default 0.2 = last 20%

    Returns:
        pd.DataFrame: Same structure as input, with fault ramp applied to
                      current, temp, and vibration in the tail rows
    """
    # Work on a copy so the original DataFrame is not modified
    df_fault = df.copy()

    # Calculate how many rows fall within the fault window
    # e.g. 200 readings × 0.2 = last 40 rows get the fault ramp
    n_faults = int(len(df_fault) * fault_fraction)

    # Safety check: if the fault window is zero rows, return unchanged
    if n_faults == 0:
        return df_fault

    # Get the integer column positions for current, temp, and vibration
    # Required for .iloc which works by position, not column name
    curr_col = df_fault.columns.get_loc('current')
    temp_col = df_fault.columns.get_loc('temp')
    vib_col = df_fault.columns.get_loc('vibration')

    # Apply a linear ramp to the last n_faults rows of each sensor column
    # np.linspace(start, stop, num) generates evenly spaced values from start to stop
    # Adding this to existing values creates a gradual upward drift — not a sudden spike
    # Current ramps up by 2.5A, temperature by 18°C, vibration by 3.2mm/s
    df_fault.iloc[-n_faults:, curr_col] += np.linspace(0, 2.5, num=n_faults)
    df_fault.iloc[-n_faults:, temp_col] += np.linspace(0, 18.0, num=n_faults)
    df_fault.iloc[-n_faults:, vib_col] += np.linspace(0, 3.2, num=n_faults)

    return df_fault

#Ensures Codes constantly remains the same
np.random.seed(42)

def simulate_fleet(n_readings=200):
    """
    Generates a full sensor dataset for all 5 machines in the fleet.

    Calls generate_readings() for every machine, then selectively injects
    faults into MOTOR_1 and PUMP_2 to simulate two degrading machines
    while the other three operate normally. All machine DataFrames are
    then stacked into one combined DataFrame.

    Parameters:
        n_readings (int): Number of readings per machine. Default 200.
                          Total rows = n_readings × number of machines.

    Returns:
        pd.DataFrame: Combined dataset for all machines, with a fresh
                      sequential index from 0 to (n_readings × 5) - 1
    """
    # Placeholder list to collect each machine's DataFrame before combining
    all_dataframes = []

    # Loop through every machine defined in equipment_profiles
    for equipment in equipment_profiles.keys():

        # Generate normal sensor readings for this machine
        data = generate_readings(equipment, n_readings)

        # Inject fault patterns into MOTOR_1 and PUMP_2 only
        # The other three machines (MOTOR_2, PUMP_1, COMPRESSOR_1) remain healthy
        # This creates a realistic scenario: not all machines fail at the same time
        if equipment in ('MOTOR_1', 'PUMP_2'):
            data = inject_fault(data)

        # Add this machine's DataFrame to the collection
        all_dataframes.append(data)

    # Stack all machine DataFrames vertically into one combined DataFrame
    # axis=0 means stack rows (not columns)
    # ignore_index=True resets the row numbers from 0 to total_rows - 1
    combined_df = pd.concat(all_dataframes, axis=0, ignore_index=True)

    return combined_df


# ─────────────────────────────────────────────
# ENTRY POINT
# This block only runs when simulator.py is executed directly from the terminal.
# It does NOT run when another file imports functions from this module.
# This separation keeps the simulator reusable as a library while still
# allowing it to be run standalone to generate and export the dataset.
# ─────────────────────────────────────────────
if __name__ == '__main__':

    # Generate the full fleet dataset — 200 readings × 5 machines = 1000 rows
    df_raw = simulate_fleet(n_readings=200)

    # Quick check before saving: confirm shape and preview first rows
    print('Shape:', df_raw.shape)
    print(df_raw.head())

    # Build an absolute path to the data/ folder based on this file's location
    # This approach works regardless of where the terminal command was run from
    src_dir = os.path.dirname(os.path.abspath(__file__))  # .../EquipWatch/src
    project_root = os.path.dirname(src_dir)               # .../EquipWatch
    data_dir = os.path.join(project_root, 'data')         # .../EquipWatch/data

    # Create the data/ folder if it doesn't already exist
    # exist_ok=True prevents an error if the folder is already there
    os.makedirs(data_dir, exist_ok=True)

    # Build the full output file path
    output_path = os.path.join(data_dir, 'simulated_readings.csv')

    # Export the DataFrame to CSV
    # index=False prevents pandas from writing row numbers as a column in the file
    df_raw.to_csv(output_path, index=False)

    # Confirm export completed successfully
    print(f'Data exported successfully to {output_path}')
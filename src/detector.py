"""
Phase 3 — Anomaly Detection Engine

This module implements a production-style anomaly detection pipeline:
1. Compute STABLE baselines from healthy period (first 80% of data per machine)
2. Calculate deviations against those fixed baselines
3. Flag point anomalies using thresholds
4. Group contiguous anomaly points into blocks (with gap tolerance)
5. Classify block severity (Normal / Warning / Critical)

Key insight: Unlike rolling baselines that adapt to faults, stable baselines
represent "true normal" and catch full degradation cycles.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def compute_stable_baselines(df: pd.DataFrame, healthy_fraction: float = 0.8) -> Dict[str, Dict[str, float]]:
    """
    Compute fixed baselines per equipment using only the healthy period.

    Args:
        df: Full sensor DataFrame with columns ['equipment', 'current', 'temp', ...]
        healthy_fraction: Fraction of each machine's timeline considered healthy (default 0.8)

    Returns:
        Dict mapping equipment_name -> {'current': baseline, 'temp': baseline}
    """
    baselines = {}

    for equipment in df['equipment'].unique():
        machine_df = df[df['equipment'] == equipment].copy()
        machine_df = machine_df.sort_values('timestamp').reset_index(drop=True)

        # Healthy period = first 80% of readings (before injected faults)
        n_healthy = int(len(machine_df) * healthy_fraction)
        healthy_df = machine_df.iloc[:n_healthy]

        baselines[equipment] = {
            'current': healthy_df['current'].mean(),
            'temp': healthy_df['temp'].mean(),
        }

    return baselines


def calculate_deviations(df: pd.DataFrame, baselines: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Calculate percentage deviations from stable baselines.

    Adds columns:
        - current_deviation_pct
        - temp_deviation_pct
    """
    df = df.copy()

    # Vectorized per-equipment deviation calculation
    for equipment, baseline in baselines.items():
        mask = df['equipment'] == equipment
        df.loc[mask, 'current_deviation_pct'] = (
            (df.loc[mask, 'current'] - baseline['current']) / baseline['current']
        ) * 100
        df.loc[mask, 'temp_deviation_pct'] = (
            (df.loc[mask, 'temp'] - baseline['temp']) / baseline['temp']
        ) * 100

    return df


def flag_anomalies(
    df: pd.DataFrame,
    current_threshold: float = 15.0,
    temp_threshold: float = 10.0
) -> pd.DataFrame:
    """
    Flag point anomalies where either current or temp deviation exceeds threshold.

    Adds column:
        - is_anomaly (bool)
    """
    df = df.copy()
    df['is_anomaly'] = (
        (df['current_deviation_pct'].abs() > current_threshold) |
        (df['temp_deviation_pct'].abs() > temp_threshold)
    )
    return df


def group_contiguous_blocks(df: pd.DataFrame, max_gap: int = 2) -> pd.DataFrame:
    """
    Group consecutive anomaly points into blocks, tolerating small gaps.

    Algorithm:
    1. Find all anomaly points
    2. Assign block IDs: new block when gap > max_gap
    3. Non-anomaly points get block_id = -1

    Adds column:
        - anomaly_block_id (int, -1 for non-anomaly)
    """
    df = df.copy()
    df = df.sort_values(['equipment', 'timestamp']).reset_index(drop=True)

    df['anomaly_block_id'] = -1  # default: not in anomaly block

    for equipment in df['equipment'].unique():
        mask = df['equipment'] == equipment
        equip_df = df[mask].copy()

        # Find anomaly indices for this equipment
        anomaly_indices = equip_df.index[equip_df['is_anomaly']].tolist()

        if not anomaly_indices:
            continue

        block_id = 0
        current_block = [anomaly_indices[0]]

        for i in range(1, len(anomaly_indices)):
            gap = anomaly_indices[i] - anomaly_indices[i - 1]
            if gap <= max_gap + 1:  # contiguous or within gap tolerance
                current_block.append(anomaly_indices[i])
            else:
                # Assign block ID to current block
                for idx in current_block:
                    df.loc[idx, 'anomaly_block_id'] = block_id
                block_id += 1
                current_block = [anomaly_indices[i]]

        # Don't forget the last block
        for idx in current_block:
            df.loc[idx, 'anomaly_block_id'] = block_id

    return df


def classify_severity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify each anomaly block by severity based on peak deviation.

    Severity rules:
        - Critical: max |current_dev| > 25% OR max |temp_dev| > 20%
        - Warning:  max |current_dev| > 15% OR max |temp_dev| > 10%
        - Normal:   otherwise (shouldn't happen for anomaly blocks)

    Adds column:
        - severity (str: 'Normal', 'Warning', 'Critical')
    """
    df = df.copy()
    df['severity'] = 'Normal'

    # Only classify actual anomaly blocks
    anomaly_blocks = df[df['anomaly_block_id'] >= 0]

    for block_id in anomaly_blocks['anomaly_block_id'].unique():
        block_mask = df['anomaly_block_id'] == block_id
        block_df = df[block_mask]

        max_current_dev = block_df['current_deviation_pct'].abs().max()
        max_temp_dev = block_df['temp_deviation_pct'].abs().max()

        if max_current_dev > 25 or max_temp_dev > 20:
            severity = 'Critical'
        elif max_current_dev > 15 or max_temp_dev > 10:
            severity = 'Warning'
        else:
            severity = 'Normal'

        df.loc[block_mask, 'severity'] = severity

    return df


def run_detection(
    df: pd.DataFrame,
    healthy_fraction: float = 0.8,
    current_threshold: float = 15.0,
    temp_threshold: float = 10.0,
    max_gap: int = 2
) -> Tuple[pd.DataFrame, Dict[str, Dict[str, float]]]:
    """
    Main entry point: run full detection pipeline.

    Args:
        df: Raw sensor DataFrame (must have equipment, timestamp, current, temp)
        healthy_fraction: Fraction of data to use for baseline (default 0.8)
        current_threshold: Current deviation % to flag anomaly (default 15%)
        temp_threshold: Temp deviation % to flag anomaly (default 10%)
        max_gap: Max gap between anomaly points to merge into same block (default 2)

    Returns:
        Tuple of (enriched_df, baselines_dict)
    """
    # Step 1: Compute stable baselines from healthy period
    baselines = compute_stable_baselines(df, healthy_fraction)

    # Step 2: Calculate deviations against stable baselines
    df = calculate_deviations(df, baselines)

    # Step 3: Flag point anomalies
    df = flag_anomalies(df, current_threshold, temp_threshold)

    # Step 4: Group into contiguous blocks
    df = group_contiguous_blocks(df, max_gap)

    # Step 5: Classify block severity
    df = classify_severity(df)

    return df, baselines


# ─────────────────────────────────────────────
# CLI / Testing Entry Point
# ─────────────────────────────────────────────
if __name__ == '__main__':
    import os

    # Load the processed data (or raw CSV)
    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(src_dir)
    data_dir = os.path.join(project_root, 'data')
    csv_path = os.path.join(data_dir, 'simulated_readings.csv')

    print("Loading data...")
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows, {df['equipment'].nunique()} machines")

    print("\nRunning anomaly detection...")
    enriched_df, baselines = run_detection(df)

    # Print baselines
    print("\nStable Baselines (from first 80% healthy data):")
    for equip, base in baselines.items():
        print(f"  {equip}: current={base['current']:.2f}A, temp={base['temp']:.1f}°C")

    # Print anomaly summary
    anomalies = enriched_df[enriched_df['is_anomaly']]
    print(f"\nPoint anomalies detected: {len(anomalies)} / {len(enriched_df)} ({len(anomalies)/len(enriched_df)*100:.1f}%)")

    # Print block summary
    blocks = enriched_df[enriched_df['anomaly_block_id'] >= 0]
    if len(blocks) > 0:
        print(f"\nAnomaly blocks found: {blocks['anomaly_block_id'].nunique()}")
        for block_id in sorted(blocks['anomaly_block_id'].unique()):
            block = blocks[blocks['anomaly_block_id'] == block_id]
            equip = block['equipment'].iloc[0]
            start = block['timestamp'].min()
            end = block['timestamp'].max()
            severity = block['severity'].iloc[0]
            max_curr_dev = block['current_deviation_pct'].abs().max()
            max_temp_dev = block['temp_deviation_pct'].abs().max()
            print(f"  Block {block_id}: {equip} | {start} → {end} | {severity} | "
                  f"max current dev: {max_curr_dev:.1f}% | max temp dev: {max_temp_dev:.1f}%")
    else:
        print("\nNo anomaly blocks found.")
# EquipWatch — Industrial Equipment Health Monitoring System

A production-style, end-to-end predictive maintenance pipeline that simulates industrial sensor data, detects anomalies, stores results in a PostgreSQL database, exposes a REST API, and visualises equipment health through a live Power BI dashboard.

---

## Problem Statement

Unplanned equipment failure is one of the most costly problems in industrial operations. A single hour of unplanned downtime on a production line can cost tens of thousands of dollars in lost output, emergency labour, and component damage. Traditional maintenance approaches — either fixed schedules or reactive repair — are either wasteful or too late.

EquipWatch addresses this by continuously monitoring equipment sensor data, establishing normal operating baselines, and flagging deviations before they become failures. It translates raw sensor readings into actionable maintenance decisions in real time.

---

## System Architecture

```
Simulated Sensors
      ↓
Python (pandas + numpy)
Data generation + feature engineering
      ↓
PostgreSQL
Stores all readings, baselines, anomaly flags
      ↓
FastAPI
Receives new readings, returns anomaly status
      ↓
Power BI
Live diagnostic dashboard pulling from PostgreSQL
```

---

## Equipment Monitored

| Equipment | Section | Normal Current (A) | Normal Temp (°C) | Normal Vibration (mm/s) |
|---|---|---|---|---|
| MOTOR_1 | Electrical | 4.5 ± 0.2 | 67.0 ± 1.5 | 2.3 ± 0.15 |
| MOTOR_2 | Electrical | 5.1 ± 0.3 | 72.0 ± 2.0 | 2.8 ± 0.20 |
| PUMP_1 | Mechanical | 3.8 ± 0.15 | 58.0 ± 1.0 | 1.9 ± 0.10 |
| PUMP_2 | Mechanical | 4.2 ± 0.25 | 63.0 ± 1.5 | 2.1 ± 0.12 |
| COMPRESSOR_1 | Mechanical | 6.3 ± 0.4 | 81.0 ± 2.5 | 3.5 ± 0.25 |

---

## Features

- **Sensor Simulation** — Realistic sensor data generation with injected fault patterns for two machines, mimicking real degradation behaviour
- **Feature Engineering** — Rolling baselines, deviation percentages, power calculations, and rule-based status classification
- **Anomaly Detection** — Rolling window baseline comparison with contiguous anomaly block identification, robust to gaps between anomaly periods
- **PostgreSQL Storage** — All readings, engineered features, and anomaly flags persisted in a relational database
- **REST API** — FastAPI endpoints to receive new sensor readings and return real-time anomaly status
- **Diagnostic Charts** — Matplotlib-generated reports showing sensor trends, baseline overlays, and highlighted anomaly zones, exported as PNG for reports
- **Live Dashboard** — Power BI dashboard connected directly to PostgreSQL, showing equipment health status, anomaly history, and section-level summaries

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data generation + processing | Python, pandas, numpy |
| Anomaly detection | Python, pandas (rolling window) |
| Database | PostgreSQL, psycopg2 |
| API | FastAPI, uvicorn |
| Visualisation — charts | Matplotlib |
| Visualisation — dashboard | Power BI |
| Environment management | pip, requirements.txt |

---

## Project Structure

```
equipwatch/
│
├── data/
│   └── simulated_readings.csv       # Raw generated sensor data
│
├── src/
│   ├── simulator.py                 # Sensor data generation
│   ├── processor.py                 # Cleaning + feature engineering
│   ├── detector.py                  # Anomaly detection engine
│   ├── db.py                        # PostgreSQL connection + queries
│   └── api.py                       # FastAPI endpoints
│
├── reports/
│   └── diagnostic_charts/           # Matplotlib PNG outputs
│
├── dashboard/
│   └── equipwatch.pbix              # Power BI dashboard file
│
├── requirements.txt
└── README.md
```

---

## Build Phases

### Phase 1 — Data Simulation
Generate realistic sensor readings for all 5 machines with injected fault patterns. Output saved to CSV and loaded into PostgreSQL.

### Phase 2 — Database Design and Storage
Design and create PostgreSQL schema. Build ingestion pipeline to store all readings and engineered features.

### Phase 3 — Anomaly Detection Engine
Rolling baseline calculation, deviation flagging, and contiguous anomaly block detection across all machines.

### Phase 4 — Diagnostic Reports
Matplotlib charts showing sensor trends, baselines, anomaly zones, and peak annotations. Exported as PNG files for engineering reports.

### Phase 5 — API Layer
FastAPI REST API with endpoints to receive new sensor readings and return anomaly classification in real time.

### Phase 6 — Power BI Dashboard
Live dashboard connected to PostgreSQL showing equipment health index, anomaly history, section summaries, and maintenance priority ranking.

### Phase 7 — Documentation and Packaging
Clean GitHub repository with full README, requirements.txt, and setup instructions.

---

## Database Schema

### Table: `sensor_readings`
| Column | Type | Description |
|---|---|---|
| id | SERIAL PRIMARY KEY | Unique reading ID |
| equipment | VARCHAR | Equipment name |
| section | VARCHAR | Plant section |
| timestamp | TIMESTAMP | Reading datetime |
| current | FLOAT | Current draw in Amps |
| temp | FLOAT | Temperature in °C |
| vibration | FLOAT | Vibration in mm/s |
| current_baseline | FLOAT | 10-reading rolling average of current |
| temp_baseline | FLOAT | 10-reading rolling average of temperature |
| current_deviation_pct | FLOAT | % deviation from current baseline |
| temp_deviation_pct | FLOAT | % deviation from temperature baseline |
| power_kw | FLOAT | Estimated power consumption in kW |
| anomaly | VARCHAR | Anomaly flag — Normal or Anomaly |
| status | VARCHAR | Status classification — Normal, Warning, Critical |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/equipment` | List all monitored equipment |
| GET | `/readings/{equipment}` | Get latest readings for one machine |
| GET | `/anomalies` | Get all current anomaly flags |
| POST | `/readings` | Submit a new sensor reading for processing |

---

## Power BI Dashboard Pages

| Page | Content |
|---|---|
| Overview | Fleet health summary, anomaly count, status distribution |
| Equipment Detail | Per-machine sensor trends over time |
| Anomaly Log | Historical anomaly events with timestamps |
| Section Report | Aggregated health metrics by plant section |

---

## Business Value

| Metric | Impact |
|---|---|
| Anomaly detection lead time | Flags degradation before threshold breach |
| Maintenance prioritisation | Status classification guides which machine to inspect first |
| Downtime reduction | Early warning reduces unplanned failures |
| Data-driven scheduling | Replaces fixed maintenance schedules with condition-based triggers |

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/equipwatch.git
cd equipwatch
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL
Create a database called `equipwatch` in your PostgreSQL instance:
```sql
CREATE DATABASE equipwatch;
```

### 4. Run the simulator
```bash
python src/simulator.py
```

### 5. Run the processor
```bash
python src/processor.py
```

### 6. Start the API
```bash
uvicorn src.api:app --reload
```

### 7. Connect Power BI
Open `dashboard/equipwatch.pbix` and update the PostgreSQL connection string to point to your local instance.

---

## Future Extensions

- Replace simulated data with real Arduino sensor feeds
- Add machine learning anomaly detection using Isolation Forest
- Deploy API to cloud (Railway or Render)
- Add ANSYS simulation baseline for digital twin comparison layer
- Extend to MQTT protocol for real-time streaming

---

## Author

**Erioluwa Akinfisoye**
Mechanical Engineer | Industrial Data Analyst
[GitHub](https://github.com/Eri-akinfisoye) | [LinkedIn](https://www.linkedin.com/in/erioluwa-akinfisoye/)

---

*EquipWatch is designed as a standalone portfolio project with an architecture that supports direct integration with physical sensor hardware, making it adaptable as an academic final year project in industrial monitoring and predictive maintenance.*

# PROJECT_CONTEXT.md
# EquipWatch — Content Agent Brain
# Last updated: 2026-09-28
# Purpose: This file is the persistent memory for the EquipWatch content agent.
# It is fed to the AI model alongside DEVLOG.md to generate LinkedIn posts and progress updates.
# Update this file whenever a major decision, phase change, or milestone occurs.

---

## Who This Is About

**Name:** Ericson Akinfisoye
**Background:** Final-year Mechanical Engineering student at FUTA (Federal University of Technology, Akure), First Class standing. Completed industrial placement at Nigerian Breweries with exposure to maintenance engineering and industrial KPIs.
**Career direction:** Industrial Data Analyst → Industrial/Manufacturing Data Scientist. Leveraging mechanical engineering domain knowledge as a differentiator in the data analytics space.
**GitHub:** https://github.com/Eri-akinfisoye
**Narrative:** "I build data systems that translate industrial equipment behaviour — from simulation to live sensor data — into business decisions."

---

## The One-Sentence Pitch

> "I build data systems that translate industrial equipment behaviour — from simulation to live sensor data — into business decisions."

Use this in every post. It is the through-line.

---

## Target Audience for Posts

- Hiring managers at manufacturing, energy, and industrial companies
- Data analytics recruiters
- Financial sector hiring managers (for TeleGuard-related content)
- Fellow engineering students making the analytics transition
- Industrial IoT and digital twin practitioners

---

## Full Learning and Build Roadmap

### Phase 1 — Analytics Foundation (current)

| Stage | Topic | Status |
|---|---|---|
| 1 | Python Foundations | Done |
| 2 | Pandas | Done |
| 3 | Matplotlib | Done |
| 4 | FYP Pipeline → EquipWatch | In progress |
| 5 | SQL | Pending |
| 6 | Machine Learning (Scikit-learn, Isolation Forest) | Pending |
| 7 | FastAPI | Pending |
| 8 | Deployment (Railway/Render, Docker) | Pending |

### Phase 2 — Simulation Layer

| Stage | Topic | Status |
|---|---|---|
| 9 | ANSYS — thermal/structural analysis | Pending |
| 10 | SolidWorks — lite, geometry only | Optional/situational |

### Phase 3 — Hardware Layer

| Stage | Topic | Status |
|---|---|---|
| 11 | Arduino — simulated sensor data generation | Pending |

---

## Portfolio Projects

### 1. EquipWatch — Industrial Equipment Health Monitoring System
**Status:** In progress — Phase 1 (simulator.py)
**Stack:** Python, pandas, numpy, matplotlib, PostgreSQL, psycopg2, FastAPI, Power BI
**What it does:** End-to-end predictive maintenance pipeline. Simulates sensor data for 5 industrial machines, detects anomalies using rolling baselines, stores results in PostgreSQL, exposes a REST API, and visualises equipment health in a live Power BI dashboard.
**Business value:** Flags equipment degradation before failure, enabling condition-based maintenance instead of reactive repair.
**FYP path:** Swapping `simulate_fleet()` for `read_arduino_serial()` connects the pipeline to real hardware — full FYP-ready with one function change.
**GitHub:** To be published on completion of Phase 1.

### 2. TeleGuard — Financial Fraud Analytics
**Status:** In progress
**Stack:** Python, PostgreSQL, Power BI, XGBoost, Scikit-learn (planned)
**What it does:** Fraud detection pipeline on the IEEE-CIS dataset (590,540 transaction rows). Pattern detection, SQL-based analysis, Power BI monitoring dashboard.
**Business value:** Financial loss prevention, risk reduction, transaction intelligence.
**GitHub:** https://github.com/Eri-akinfisoye

### 3. Dangote KPI Automation (DCP4)
**Status:** Complete — Top 20 National Finalist
**Stack:** Power Apps, Power Automate, SharePoint, Dataverse, Power BI
**What it does:** Automated KPI data entry, validation, escalation, and role-based dashboards for a cement manufacturing plant. 15 daily KPIs across 5 roles.
**GitHub:** https://github.com/Eri-akinfisoye/Dangote-Cement-Digital-KPI-

### 4. NexaLink Churn Analysis
**Status:** Complete
**Stack:** Power BI, DAX
**What it does:** End-to-end churn analysis for a fictional telecom (7,043 customers, 23 variables). 26.5% churn rate identified. Contract type found as strongest churn predictor.

### 5. EquipWatch v2 (planned)
**Status:** Planned — after ML stage
**What it adds:** Replaces rolling baseline anomaly detection with a trained Isolation Forest ML model. Same pipeline, smarter engine.

---

## EquipWatch — Detailed Build Plan

### Architecture
```
Simulated Sensors
      ↓
Python (pandas + numpy) — data generation + feature engineering
      ↓
PostgreSQL — stores all readings, baselines, anomaly flags
      ↓
FastAPI — exposes endpoints to receive data and return anomaly status
      ↓
Power BI — live dashboard pulling from PostgreSQL
```

### Phase Breakdown

| Phase | What gets built | Key files | Status |
|---|---|---|---|
| 1 | Data simulation | src/simulator.py | In progress |
| 2 | Database design + ingestion | src/db.py | Pending |
| 3 | Anomaly detection engine | src/detector.py | Pending |
| 4 | Diagnostic charts | src/reporter.py, reports/ | Pending |
| 5 | REST API | src/api.py | Pending |
| 6 | Power BI dashboard | dashboard/equipwatch.pbix | Pending |
| 7 | GitHub packaging + content agent | content_agent.py, README.md | Pending |

### Equipment Monitored

| Equipment | Section | Fault injected? |
|---|---|---|
| MOTOR_1 | Electrical | Yes |
| MOTOR_2 | Electrical | No |
| PUMP_1 | Mechanical | No |
| PUMP_2 | Mechanical | Yes |
| COMPRESSOR_1 | Mechanical | No |

---

## Key Decisions and Why

| Decision | Reason |
|---|---|
| MATLAB dropped | Python covers everything MATLAB does; job market increasingly prefers Python |
| ANSYS deferred to Phase 2 | Analytics foundation gets Ericson employed faster; ANSYS adds digital twin layer after |
| SolidWorks optional | Only enters if digital twin or CAD-adjacent role is targeted |
| PostgreSQL chosen over SQLite | Production-grade, matches real-world data engineering stacks, already installed |
| Rolling baseline for anomaly detection (v1) | Interpretable, no training data required, directly mirrors real industrial condition monitoring |
| Isolation Forest for v2 | Replaces hardcoded thresholds with learned normality — more robust for real sensor variance |
| FastAPI over Flask | Faster, modern, async-native, better for data API use cases |
| CSV as Phase 1 handoff format | Keeps simulator.py decoupled from database — clean separation of concerns |
| Two fault machines only (MOTOR_1, PUMP_2) | Realistic — not all machines fail simultaneously; makes anomaly detection meaningful |

---

## Decisions Still Open

- Whether to add MQTT streaming layer for real-time sensor feeds
- Whether to deploy on Railway, Render, or AWS depending on cost at time of deployment
- Whether to add a Streamlit dashboard as alternative to Power BI for web accessibility
- Exact ML model selection for EquipWatch v2 (Isolation Forest vs. One-Class SVM)

---

## LinkedIn Post Guidelines

**Format that works:**
```
Hook — one provocative or surprising line

Short context — 2 to 3 sentences

The substance — what was built, learned, or decided
In short punchy lines
Not long paragraphs

Takeaway — one clean closing line

3 to 5 hashtags
```

**Tone:** Confident, human, direct. No corporate speak. No "excited to share." No "humbled by."

**Always include:**
- What was built or learned (specific, not vague)
- Why it matters (business or career angle)
- A visual — screenshot, diagram, or chart
- A link to GitHub when a phase is complete

**Hashtags to rotate:**
#PredictiveMaintenance #DataAnalytics #Python #MechanicalEngineering #EquipWatch #IndustrialData #DigitalTwin #PostgreSQL #FastAPI #PowerBI #MachineLearning #PortfolioProject

---

## Content Agent Instructions (for when content_agent.py is built)

When generating a LinkedIn post:
1. Read the most recent entry in DEVLOG.md
2. Read the current phase status from this file
3. Frame the post around what was built and why it matters — not just what was done
4. Suggest one visual: screenshot, chart, or diagram
5. Keep the post under 1,300 characters — LinkedIn optimal length
6. End with 3 to 5 relevant hashtags from the list above
7. Output: draft post text + suggested visual description + suggested code snippet if relevant

---

## DEVLOG Location

`equipwatch/DEVLOG.md` — updated after every task set completion.

---
*This file is living documentation. Update it at every phase transition, major decision, or significant change to the project plan.*

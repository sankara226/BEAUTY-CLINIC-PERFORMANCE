# Premium Beauty Clinic Analytics & Time-Series Revenue Forecasting

A modular, production-ready data engineering and business intelligence pipeline designed to ingest, process, and forecast longitudinal customer transactions from a high-end aesthetics clinic (2023–2026). The pipeline distinguishes between high-frequency skincare routines and high-value clinical interventions (e.g., fillers/neuromodulators) to compute robust customer lifetime value metrics and model revenue trajectories.

## Features & Analytical Capabilities

- **Normalizing Normalization Pipeline:** Maps raw tracking streams dynamically into clean SQL dimensions (`Customers`, `Products`, `Transactions`).
- **Advanced Cohort Metric Analysis:** Extracts Repeat Purchase Factors and individual Customer Lifetime Value indices via native relational queries.
- **Predictive Run-Rate Projections:** Uses cycles of trend-based linear regressions to outline operational earnings 12 months into the future.

## Setup & Local Deployment

### 1. Provision Environments Package Modules

```bash
pip install -r requirements.txt
```

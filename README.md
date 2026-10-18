# Agentic AI for Fleet Insights

A locally runnable Full Stack AI demo with a React dashboard, FastAPI backend, seven specialist agents/tools, and persistent insight history. It runs in **demo mode without cloud credentials**. Optional Google Cloud BigQuery integration is included for users who configure credentials and a dataset.

## What it does

- Explore sample fleet and vehicle data.
- Ask questions such as: "Which customers have the highest maintenance risk?" or "Summarize fleet replacement opportunities."
- Routes questions through a lightweight multi-agent workflow: Fleet Overview, Customer Insights, Vehicle Health, Maintenance, Replacement, Recommendations, and Critic.
- Saves generated insight reports to a local SQLite database.
- Optionally writes reports to BigQuery.
- Displays tool/agent execution traces in the React UI.

> This is a portfolio-ready starter/demo, not a claim that it is a production deployment. The default agents use transparent rule-based analysis so it works immediately without paid API keys. Google ADK integration is documented as an extension point; the current workflow is implemented locally to keep setup simple and reliable.

## Architecture

```text
React + Vite UI (localhost:5173)
        |
        | HTTP / REST
        v
FastAPI API (localhost:8000)
  ├── Fleet data service (sample data or BigQuery)
  ├── 7 specialist agent/tool functions
  ├── Critic/quality check
  └── SQLite persistence
        |
        └── Optional BigQuery report persistence
```

## Requirements

- Python 3.10+
- Node.js 18+ and npm
- Git (optional, for GitHub upload)

## Run locally

### 1. Start the backend

Open a terminal in the project folder:

```bash
cd backend
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install packages and start API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs  
Health check: http://127.0.0.1:8000/health

### 2. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually http://localhost:5173.

## Optional BigQuery setup

The project works without BigQuery. To enable it:

1. Create a Google Cloud project and enable the BigQuery API.
2. Create a dataset and a table named `fleet_vehicles` with fields matching the sample schema:
   `vehicle_id STRING, customer_id STRING, make STRING, model STRING, model_year INT64, mileage INT64, maintenance_cost FLOAT64, days_since_service INT64, risk_score FLOAT64, replacement_candidate BOOL`
3. Set up Application Default Credentials:
   ```bash
   gcloud auth application-default login
   ```
4. Copy `backend/.env.example` to `backend/.env` and set:
   ```env
   DATA_SOURCE=bigquery
   GCP_PROJECT_ID=your-gcp-project-id
   BIGQUERY_DATASET=your_dataset
   BIGQUERY_VEHICLE_TABLE=fleet_vehicles
   BIGQUERY_REPORTS_TABLE=fleet_insight_reports
   ```
5. Ensure the account has permission to query the table and create/insert into the reports table. The app attempts to create the report table if it doesn't exist.

Do not commit credentials, service-account JSON files, or `.env` to GitHub.

## Example questions

- Which customers have the highest maintenance risk?
- Which vehicles should be considered for replacement?
- Summarize the fleet's maintenance status.
- What actions should the fleet manager prioritize?
- Give me a customer and vehicle insight summary.

## API endpoints

- `GET /health` — service status
- `GET /api/fleet/summary` — summary metrics
- `GET /api/fleet/vehicles` — fleet vehicle list
- `POST /api/insights` — run the agent workflow and persist the report
- `GET /api/insights/history` — previously saved reports

## GitHub upload

From the project root:

```bash
git init
git add .
git commit -m "Build Agentic AI Fleet Insights app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agentic-ai-fleet-insights.git
git push -u origin main
```

Before uploading, verify `.env`, credentials, or customer/company data are not included. The included `.gitignore` excludes them.

## Notes for extending

- Replace the rule-based agent functions in `backend/app/agents.py` with Google ADK agents and model-backed tools.
- Add authentication and authorization before exposing the API publicly.
- Use a real fleet dataset only when you have permission to use it.
- Add tests and deployment automation before describing it as production-ready.

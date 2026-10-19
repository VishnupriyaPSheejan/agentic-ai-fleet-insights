# Agentic AI for Fleet Insights

Full-stack demo: React/Vite frontend, FastAPI backend, seven fleet-analysis agents/tools, SQLite report history, optional BigQuery input, Docker Compose, backend tests, and GitHub Actions CI.

**Default mode uses synthetic sample data and works without cloud credentials or LLM API keys.** Agent functions currently perform deterministic Python analysis; Google ADK/LLM execution is not wired in yet.

## Quick start (Docker)
1. Install and open Docker Desktop.
2. Extract this project.
3. Open a terminal in this folder and run:
   ```bash
   docker compose up --build
   ```
4. Open http://localhost:5173 (dashboard), http://localhost:8000/docs (API docs).
5. Stop with `Ctrl+C`, then run `docker compose down`.

## Run without Docker
Backend terminal:
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```
Frontend terminal, from project root:
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

## Included
- React dashboard with fleet metrics, question submission, agent traces, vehicle explorer and report history
- FastAPI endpoints and SQLite persistence
- Seven analysis functions: Fleet Overview, Customer Insights, Vehicle Health, Maintenance, Replacement, Recommendations, Critic
- Optional BigQuery vehicle table reader
- Dockerfiles for frontend/backend and Docker Compose
- GitHub Actions CI for pytest and frontend production build

## Optional BigQuery
Create a table with `vehicle_id STRING, customer_id STRING, make STRING, model STRING, model_year INT64, mileage INT64, maintenance_cost FLOAT64, days_since_service INT64, risk_score FLOAT64, replacement_candidate BOOL`. Configure `DATA_SOURCE=bigquery`, `GCP_PROJECT_ID`, `BIGQUERY_DATASET`, and `BIGQUERY_VEHICLE_TABLE` in `backend/.env`. Authenticate with `gcloud auth application-default login`. Do not commit `.env` or credentials. Docker Compose defaults to demo mode.

## CI/CD scope
`.github/workflows/ci.yml` runs backend tests and frontend build on pushes and pull requests. This is continuous integration, not cloud deployment. A deployment workflow requires a chosen hosting platform and secrets.

## GitHub Desktop
Create an empty GitHub repository, then add this extracted folder in GitHub Desktop and commit/publish it. Alternatively:
```bash
git init
git add .
git commit -m "Add Fleet Insights full-stack app with Docker and CI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agentic-ai-fleet-insights.git
git push -u origin main
```

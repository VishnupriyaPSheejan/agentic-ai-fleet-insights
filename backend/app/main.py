from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .data import get_vehicles
from .agents import run_workflow
from .storage import save_report, list_reports
app=FastAPI(title="Agentic AI for Fleet Insights API",version="1.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_methods=["*"],allow_headers=["*"])
class InsightRequest(BaseModel):
    question:str=Field(min_length=3,max_length=1000)
@app.get("/health")
def health(): return {"status":"ok","service":"agentic-ai-fleet-insights"}
@app.get("/api/fleet/summary")
def summary():
    try: vs=get_vehicles()
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))
    n=len(vs)
    return {"total_vehicles":n,"customers":len({v["customer_id"] for v in vs}),"high_risk_vehicles":sum(v["risk_score"]>=.75 for v in vs),"replacement_candidates":sum(bool(v["replacement_candidate"]) for v in vs),"average_risk":round(sum(v["risk_score"] for v in vs)/n,2) if n else 0}
@app.get("/api/fleet/vehicles")
def vehicles():
    try: return get_vehicles()
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))
@app.post("/api/insights")
def insights(req:InsightRequest):
    try: return save_report(run_workflow(req.question,get_vehicles()))
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))
@app.get("/api/insights/history")
def history(limit:int=20): return list_reports(max(1,min(limit,100)))

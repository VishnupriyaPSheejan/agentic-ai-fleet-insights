from fastapi.testclient import TestClient
from app.main import app
def test_health():
    with TestClient(app) as c: r=c.get("/health")
    assert r.status_code==200 and r.json()["status"]=="ok"
def test_summary_has_sample_vehicles():
    with TestClient(app) as c: r=c.get("/api/fleet/summary")
    assert r.status_code==200 and r.json()["total_vehicles"]==10
def test_vehicle_list():
    with TestClient(app) as c: r=c.get("/api/fleet/vehicles")
    assert r.status_code==200 and len(r.json())==10
def test_insights_return_seven_agents(tmp_path,monkeypatch):
    import app.storage as storage
    monkeypatch.setattr(storage,"DB_PATH",str(tmp_path/"test.db"))
    with TestClient(app) as c: r=c.post("/api/insights",json={"question":"Which vehicles are high risk?"})
    assert r.status_code==200 and r.json()["agent_count"]==7
def test_short_question_rejected():
    with TestClient(app) as c: r=c.post("/api/insights",json={"question":"?"})
    assert r.status_code==422

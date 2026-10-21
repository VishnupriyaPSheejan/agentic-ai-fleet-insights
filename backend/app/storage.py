import json, os, sqlite3
from datetime import datetime, timezone
DB_PATH=os.getenv("DATABASE_PATH","./fleet_insights.db")
def connect():
    parent=os.path.dirname(DB_PATH)
    if parent: os.makedirs(parent,exist_ok=True)
    c=sqlite3.connect(DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT,question TEXT,title TEXT,summary TEXT,payload_json TEXT)")
    c.commit()
    return c
def save_report(report):
    now=datetime.now(timezone.utc).isoformat()
    payload={**report,"created_at":now}
    c=connect()
    cur=c.execute("INSERT INTO reports(created_at,question,title,summary,payload_json) VALUES(?,?,?,?,?)",(now,report["question"],report["title"],report["summary"],json.dumps(payload)))
    c.commit(); payload["id"]=cur.lastrowid; c.close()
    return payload
def list_reports(limit=20):
    c=connect(); rows=c.execute("SELECT id,payload_json FROM reports ORDER BY id DESC LIMIT ?",(limit,)).fetchall(); c.close()
    out=[]
    for i,raw in rows:
        x=json.loads(raw); x["id"]=i; out.append(x)
    return out

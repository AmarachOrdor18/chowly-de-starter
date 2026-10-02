"""
Reference analytics API for the Chowly manager dashboard (Python / FastAPI).
Your own app may use Node, Django, whatever. Port the idea, not the code (ask your AI tool to help, and log it).

The API reads ONLY from the Fabric Gold layer through the Warehouse SQL endpoint, with a read-only service principal.
The browser never talks to Fabric. Secrets live in environment variables, never in git.

Run:  pip install fastapi uvicorn pyodbc python-dotenv
      uvicorn main:app --reload
Needs the Microsoft ODBC Driver 18 for SQL Server installed on the machine that runs the API.
"""
import os
import time

import pyodbc
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()
app = FastAPI(title="Chowly analytics")

CONN_STR = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={os.environ['FABRIC_SQL_ENDPOINT']};"       # copy from the Warehouse settings in Fabric
    f"Database={os.environ['FABRIC_WAREHOUSE']};"
    "Authentication=ActiveDirectoryServicePrincipal;"
    f"UID={os.environ['AZURE_CLIENT_ID']};PWD={os.environ['AZURE_CLIENT_SECRET']};"
    "Encrypt=yes;TrustServerCertificate=no;"
)
_cache: dict = {}


def query(sql: str, params: tuple = (), ttl: int = 60):
    """Small cache so 50 dashboard refreshes do not become 50 warehouse queries."""
    key = (sql, params)
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < ttl:
        return hit[1]
    try:
        with pyodbc.connect(CONN_STR, timeout=30) as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            cols = [c[0] for c in cur.description]
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    except pyodbc.Error as e:
        raise HTTPException(status_code=503, detail="Analytics store unavailable") from e
    _cache[key] = (time.time(), rows)
    return rows


@app.get("/api/analytics/revenue-by-day")
def revenue_by_day():
    return query("""
        SELECT d.full_date, SUM(f.order_total) AS revenue, COUNT(*) AS orders
        FROM gold.fact_order f JOIN gold.dim_date d ON d.date_key = f.date_key
        GROUP BY d.full_date ORDER BY d.full_date""")


@app.get("/api/analytics/wait-time-by-chef")
def wait_time_by_chef():
    return query("""
        SELECT s.full_name AS chef, AVG(f.est_wait_min * 1.0) AS avg_estimated,
               AVG(f.actual_wait_min) AS avg_actual, AVG(CASE WHEN f.is_delayed = 1 THEN 1.0 ELSE 0 END) AS delayed_share
        FROM gold.fact_order f JOIN gold.dim_staff s ON s.staff_key = f.chef_key
        GROUP BY s.full_name ORDER BY avg_actual DESC""")


@app.get("/api/analytics/complaints-vs-delay")
def complaints_vs_delay():
    return query("""
        SELECT CASE WHEN c.was_delayed = 1 THEN 'delayed' ELSE 'on time' END AS bucket,
               COUNT(*) AS complaints, AVG(c.rating * 1.0) AS avg_rating
        FROM gold.fact_complaint c GROUP BY CASE WHEN c.was_delayed = 1 THEN 'delayed' ELSE 'on time' END""")


@app.get("/api/analytics/data-health")
def data_health():
    """The panel that makes quality and governance visible to a non-technical manager."""
    # Start with the watermark table. In Lab 5 you extend this with a gold.dq_log table (rows loaded, rows rejected).
    return query("SELECT table_name, last_loaded_at FROM gold.etl_watermark")

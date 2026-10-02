"""
Load the sample history into your OWN source systems, so Fabric has real databases to ingest from.

  Postgres : menu_items, menu_price_history, staff, orders, order_items, payments
  MongoDB  : complaints, order_events

Set connection strings in a .env file (see .env.example). Run:
  pip install -r requirements.txt
  python load_sources.py --data ../sample_data
Create the Postgres schema first: run app_changes/reference_schema.postgres.sql in your Postgres.
"""
import argparse
import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient

TABLES = {
    "staff": ("staff.csv", "staff_id, full_name, role, is_active, updated_at"),
    "menu_items": ("menu_items.csv", "item_id, name, category, price, prep_minutes, is_active, updated_at"),
    "menu_price_history": ("menu_price_history.csv", "item_id, price, valid_from, valid_to"),
    "orders": ("orders.csv", "order_id, table_no, waiter_id, chef_id, bartender_id, status, placed_at, served_at, paid_at, estimated_wait_min, updated_at"),
    "order_items": ("order_items.csv", "order_item_id, order_id, item_id, quantity, unit_price, est_prep_minutes, updated_at"),
    "payments": ("payments.csv", "payment_id, order_id, amount, method, is_simulated, paid_at, updated_at"),
}


def load_postgres(data: Path):
    conn = psycopg2.connect(os.environ["POSTGRES_DSN"])
    cur = conn.cursor()
    for table, (fname, cols) in TABLES.items():
        cur.execute(f"TRUNCATE chowly.{table} CASCADE" if table in ("staff", "menu_items") else f"TRUNCATE chowly.{table}")
    conn.commit()
    for table, (fname, cols) in TABLES.items():          # order matters: parents first
        with open(data / fname, encoding="utf-8") as f:
            cur.copy_expert(f"COPY chowly.{table} ({cols}) FROM STDIN WITH (FORMAT csv, HEADER true)", f)
        conn.commit()
        cur.execute(f"SELECT count(*) FROM chowly.{table}")
        print(f"postgres chowly.{table}: {cur.fetchone()[0]} rows")
    conn.close()


def load_mongo(data: Path):
    client = MongoClient(os.environ["MONGO_URI"])
    db = client[os.environ.get("MONGO_DB", "chowly")]
    for coll, fname in (("complaints", "complaints.jsonl"), ("order_events", "order_events.jsonl")):
        docs = [json.loads(line) for line in open(data / fname, encoding="utf-8")]
        db[coll].drop()
        db[coll].insert_many(docs)
        print(f"mongo {coll}: {db[coll].count_documents({})} documents")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="../sample_data")
    ap.add_argument("--only", choices=["postgres", "mongo"])
    a = ap.parse_args()
    load_dotenv()
    data = Path(a.data)
    if a.only in (None, "postgres"):
        load_postgres(data)
    if a.only in (None, "mongo"):
        load_mongo(data)

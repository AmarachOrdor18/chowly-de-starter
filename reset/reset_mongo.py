"""Drops the course collections. Reload with: python data_generator/load_sources.py --only mongo"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
db = MongoClient(os.environ["MONGO_URI"])[os.environ.get("MONGO_DB", "chowly")]
answer = input(f"Drop complaints and order_events in database '{db.name}'? Type yes: ")
if answer.strip().lower() == "yes":
    for c in ("complaints", "order_events"):
        db[c].drop()
        print("dropped", c)
else:
    print("cancelled")

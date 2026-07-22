"""
Run this once to populate MongoDB with the portfolio content.

Usage:
    python seed_db.py
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app import FALLBACK  # reuse the same content defined in app.py

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "poonam_portfolio")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

COLLECTIONS = ["experience", "projects", "skills", "education", "stats"]

def seed():
    for name in COLLECTIONS:
        col = db[name]
        col.delete_many({}) 
        docs = FALLBACK[name]
        if docs:
            col.insert_many(docs)
        print(f"Seeded '{name}': {len(docs)} document(s)")

    # make sure the contact messages collection exists (created lazily otherwise)
    if "messages" not in db.list_collection_names():
        db.create_collection("messages")
        print("Created empty 'messages' collection")

    print("\nDone. Collections in database:", db.list_collection_names())

if __name__ == "__main__":
    seed()
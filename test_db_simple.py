import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if db_url:
    print(f"DATABASE_URL found.")
    print(f"Starts with: {db_url[:20]}...")
    print(f"Contains 'sslmode=require': {'sslmode=require' in db_url}")
else:
    print("DATABASE_URL NOT FOUND")

import psycopg2
try:
    print("Attempting basic psycopg2 connection...")
    conn = psycopg2.connect(db_url, connect_timeout=5)
    print("✅ Basic Connection Success!")
    conn.close()
except Exception as e:
    print(f"❌ Basic Connection Failed: {e}")

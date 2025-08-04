#!/usr/bin/env python3

import sqlite3
import os

def check_database(db_name):
    if not os.path.exists(db_name):
        print(f"{db_name}: Does not exist")
        return
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"{db_name}: {[t[0] for t in tables]}")
        
        # Check size
        size = os.path.getsize(db_name)
        print(f"  Size: {size} bytes")
        conn.close()
    except Exception as e:
        print(f"{db_name}: Error - {e}")

if __name__ == "__main__":
    check_database('client_management.db')
    check_database('webapi_starter.db')

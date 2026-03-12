"""T002/T003: 嘗試連接 CMoney資料 並搜尋 stock_events / stock_daily"""
from src.db.connection import get_connection
import os

# Try different databases
target_dbs = ['CMoney資料', 'D_衍生資料', 'BVL策略研究', 'finlab', 'TEST', '安杰測試']

conn = get_connection()
cursor = conn.cursor()

results = {}

for db in target_dbs:
    try:
        # Try to USE database
        cursor.execute(f"USE [{db}]")
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME")
        tables = [r[0] for r in cursor.fetchall()]
        results[db] = tables
        print(f"=== {db} Tables ===")
        for t in tables:
            print(f"  {t}")
        # Reset back
        cursor.execute(f"USE [股價即時]")
    except Exception as e:
        results[db] = f"ERROR: {str(e)[:120]}"
        print(f"=== {db}: SKIP ({str(e)[:80]})")

# Write to file
with open('_tmp_other_dbs.txt', 'w', encoding='utf-8') as f:
    for db, val in results.items():
        f.write(f"\n=== {db} ===\n")
        if isinstance(val, list):
            for t in val:
                f.write(f"  {t}\n")
        else:
            f.write(f"  {val}\n")

conn.close()
print("\nResults written to _tmp_other_dbs.txt")

"""臨時腳本：確認 DB 資料表名稱與欄位（T002/T003）"""
from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

# 列出所有資料表
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME")
rows = cursor.fetchall()
print("=== Tables ===")
for r in rows:
    print(" ", r[0])

# 嘗試幾個可能的事件表名稱
event_candidates = ["stock_events", "StockEvents", "events", "Events", "strategy_events"]
for t in event_candidates:
    try:
        cursor.execute(f"SELECT TOP 1 * FROM [{t}]")
        cols = [col[0] for col in cursor.description]
        print(f"\n=== {t} columns ===")
        print(cols)
        row = cursor.fetchone()
        if row:
            print("  Sample:", dict(zip(cols, row)))
    except Exception as e:
        pass  # table doesn't exist

# 嘗試幾個可能的日 K 線表名稱
daily_candidates = ["stock_daily", "StockDaily", "daily", "日K", "日線"]
for t in daily_candidates:
    try:
        cursor.execute(f"SELECT TOP 1 * FROM [{t}]")
        cols = [col[0] for col in cursor.description]
        print(f"\n=== {t} columns ===")
        print(cols)
        row = cursor.fetchone()
        if row:
            print("  Sample:", dict(zip(cols, row)))
    except Exception as e:
        pass  # table doesn't exist

conn.close()

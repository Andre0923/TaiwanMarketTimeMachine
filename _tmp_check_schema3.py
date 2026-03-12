"""T002/T003: 搜尋所有 DB 中含 event 或 daily 的表，以及列出所有 DB 名稱（UTF-8 輸出）"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

# 列出所有使用者資料庫
cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4 ORDER BY name")
dbs = [r[0] for r in cursor.fetchall()]
print("=== Available Databases ===")
for d in dbs:
    print(f"  [{d}]")

# 在各 DB 中搜尋包含 stock_events / stock_daily 字樣的資料表
keywords = ['event', 'daily', 'stock', '事件', '日線', '日K']
print("\n=== Searching for event/daily tables in all databases ===")
for db in dbs:
    try:
        q = f"SELECT '{db}' as db, TABLE_SCHEMA, TABLE_NAME FROM [{db}].INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
        cursor.execute(q)
        rows = cursor.fetchall()
        for r in rows:
            name_lower = r[2].lower()
            if any(k.lower() in name_lower for k in keywords):
                print(f"  FOUND: {r[0]}.{r[1]}.{r[2]}")
    except Exception as e:
        print(f"  SKIP {db}: {str(e)[:60]}")

# 查看 1分K 欄位（確認日期與代號欄名）
cursor.execute("SELECT TOP 1 * FROM [股價即時].[dbo].[1分K]")
cols = [col[0] for col in cursor.description]
row = cursor.fetchone()
print(f"\n=== 股價即時.dbo.1分K columns ===")
print(cols)
if row:
    d = dict(zip(cols, row))
    for k, v in list(d.items())[:8]:
        print(f"  {k}: {v}")

conn.close()
print("\nDone.")

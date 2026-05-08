"""T002/T003: 確認所有資料庫與資料表"""
from src.db.connection import get_connection
import os

conn = get_connection()
cursor = conn.cursor()

# 列出所有資料庫
cursor.execute("SELECT name FROM sys.databases WHERE name NOT IN ('master','tempdb','model','msdb') ORDER BY name")
dbs = [r[0] for r in cursor.fetchall()]
print("=== Available Databases ===")
for d in dbs:
    print(f"  {d}")

# 在當前 DB 中尋找包含 event 或 daily 關鍵字的表
cursor.execute("""
    SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE='BASE TABLE' 
    ORDER BY TABLE_NAME
""")
tables = cursor.fetchall()
print(f"\n=== Tables in current DB ({os.getenv('DB_DATABASE', '?')}) ===")
for t in tables:
    print(f"  {t[0]}.{t[1]}.{t[2]}")

# 查看 1分K 表的欄位（作為對照）
cursor.execute("SELECT TOP 1 * FROM [1分K]")
cols = [col[0] for col in cursor.description]
row = cursor.fetchone()
print(f"\n=== 1分K columns ===")
print(cols)
if row:
    print("  Sample row keys:", list(zip(cols, row))[:5], "...")

conn.close()
print("\nDone.")

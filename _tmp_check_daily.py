"""T002/T003: 確認 CMoney資料.日收盤行情 欄位與 stock_events 存在性"""
from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("USE [CMoney資料]")

# 日收盤行情 columns
cursor.execute("SELECT TOP 1 * FROM [日收盤行情]")
cols = [col[0] for col in cursor.description]
row = cursor.fetchone()

with open('_tmp_daily_schema.txt', 'w', encoding='utf-8') as f:
    f.write("=== CMoney資料.dbo.日收盤行情 columns ===\n")
    f.write(str(cols) + "\n\n")
    if row:
        f.write("Sample row:\n")
        for k, v in zip(cols, row):
            f.write(f"  {k}: {v!r}\n")

# 日收盤還原
cursor.execute("SELECT TOP 1 * FROM [日收盤還原]")
cols2 = [col[0] for col in cursor.description]
row2 = cursor.fetchone()
with open('_tmp_daily_schema.txt', 'a', encoding='utf-8') as f:
    f.write("\n=== CMoney資料.dbo.日收盤還原 columns ===\n")
    f.write(str(cols2) + "\n\n")
    if row2:
        f.write("Sample row:\n")
        for k, v in zip(cols2, row2):
            f.write(f"  {k}: {v!r}\n")

conn.close()
print("Done - see _tmp_daily_schema.txt")

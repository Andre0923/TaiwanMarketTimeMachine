"""T002/T003: Search all DBs for event/daily tables - ASCII-safe output"""
from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

# Show all databases (repr for safe ASCII output)
cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4 ORDER BY name")
dbs = [r[0] for r in cursor.fetchall()]
print("=== Available Databases ===")
for d in dbs:
    print(f"  {repr(d)}")

# Search each DB for event/daily tables
keywords = ['event', 'daily', 'stock', '\u4e8b\u4ef6', '\u65e5\u7dda', '\u65e5K']
print("\n=== Tables containing event/daily/stock keywords ===")
for db in dbs:
    try:
        q = f"SELECT TABLE_NAME FROM [{db}].INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME"
        cursor.execute(q)
        rows = cursor.fetchall()
        for r in rows:
            table = r[0]
            if any(k.lower() in table.lower() for k in keywords):
                print(f"  MATCH: [{db}].[dbo].[{table}]")
    except Exception as e:
        print(f"  SKIP {repr(db)}: {str(e)[:80]}")

# Show 1分K column names
cursor.execute("SELECT TOP 1 * FROM [1\u5206K]")
cols = [col[0] for col in cursor.description]
row = cursor.fetchone()
print(f"\n=== 1\u5206K columns (repr) ===")
print([repr(c) for c in cols])

# Write results to file for readability
with open('_tmp_schema_result.txt', 'w', encoding='utf-8') as f:
    f.write("=== Available Databases ===\n")
    for d in dbs:
        f.write(f"  {d}\n")
    f.write(f"\n=== 1\u5206K columns ===\n")
    f.write(str(cols) + "\n")
    if row:
        d_row = dict(zip(cols, row))
        for k, v in d_row.items():
            f.write(f"  {k}: {v}\n")

conn.close()
print("\nResults also written to _tmp_schema_result.txt")

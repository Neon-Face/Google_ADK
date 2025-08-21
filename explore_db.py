# import sqlite3

# db_path = "ripencc_agent/data/insights.db"

# conn = sqlite3.connect(db_path)
# cur = conn.cursor()

# SQL = "SELECT name FROM sqlite_master WHERE type='table';"
# cur.execute(SQL)

# tables = [row[0] for row in cur.fetchall()]
# print("Tables:", tables)

# conn.close()

import sqlite3

db_path = "ripencc_agent/data/insights.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

table_name = "Country_IPv6_Adoption"

cur.execute(f"PRAGMA table_info({table_name});")
columns = [row[1] for row in cur.fetchall()]

print(f"Columns in {table_name}:", columns)

conn.close()

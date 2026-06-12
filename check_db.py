import sqlite3
conn = sqlite3.connect('P:/bluestock_mf_capstone/data/db/bluestock_mf.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', len(tables))
for t in tables:
    print(' -', t[0])
conn.close()

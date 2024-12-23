import pandas as pd
import sqlite3

conn = sqlite3.connect('routes.db')
df = pd.read_sql("SELECT * FROM routes;", conn)
conn.close()

print(df)
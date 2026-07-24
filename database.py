import sqlite3

conn = sqlite3.connect("jobs.db")

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS jobs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
link TEXT UNIQUE
)
""")

conn.commit()

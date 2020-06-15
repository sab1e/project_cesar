import sqlite3

conn = sqlite3.connect('projects_data.sqlite')
cur = conn.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
conn.close()

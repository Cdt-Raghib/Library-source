import sqlite3

conn = sqlite3.connect('assets/databases/library.db')

cursor = conn.cursor()
cursor.row_factory = sqlite3.Row

cursor.execute('ALTER TABLE books ADD COLUMN comments TEXT')
conn.commit()
conn.close()
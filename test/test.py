import sqlite3

conn = sqlite3.connect('assets/databases/library.db')

cursor = conn.cursor()
cursor.row_factory = sqlite3.Row
# fetched = cursor.execute('SELECT * FROM transactions').fetchall()
# for f in fetched:
#     title = cursor.execute('SELECT title FROM books WHERE book_no=?', (f['book_no'],)).fetchone()
#     cursor.execute('UPDATE transactions SET title=? WHERE book_no=?', (title['title'], int(f['book_no'])))

x = cursor.execute('SELECT * FROM transactions').fetchall()
for f in x:
    print(dict(f))
# cmd = '''
# ALTER TABLE transactions ADD column title TEXT REFERENCES books(title)
# '''
# cursor.execute(cmd)
conn.commit()
conn.close()
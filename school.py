import sqlite3
conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    klass TEXT
)
''')

conn.commit()
conn.close()

print("База данных и таблица успешно созданы.")
import sqlite3
from config import DATABASE_FILE

class Database:
    def __init__(self, db_file=DATABASE_FILE):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS teachers
                     (id INTEGER PRIMARY KEY, name TEXT UNIQUE)""")
        c.execute("""CREATE TABLE IF NOT EXISTS subjects
                     (id INTEGER PRIMARY KEY, name TEXT UNIQUE)""")
        c.execute("""CREATE TABLE IF NOT EXISTS classrooms
                     (number INTEGER PRIMARY KEY, capacity INTEGER)""")
        c.execute("""CREATE TABLE IF NOT EXISTS schedule
                     (id INTEGER PRIMARY KEY, subject_id INTEGER, teacher_id INTEGER, classroom_number INTEGER, date TEXT, deleted INTEGER DEFAULT 0, FOREIGN KEY(subject_id) REFERENCES subjects(id), FOREIGN KEY(teacher_id) REFERENCES teachers(id), FOREIGN KEY(classroom_number) REFERENCES classrooms(number))""")
        self.conn.commit()

    def close(self):
        self.conn.close()
import sqlite3

from datetime import date
from config import MAX_LESSONS_PER_DAY
from .schedule_item import ScheduleItem

class Schedule:
    def __init__(self, database):
        self.db = database

    # Добавление учителя
    
    def add_teacher(self, name):
        c = self.db.conn.cursor()

        try:
            c.execute("INSERT INTO teachers (name) VALUES (?)", (name,))
            self.db.conn.commit()

        except sqlite3.IntegrityError:
            print(f"Учитель с именем «{name}» уже существует в базе данных.")

        else:
            print(f"Учитель «{name}» успешно добавлен.")

    # Добавление предмета
    
    def add_subject(self, name):
        c = self.db.conn.cursor()

        try:
            c.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
            self.db.conn.commit()

        except sqlite3.IntegrityError:
            print(f"Предмет «{name}» уже существует в базе данных.")

        else:
            print(f"Предмет «{name}» успешно добавлен.")

    # Добавление класса
    
    def add_classroom(self, number, capacity):
        c = self.db.conn.cursor()

        if int(number) < 1 or int(number) > 150:
            print(f"Номер класса должен быть с 1 по 150 включительно")
            return
        
        try:
            c.execute("INSERT INTO classrooms (number, capacity) VALUES (?, ?)", (number, capacity))
            self.db.conn.commit()

        except sqlite3.IntegrityError:
            print(f"Класс «{number}» уже существует в базе данных.")

        else:
            print(f"Класс «{name}» со вместимостью {capacity} чел. успешно добавлен.")

    # Добавление учителю урока и кабинета
    
    def add_schedule_item(self, subject_name, teacher_name, classroom_number):
        c = self.db.conn.cursor()

        # Приведение к нижнему регистру для игнорирования капса
        subject_name = subject_name.lower()
        teacher_name = teacher_name.lower()

        # Проверка наличия предмета в базе данных
        subject_exists = c.execute("SELECT COUNT(*) FROM subjects WHERE LOWER(name) = ?", (subject_name,)).fetchone()[0] > 0
        if not subject_exists:
            print(f"Предмет «{subject_name}» не найден в базе данных.")
            return

        # Проверка наличия учителя в базе данных
        teacher_exists = c.execute("SELECT COUNT(*) FROM teachers WHERE LOWER(name) = ?", (teacher_name,)).fetchone()[0] > 0
        if not teacher_exists:
            print(f"Учитель «{teacher_name}» не найден в базе данных.")
            return

        # Проверка наличия класса в базе данных
        classroom_exists = c.execute("SELECT COUNT(*) FROM classrooms WHERE number = ?", (classroom_number,)).fetchone()[0] > 0
        if not classroom_exists:
            print(f"Класс «{classroom_number}» не найден в базе данных.")
            return

        subject_id = c.execute("SELECT id FROM subjects WHERE LOWER(name) = ?", (subject_name,)).fetchone()[0]
        teacher_id = c.execute("SELECT id FROM teachers WHERE LOWER(name) = ?", (teacher_name,)).fetchone()[0]

        # Проверка, достиг ли учитель уже максимального количества уроков за день
        lessons_count = c.execute("""
            SELECT COUNT(*)
            FROM schedule
            WHERE teacher_id = ? AND date = ? AND deleted = 0

        """, (teacher_id, date.today().isoformat())).fetchone()[0]

        if lessons_count >= MAX_LESSONS_PER_DAY:
            print(f"Учитель «{teacher_name}» уже выполнил максимальное количество уроков на сегодня.")
            return

        c.execute("""
            INSERT INTO schedule (subject_id, teacher_id, classroom_number, date)
            VALUES (?, ?, ?, ?)
        """, (subject_id, teacher_id, classroom_number, date.today().isoformat()))
        self.db.conn.commit()

        print(f"Предмет: {subject_name}, учитель: {teacher_name}, класс: №{classroom_number} были добавлены в расписание текущего дня.")

    # Просмотр расписания на текущий день
    
    def view_schedule(self):
        c = self.db.conn.cursor()
        schedule = c.execute("""
            SELECT s.name, t.name, c.number, sc.date
            FROM schedule sc
            JOIN subjects s ON sc.subject_id = s.id
            JOIN teachers t ON sc.teacher_id = t.id
            JOIN classrooms c ON sc.classroom_number = c.number
            WHERE sc.date LIKE ? AND sc.deleted = 0
        """, (f"%{date.today().isoformat()}%",)).fetchall()

        if not schedule:
            print("Нет расписания на сегодня.")
        else:
            for subject, teacher, classroom, schedule_date in schedule:
                print(f"Предмет: «{subject}», Учитель: «{teacher}», Класс: «{classroom}», Дата: {schedule_date}")

    # Удаление предмета учителю
    
    def delete_schedule_item(self, subject_name, teacher_name):
        c = self.db.conn.cursor()

        subject_id = c.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,)).fetchone()
        if subject_id is None:
            print(f"Предмет «{subject_name}» не найден.")
            return

        subject_id = subject_id[0]
        teacher_id = c.execute("SELECT id FROM teachers WHERE name = ?", (teacher_name,)).fetchone()
        if teacher_id is None:
            print(f"Учитель «{teacher_name}» не найден.")
            return

        teacher_id = teacher_id[0]
        c.execute("UPDATE schedule SET deleted = 1 WHERE subject_id = ? AND teacher_id = ? AND date = ?", (subject_id, teacher_id, date.today().isoformat()))
        self.db.conn.commit()

        print(f"Элемент расписания для предмета «{subject_name}» и учителя «{teacher_name}» удален.")

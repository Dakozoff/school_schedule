from models import Teacher, Subject, Classroom, Schedule

class Console:
    def __init__(self, database):
        self.db = database
        self.schedule = Schedule(database)

    def run(self):
        start_text = ("""
School Schedule - управление расписанием учебного заведения

Управление:
1. Добавить учителя
2. Добавить предмет
3. Добавить класс
4. Добавить элемент в расписание
5. Посмотреть расписание
6. Удалить элемент расписания

""")

        print(start_text)

        while True:
            action = int(input("Введите запрос: "))
            
            if action == 1:
                print("~~~~")
                name = input("Введите имя учителя: ")
                self.schedule.add_teacher(name)
                print("~~~~")
                
            elif action == 2:
                print("~~~~")
                name = input("Введите название предмета: ")
                self.schedule.add_subject(name)
                print("~~~~")

            elif action == 3:
                print("~~~~")
                number = int(input("Введите номер класса: "))
                capacity = int(input("Введите вместимость класса: "))
                self.schedule.add_classroom(number, capacity)
                print("~~~~")

            elif action == 4:
                print("~~~~")
                subject_name = input("Введите название предмета: ")
                teacher_name = input("Введите имя учителя: ")
                classroom_number = int(input("Введите номер класса: "))
                self.schedule.add_schedule_item(subject_name, teacher_name, classroom_number)
                print("~~~~")

            elif action == 5:
                print("~~~~")
                self.schedule.view_schedule()
                print("~~~~")

            elif action == 6:
                print("~~~~")
                subject_name = input("Введите название предмета: ")
                teacher_name = input("Введите имя учителя: ")
                self.schedule.delete_schedule_item(subject_name, teacher_name)
                print("~~~~")

            elif action == "exit":
                self.db.close()
                break

            else:
                print("Действие не найдено.")

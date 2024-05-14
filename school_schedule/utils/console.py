from models import Teacher, Subject, Classroom, Schedule

class Console:
    def __init__(self, database):
        self.db = database
        self.schedule = Schedule(database)

    def run(self):
        while True:
            action = input("Введите действие, доступные: (add_teacher, add_subject, add_classroom, add_schedule_item, view_schedule, delete_schedule_item, exit): ")

            if action == "add_teacher":
                name = input("Введите имя учителя: ")
                self.schedule.add_teacher(name)
                
            elif action == "add_subject":
                name = input("Введите название предмета: ")
                self.schedule.add_subject(name)

            elif action == "add_classroom":
                number = int(input("Введите номер класса: "))
                capacity = int(input("Введите вместимость класса: "))
                self.schedule.add_classroom(number, capacity)

            elif action == "add_schedule_item":
                subject_name = input("Введите название предмета: ")
                teacher_name = input("Введите имя учителя: ")
                classroom_number = int(input("Введите номер класса: "))
                self.schedule.add_schedule_item(subject_name, teacher_name, classroom_number)

            elif action == "view_schedule":
                self.schedule.view_schedule()

            elif action == "delete_schedule_item":
                subject_name = input("Введите название предмета: ")
                teacher_name = input("Введите имя учителя: ")
                self.schedule.delete_schedule_item(subject_name, teacher_name)

            elif action == "exit":
                self.db.close()
                break

            else:
                print("Действие не найдено. Список доступных: add_teacher, add_subject, add_classroom, add_schedule_item, view_schedule, delete_schedule_item, exit")

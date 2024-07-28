from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
    QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, 
    QHeaderView, QMessageBox, QInputDialog, QDialog, QFormLayout, QLineEdit, 
    QAbstractItemView, QLabel, QDateEdit, QTimeEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
import sys
import psycopg2

# диалоговые окна вкладки ГРУППЫ
class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить студента")
        self.layout = QFormLayout(self)

        self.surname_edit = QLineEdit(self)
        self.name_edit = QLineEdit(self)
        self.otchestvo_edit = QLineEdit(self)
        self.military_department_edit = QComboBox(self)
        self.military_department_edit.addItems(["Да", "Нет"])
        self.dorm_edit = QComboBox(self)
        self.dorm_edit.addItems(["Да", "Нет"])
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Военная кафедра", self.military_department_edit)
        self.layout.addRow("Общежитие", self.dorm_edit)
        self.layout.addRow(self.add_button)

        self.add_button.clicked.connect(self.accept)

    def get_values(self):
        return self.surname_edit.text(), self.name_edit.text(), self.otchestvo_edit.text(), self.military_department_edit.currentText() == "Да", self.dorm_edit.currentText() == "Да"

class EditStudentDialog(QDialog):
    def __init__(self, student, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать студента")
        self.layout = QFormLayout(self)

        self.surname_edit = QLineEdit(self)
        self.surname_edit.setText(student[0])
        self.name_edit = QLineEdit(self)
        self.name_edit.setText(student[1])
        self.otchestvo_edit = QLineEdit(self)
        self.otchestvo_edit.setText(student[2])
        self.military_department_edit = QComboBox(self)
        self.military_department_edit.addItems(["Да", "Нет"])
        self.military_department_edit.setCurrentText("Да" if student[3] else "Нет")
        self.dorm_edit = QComboBox(self)
        self.dorm_edit.addItems(["Да", "Нет"])
        self.dorm_edit.setCurrentText("Да" if student[4] else "Нет")
        self.edit_button = QPushButton("Изменить", self)
        self.remove_button = QPushButton("Удалить", self)

        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Военная кафедра", self.military_department_edit)
        self.layout.addRow("Общежитие", self.dorm_edit)
        self.layout.addRow(self.edit_button)
        self.layout.addRow(self.remove_button)

        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def edit(self):
        self.button_clicked = "Изменить"
        self.accept()

    def remove(self):
        self.button_clicked = "Удалить"
        self.done(QDialog.Rejected)

    def buttonClicked(self):
        return self.button_clicked

    def get_values(self):
        return self.surname_edit.text(), self.name_edit.text(), self.otchestvo_edit.text(), self.military_department_edit.currentText() == "Да", self.dorm_edit.currentText() == "Да"

# диалоговые окна вкладки ПРЕДМЕТЫ
class EditSubjectDialog(QDialog):
    def __init__(self, subject, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать предмет")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(subject[1])
        self.edit_button = QPushButton("Изменить", self)
        self.remove_button = QPushButton("Удалить", self)

        self.layout.addRow("Название предмета", self.name_edit)
        self.layout.addRow(self.edit_button)
        self.layout.addRow(self.remove_button)

        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def edit(self):
        self.button_clicked = "Изменить"
        self.accept()

    def remove(self):
        self.button_clicked = "Удалить"
        self.done(QDialog.Rejected)

    def buttonClicked(self):
        return self.button_clicked

    def get_values(self):
        return self.name_edit.text()

# диалоговые окна вкладки ПРЕПОДАВАТЕЛЬСКИЙ СОСТАВ
class AddTeacherDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить преподавателя")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.surname_edit = QLineEdit(self)
        self.otchestvo_edit = QLineEdit(self)
        self.max_hours_edit = QLineEdit(self)
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Максимальное количество часов", self.max_hours_edit)
        self.layout.addRow(self.add_button)

        self.add_button.clicked.connect(self.accept)

    def get_values(self):
        if not((str.isnumeric(self.max_hours_edit.text()))):
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода часов!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.surname_edit.text(), self.otchestvo_edit.text(), int(self.max_hours_edit.text())


class EditTeacherDialog(QDialog):
    def __init__(self, teacher, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать преподавателя")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(teacher[1])
        self.surname_edit = QLineEdit(self)
        self.surname_edit.setText(teacher[2])
        self.otchestvo_edit = QLineEdit(self)
        self.otchestvo_edit.setText(teacher[3])
        self.max_hours_edit = QLineEdit(self)
        self.max_hours_edit.setText(str(teacher[4]))
        self.edit_button = QPushButton("Изменить", self)
        self.remove_button = QPushButton("Удалить", self)

        self.layout.addRow("Имя", self.name_edit)
        self.layout.addRow("Фамилия", self.surname_edit)
        self.layout.addRow("Отчество", self.otchestvo_edit)
        self.layout.addRow("Максимальное количество часов", self.max_hours_edit)
        self.layout.addRow(self.edit_button)
        self.layout.addRow(self.remove_button)

        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def edit(self):
        self.button_clicked = "Изменить"
        self.accept()

    def remove(self):
        self.button_clicked = "Удалить"
        self.done(QDialog.Rejected)

    def buttonClicked(self):
        return self.button_clicked

    def get_values(self):
        if not(str.isnumeric(self.max_hours_edit.text())):
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода часов!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.surname_edit.text(), self.otchestvo_edit.text(), int(self.max_hours_edit.text())


class AssignSubjectsDialog(QDialog):
    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Назначить предметы")
        self.layout = QVBoxLayout(self)

        self.connection = connection
        self.cursor = self.connection.cursor()

        self.teachers_combo = QComboBox(self)
        self.load_teachers()
        self.subjects_table = QTableWidget()
        self.subjects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.add_subject_button = QPushButton("Добавить предмет", self)

        self.layout.addWidget(self.teachers_combo)
        self.layout.addWidget(self.subjects_table)
        self.layout.addWidget(self.add_subject_button)

        self.teachers_combo.currentIndexChanged.connect(self.load_subjects)
        self.add_subject_button.clicked.connect(self.add_subject)
        self.subjects_table.itemDoubleClicked.connect(self.delete_subject)

        self.load_subjects()

    def load_teachers(self):
        self.cursor.execute("SELECT teacher_id, teacher_surname, teacher_name, teacher_otchestvo FROM teachers ORDER BY teacher_id")
        teachers = self.cursor.fetchall()
        self.teachers_combo.addItems([f"{teacher[1]} {teacher[2]} {teacher[3]} ({teacher[0]})" for teacher in teachers])

    def load_subjects(self):
        teacher_id = int(self.teachers_combo.currentText().split('(')[-1].split(')')[0])
        self.cursor.execute(f"SELECT subjects.subject_name FROM teachers_and_subjects JOIN subjects ON teachers_and_subjects.subject_id = subjects.subject_id WHERE teachers_and_subjects.teacher_id = {teacher_id}")
        subjects = self.cursor.fetchall()

        self.subjects_table.setRowCount(len(subjects))
        self.subjects_table.setColumnCount(1)
        self.subjects_table.setHorizontalHeaderLabels(["Название предмета"])

        for i, subject in enumerate(subjects):
            self.subjects_table.setItem(i, 0, QTableWidgetItem(subject[0]))

    def add_subject(self):
        dialog = QInputDialog(self)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("Добавить предмет")
        dialog.setLabelText("Название предмета:")
        dialog.resize(400, 200)

        self.cursor.execute("SELECT subject_name FROM subjects ORDER BY subject_id")
        subjects = self.cursor.fetchall()
        dialog.setComboBoxItems([subject[0] for subject in subjects])

        result = dialog.exec_()
        if result == QDialog.Accepted:
            subject_name = dialog.textValue()
            teacher_id = int(self.teachers_combo.currentText().split('(')[-1].split(')')[0])
            self.cursor.execute(f"SELECT subject_id FROM subjects WHERE subject_name = '{subject_name}'")
            subject_id = self.cursor.fetchone()[0]
            self.cursor.execute(f"INSERT INTO teachers_and_subjects (teacher_id, subject_id) VALUES ({teacher_id}, {subject_id})")
            self.connection.commit()
            self.load_subjects()

    def delete_subject(self):
        teacher_id = int(self.teachers_combo.currentText().split('(')[-1].split(')')[0])
        current_row = self.subjects_table.currentRow()
        subject_name = self.subjects_table.item(current_row, 0).text()
        print(subject_name)
        self.cursor.execute(f"SELECT subject_id FROM subjects WHERE subject_name = '{subject_name}'")
        subject_id = self.cursor.fetchone()[0]


        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Вы уверены, что хотите удалить этот предмет?")
        msg.setWindowTitle("Подтверждение удаления")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()

        # Если пользователь подтвердил удаление
        if retval == QMessageBox.Ok:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM teachers_and_subjects WHERE teacher_id = {teacher_id} AND subject_id = {subject_id}")
            self.connection.commit()

        self.load_subjects()

# диалоговые окна вкладки АУДИТОРИИ
class AddClassroomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить аудиторию")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.building_edit = QComboBox(self)
        self.building_edit.addItems(["GUK", "GAK", "ORSH"])
        self.type_edit = QComboBox(self)
        self.type_edit.addItems(["lecture hall", "seminary", "computer class", "gym", "laboratory"])
        self.capacity_edit = QLineEdit(self)
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Название аудитории", self.name_edit)
        self.layout.addRow("Здание", self.building_edit)
        self.layout.addRow("Тип", self.type_edit)
        self.layout.addRow("Вместимость", self.capacity_edit)
        self.layout.addRow(self.add_button)

        self.add_button.clicked.connect(self.accept)

    def get_values(self):
        capacity = self.capacity_edit.text()
        if not(str.isnumeric(capacity)) or int(capacity) <= 0:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода вместимости аудитории!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.building_edit.currentText(), self.type_edit.currentText(), int(capacity)

class EditClassroomDialog(QDialog):
    def __init__(self, classroom, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать аудиторию")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(classroom[1])
        self.building_edit = QComboBox(self)
        self.building_edit.addItems(["GUK", "GAK", "ORSH"])
        self.building_edit.setCurrentText(classroom[2])
        self.type_edit = QComboBox(self)
        self.type_edit.addItems(["lecture hall", "seminary", "computer class", "gym", "laboratory"])
        self.type_edit.setCurrentText(classroom[3])
        self.capacity_edit = QLineEdit(self)
        self.capacity_edit.setText(str(classroom[4]))
        self.edit_button = QPushButton("Изменить", self)
        self.remove_button = QPushButton("Удалить", self)

        self.layout.addRow("Название аудитории", self.name_edit)
        self.layout.addRow("Здание", self.building_edit)
        self.layout.addRow("Тип", self.type_edit)
        self.layout.addRow("Вместимость", self.capacity_edit)
        self.layout.addRow(self.edit_button)
        self.layout.addRow(self.remove_button)

        self.edit_button.clicked.connect(self.edit)
        self.remove_button.clicked.connect(self.remove)

    def edit(self):
        self.button_clicked = "Изменить"
        self.accept()

    def remove(self):
        self.button_clicked = "Удалить"
        self.done(QDialog.Rejected)

    def buttonClicked(self):
        return self.button_clicked

    def get_values(self):
        capacity = self.capacity_edit.text()
        if not(str.isnumeric(capacity)) or int(capacity) <= 0:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверный формат ввода вместимости аудитории!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return []

        return self.name_edit.text(), self.building_edit.currentText(), self.type_edit.currentText(), int(capacity)

# диалоговые окна вкладки РАСПИСАНИЕ
class AddLessonDialog(QDialog):
    def __init__(self, connection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить занятие")
        self.layout = QFormLayout(self)

        self.date_edit = QDateEdit(self)
        self.time_edit = QTimeEdit(self)
        self.classroom_edit = QComboBox(self)
        self.group_edit = QComboBox(self)
        self.subject_edit = QComboBox(self)
        self.type_edit = QComboBox(self)
        self.teacher_edit = QComboBox(self)
        self.type_edit.addItems(["lecture", "laboratory", "seminary"])
        self.add_button = QPushButton("Добавить", self)

        self.layout.addRow("Дата", self.date_edit)
        self.layout.addRow("Время", self.time_edit)
        self.layout.addRow("Аудитория", self.classroom_edit)
        self.layout.addRow("Группа", self.group_edit)
        self.layout.addRow("Предмет", self.subject_edit)
        self.layout.addRow("Тип", self.type_edit)
        self.layout.addRow("Преподаватель", self.teacher_edit)
        self.layout.addRow(self.add_button)

        self.connection = connection
        self.cursor = self.connection.cursor()

        self.load_classrooms()
        self.load_groups()
        self.load_subjects()
        self.load_teachers()


        self.add_button.clicked.connect(self.accept)

    def load_classrooms(self):
        self.cursor.execute("SELECT classroom_name, classroom_id FROM classrooms")
        classrooms = self.cursor.fetchall()
        for classroom in classrooms:
            self.classroom_edit.addItem(f"{classroom[0]} ({classroom[1]})")

    def load_groups(self):
        self.cursor.execute("SELECT group_name FROM groups")
        groups = self.cursor.fetchall()
        for group in groups:
            self.group_edit.addItem(group[0])

    def load_subjects(self):
        self.cursor.execute("SELECT subject_name FROM subjects")
        subjects = self.cursor.fetchall()
        for subject in subjects:
            self.subject_edit.addItem(subject[0])

    def load_teachers(self):
        self.cursor.execute("SELECT teacher_surname, teacher_name, teacher_otchestvo, teacher_id FROM teachers ORDER BY teacher_id")
        teachers = self.cursor.fetchall()
        for teacher in teachers:
            teacher_info = f"{teacher[0]} {teacher[1][0]}. {teacher[2][0]}. ({teacher[3]})"
            self.teacher_edit.addItem(teacher_info)

    def get_values(self):
        return self.date_edit.date(), self.time_edit.time(), self.classroom_edit.currentText(), self.group_edit.currentText(), self.subject_edit.currentText(), self.type_edit.currentText(), self.teacher_edit.currentText()



# главное окно
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schedule")
        self.setGeometry(0, 0, 300, 200)
        self.setMinimumSize(900, 700)
        self.setWindowIcon(QIcon('C:/Users/kirill/Desktop/КП БД/ПРИЛОЖЕНИЕ/icon.ico'))

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tabs = ["Группы", "Предметы", "Преподавательский состав", "Аудитории", "Расписание"]
        for tab_name in self.tabs:
            tab = QWidget()
            if tab_name == "Предметы":
                self.subjects_tab = tab
            elif tab_name == "Группы":
                self.groups_tab = tab
            elif tab_name == "Преподавательский состав":
                self.teachers_tab = tab
            elif tab_name == "Аудитории":
                self.classrooms_tab = tab
            elif tab_name == "Расписание":
                self.schedule_tab = tab
            self.tab_widget.addTab(tab, tab_name)

        self.connect_to_database()

        # вкладка ГРУППЫ
        self.groups_layout = QVBoxLayout(self.groups_tab)
        self.combo_layout = QHBoxLayout()
        self.groups_combo = QComboBox()
        self.groups_combo.setStyleSheet("font-size: 14px; color: blue")
        self.add_group_button = QPushButton("Добавить группу")
        self.add_group_button.setStyleSheet("font-size: 14px")
        self.combo_layout.addWidget(self.groups_combo)
        self.combo_layout.addWidget(self.add_group_button)
        self.groups_layout.addLayout(self.combo_layout)

        self.add_student_button = QPushButton("Добавить студента")
        self.remove_group_button = QPushButton("Удалить группу")
        
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.add_student_button)
        self.buttons_layout.addWidget(self.remove_group_button)
        self.groups_layout.addLayout(self.buttons_layout)

        self.add_student_button.setStyleSheet("font-size: 14px")
        self.remove_group_button.setStyleSheet("font-size: 14px")

        self.groups_table = QTableWidget()
        self.groups_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.groups_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.groups_layout.addWidget(self.groups_table)

        self.groups_combo.currentIndexChanged.connect(self.update_table)
        self.add_group_button.clicked.connect(self.add_group)
        self.remove_group_button.clicked.connect(self.remove_group)
        self.add_student_button.clicked.connect(self.add_student)
        self.groups_table.itemDoubleClicked.connect(self.edit_or_remove_student)

        self.load_groups()

        # вкладка ПРЕДМЕТЫ
        self.subjects_layout = QVBoxLayout(self.subjects_tab)
        self.subjects_table = QTableWidget()
        self.subjects_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.subjects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subjects_layout.addWidget(self.subjects_table)
        self.add_subject_button = QPushButton("Добавить предмет")
        self.add_subject_button.setStyleSheet("font-size: 14px")
        self.subjects_layout.addWidget(self.add_subject_button)

        self.add_subject_button.clicked.connect(self.add_subject)
        self.subjects_table.itemDoubleClicked.connect(self.edit_or_remove_subject)

        self.load_subjects()

        # вкладка ПРЕПОДАВАТЕЛЬСКИЙ СОСТАВ
        self.teachers_layout = QVBoxLayout(self.teachers_tab)
        self.teachers_table = QTableWidget()
        self.teachers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.teachers_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.teachers_layout.addWidget(self.teachers_table)
        self.add_teacher_button = QPushButton("Добавить преподавателя")
        self.add_teacher_button.setStyleSheet("font-size: 14px")
        self.teachers_layout.addWidget(self.add_teacher_button)

        self.add_teacher_button.clicked.connect(self.add_teacher)
        self.teachers_table.itemDoubleClicked.connect(self.edit_or_remove_teacher)

        self.assign_subjects_button = QPushButton("Назначить предметы", self)
        self.assign_subjects_button.setStyleSheet("font-size: 14px")
        self.teachers_layout.addWidget(self.assign_subjects_button)
        self.assign_subjects_button.clicked.connect(self.assign_subjects)

        self.load_teachers()

        # вкладка АУДИТОРИИ
        self.classrooms_layout = QVBoxLayout(self.classrooms_tab)
        self.classrooms_table = QTableWidget()
        self.classrooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.classrooms_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.classrooms_layout.addWidget(self.classrooms_table)
        self.add_classroom_button = QPushButton("Добавить аудиторию")
        self.add_classroom_button.setStyleSheet("font-size: 14px")
        self.classrooms_layout.addWidget(self.add_classroom_button)

        self.add_classroom_button.clicked.connect(self.add_classroom)
        self.classrooms_table.itemDoubleClicked.connect(self.edit_or_remove_classroom)

        self.load_classrooms()

        # вкладка РАСПИСАНИЕ
        self.schedule_layout = QVBoxLayout(self.schedule_tab)

        self.group_layout = QVBoxLayout()
        self.group_label = QLabel("Группа:")
        self.group_label.setStyleSheet("font-size: 14px;")
        self.groups_combo_schedule = QComboBox()
        self.groups_combo_schedule.setStyleSheet("font-size: 14px; color: blue")
        self.group_layout.addWidget(self.group_label)
        self.group_layout.addWidget(self.groups_combo_schedule)

        self.teacher_layout = QVBoxLayout()
        self.teacher_label = QLabel("Преподаватель:")
        self.teacher_label.setStyleSheet("font-size: 14px;")
        self.teachers_combo_schedule = QComboBox()
        self.teachers_combo_schedule.setStyleSheet("font-size: 14px; color: blue")
        self.teacher_layout.addWidget(self.teacher_label)
        self.teacher_layout.addWidget(self.teachers_combo_schedule)

        self.combo_layout_schedule = QHBoxLayout()
        self.combo_layout_schedule.addLayout(self.group_layout)
        self.combo_layout_schedule.addLayout(self.teacher_layout)
        self.schedule_layout.addLayout(self.combo_layout_schedule)

        self.schedule_table = QTableWidget()
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.schedule_layout.addWidget(self.schedule_table)

        self.add_lesson_button = QPushButton("Добавить занятие")
        self.add_lesson_button.setStyleSheet("font-size: 14px")
        self.schedule_layout.addWidget(self.add_lesson_button)

        self.groups_combo_schedule.currentIndexChanged.connect(self.update_schedule)
        self.teachers_combo_schedule.currentIndexChanged.connect(self.update_schedule)
        self.add_lesson_button.clicked.connect(self.add_lesson)

        self.schedule_table.itemDoubleClicked.connect(self.delete_lesson)

        self.load_groups_schedule()
        self.load_teachers_schedule()
        self.update_schedule()



    # Подключение к БД
    def connect_to_database(self):
        try:
            self.connection = psycopg2.connect(
                dbname="mai",
                user="postgres",
                password="20032331k",
                host="localhost",
                port="5432"
            )
            print("Успешное подключение к базе данных")
        except Exception as e:
            print(f"Произошла ошибка при подключении к базе данных: {e}")


    # Функции вкладки ГРУППЫ
    def load_groups(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT group_name FROM groups")
        groups = cursor.fetchall()
        for group in groups:
            self.groups_combo.addItem(group[0])

    def add_group(self):
        group_name, ok = QInputDialog.getText(self, 'Добавить группу', 'Введите имя группы:')
        if ok:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(group_id) FROM groups")
            max_group_id = cursor.fetchone()[0]
            new_group_id = max_group_id + 1 if max_group_id is not None else 1
            cursor.execute(f"INSERT INTO groups (group_id, group_name) VALUES ({new_group_id}, '{group_name}')")
            self.connection.commit()
            self.groups_combo.addItem(group_name)

    def update_table(self):
        group_name = self.groups_combo.currentText()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT student_id, student_surname, student_name, student_otchestvo FROM students WHERE group_id = (SELECT group_id FROM groups WHERE group_name = '{group_name}') ORDER BY student_id")
        students = cursor.fetchall()

        self.groups_table.setRowCount(len(students))
        self.groups_table.setColumnCount(4)
        self.groups_table.setHorizontalHeaderLabels(["Id", "Фамилия", "Имя", "Отчество"])

        for i, student in enumerate(students):
            for j in range(4):
                self.groups_table.setItem(i, j, QTableWidgetItem(str(student[j])))

    def remove_group(self):
        group_name = self.groups_combo.currentText()

        # Создать окно подтверждения
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setWindowTitle("Подтверждение удаления")
        confirm_box.setText(f"Вы уверены, что хотите удалить группу '{group_name}' и всех ее студентов?")
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)

        if confirm_box.exec_() == QMessageBox.Yes:
            cursor = self.connection.cursor()

            # Удалить студентов выбранной группы
            cursor.execute(f"DELETE FROM students WHERE group_id = (SELECT group_id FROM groups WHERE group_name = '{group_name}')")

            # Удалить выбранную группу
            cursor.execute(f"DELETE FROM groups WHERE group_name = '{group_name}'")

            self.connection.commit()

            # Удалить группу из выпадающего списка
            self.groups_combo.removeItem(self.groups_combo.currentIndex())

    def add_student(self):
        dialog = AddStudentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            surname, name, otchestvo, military_department, dorm = dialog.get_values()
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(student_id) FROM students")
            max_student_id = cursor.fetchone()[0]
            new_student_id = max_student_id + 1 if max_student_id is not None else 1
            group_name = self.groups_combo.currentText()
            cursor.execute(f"SELECT group_id FROM groups WHERE group_name = '{group_name}'")
            group_id = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO students (student_id, student_name, student_surname, student_otchestvo, dorm, military_department, group_id) VALUES ({new_student_id}, '{name}', '{surname}', '{otchestvo}', {dorm}, {military_department}, {group_id})")
            self.connection.commit()
            self.update_table()

    def edit_or_remove_student(self):
        current_row = self.groups_table.currentRow()
        student_id = self.groups_table.item(current_row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT student_surname, student_name, student_otchestvo, military_department, dorm FROM students WHERE student_id = {student_id}")
        student = cursor.fetchone()
        dialog = EditStudentDialog(student, self)
        result = dialog.exec_()
        if dialog.buttonClicked() == "Изменить" and result == QDialog.Accepted:
            surname, name, otchestvo, military_department, dorm = dialog.get_values()
            cursor.execute(f"UPDATE students SET student_surname = '{surname}', student_name = '{name}', student_otchestvo = '{otchestvo}', military_department = {military_department}, dorm = {dorm} WHERE student_id = {student_id}")
        elif dialog.buttonClicked() == "Удалить":
            cursor.execute(f"DELETE FROM students WHERE student_id = {student_id}")
        self.connection.commit()
        self.update_table()

    # Функции вкладки ПРЕДМЕТЫ
    def load_subjects(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM subjects ORDER BY subject_id")
        subjects = cursor.fetchall()

        self.subjects_table.setRowCount(len(subjects))
        self.subjects_table.setColumnCount(2)
        self.subjects_table.setHorizontalHeaderLabels(["Id", "Название предмета"])

        for i, subject in enumerate(subjects):
            for j in range(2):
                self.subjects_table.setItem(i, j, QTableWidgetItem(str(subject[j])))

    def add_subject(self):
        dialog = QInputDialog(self)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("Добавить предмет")
        dialog.setLabelText("Название предмета:")
        dialog.resize(400, 200)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            subject_name = dialog.textValue()
            cursor = self.connection.cursor()
            
            # Получение group_id последнего добавленного элемента
            cursor.execute("SELECT MAX(subject_id) FROM subjects")
            last_subject_id = cursor.fetchone()[0]
            
            # Если таблица groups пуста, устанавливаем group_id равным 1
            if last_subject_id is None:
                last_subject_id = 0
            subject_id = last_subject_id + 1

            cursor.execute(f"INSERT INTO subjects (subject_id, subject_name) VALUES ({subject_id}, '{subject_name}')")
            self.connection.commit()
            self.load_subjects()

    def edit_or_remove_subject(self):
        current_row = self.subjects_table.currentRow()
        subject_id = self.subjects_table.item(current_row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM subjects WHERE subject_id = {subject_id}")
        subject = cursor.fetchone()
        dialog = EditSubjectDialog(subject, self)
        result = dialog.exec_()
        if dialog.buttonClicked() == "Изменить" and result == QDialog.Accepted:
            subject_name = dialog.get_values()
            cursor.execute(f"UPDATE subjects SET subject_name = '{subject_name}' WHERE subject_id = {subject_id}")
        elif dialog.buttonClicked() == "Удалить":
            cursor.execute(f"DELETE FROM subjects WHERE subject_id = {subject_id}")
        self.connection.commit()
        self.load_subjects()

    # Функции вкладки ПРЕПОДАВАТЕЛЬСКИЙ СОСТАВ
    def load_teachers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT teacher_id, teacher_surname, teacher_name, teacher_otchestvo, max_hours FROM teachers ORDER BY teacher_id")
        teachers = cursor.fetchall()

        self.teachers_table.setRowCount(len(teachers))
        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels(["Id", "Фамилия", "Имя", "Отчество", "Занятость"])

        for i, teacher in enumerate(teachers):
            teacher = list(teacher)
            cursor.execute(f"SELECT public.get_teacher_hours({teacher[0]})")
            teacher_busy_hours = cursor.fetchone()[0]
            teacher[-1] = f"{teacher_busy_hours}/{teacher[-1]}"
            for j in range(5):
                self.teachers_table.setItem(i, j, QTableWidgetItem(str(teacher[j])))

    def add_teacher(self):
        dialog = AddTeacherDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            values = dialog.get_values()
            if not values:
                return
            name, surname, otchestvo, max_hours = values
            cursor = self.connection.cursor()
            
            # Получение teacher_id последнего добавленного элемента
            cursor.execute("SELECT MAX(teacher_id) FROM teachers")
            last_teacher_id = cursor.fetchone()[0]
            
            # Если таблица teachers пуста, устанавливаем teacher_id равным 1
            if last_teacher_id is None:
                last_teacher_id = 0
            new_teacher_id = last_teacher_id + 1

            try:
                cursor.execute(f"INSERT INTO teachers (teacher_id, teacher_name, teacher_surname, teacher_otchestvo, max_hours) VALUES ({new_teacher_id}, '{name}', '{surname}', '{otchestvo}', {max_hours})")
                self.connection.commit()
            except psycopg2.Error as e:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText(str(str(e)).split("\n")[0])
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.connection.rollback()

            self.load_teachers()

    def edit_or_remove_teacher(self):
        current_row = self.teachers_table.currentRow()
        teacher_id = self.teachers_table.item(current_row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM teachers WHERE teacher_id = {teacher_id}")
        teacher = cursor.fetchone()
        dialog = EditTeacherDialog(teacher, self)
        result = dialog.exec_()
        if dialog.buttonClicked() == "Изменить" and result == QDialog.Accepted:
            values = dialog.get_values()
            if not values:
                return
            name, surname, otchestvo, max_hours = values
            try:
                cursor.execute(f"UPDATE teachers SET teacher_name = '{name}', teacher_surname = '{surname}', teacher_otchestvo = '{otchestvo}', max_hours = {max_hours} WHERE teacher_id = {teacher_id}")
            except psycopg2.Error as e:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText(str(str(e)).split("\n")[0])
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.connection.rollback()

        elif dialog.buttonClicked() == "Удалить":
            cursor.execute(f"DELETE FROM teachers WHERE teacher_id = {teacher_id}")
        
        self.connection.commit()
        self.load_teachers()

    def assign_subjects(self):
        dialog = AssignSubjectsDialog(self.connection, self)
        dialog.exec_()


    # Функции вкладки Аудитории
    def load_classrooms(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM classrooms ORDER BY classroom_id")
        classrooms = cursor.fetchall()

        self.classrooms_table.setRowCount(len(classrooms))
        self.classrooms_table.setColumnCount(5)
        self.classrooms_table.setHorizontalHeaderLabels(["Id", "Название аудитории", "Здание", "Тип", "Вместимость"])

        for i, classroom in enumerate(classrooms):
            for j in range(5):
                self.classrooms_table.setItem(i, j, QTableWidgetItem(str(classroom[j])))

    def add_classroom(self):
        dialog = AddClassroomDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            values = dialog.get_values()
            if not values:
                return
            name, building, room_type, capacity = values

            cursor = self.connection.cursor()
            
            # Получение classroom_id последнего добавленного элемента
            cursor.execute("SELECT MAX(classroom_id) FROM classrooms")
            last_classroom_id = cursor.fetchone()[0]
            
            # Если таблица classrooms пуста, устанавливаем classroom_id равным 1
            if last_classroom_id is None:
                last_classroom_id = 0
            new_classroom_id = last_classroom_id + 1

            cursor.execute(f"INSERT INTO classrooms (classroom_id, classroom_name, classroom_building, classroom_type, classroom_capacity) VALUES ({new_classroom_id}, '{name}', '{building}', '{room_type}', {capacity})")
            self.connection.commit()
            self.load_classrooms()

    def edit_or_remove_classroom(self):
        current_row = self.classrooms_table.currentRow()
        classroom_id = self.classrooms_table.item(current_row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM classrooms WHERE classroom_id = {classroom_id}")
        classroom = cursor.fetchone()
        dialog = EditClassroomDialog(classroom, self)
        result = dialog.exec_()
        if dialog.buttonClicked() == "Изменить" and result == QDialog.Accepted:            
            values = dialog.get_values()
            if not values:
                return
            name, building, room_type, capacity = values
            cursor.execute(f"UPDATE classrooms SET classroom_name = '{name}', classroom_building = '{building}', classroom_type = '{room_type}', classroom_capacity = {capacity} WHERE classroom_id = {classroom_id}")
        elif dialog.buttonClicked() == "Удалить":
            cursor.execute(f"DELETE FROM classrooms WHERE classroom_id = {classroom_id}")
        self.connection.commit()
        self.load_classrooms()


    # Функции вкладки Расписание
    def load_groups_schedule(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT group_name FROM groups")
        groups = cursor.fetchall()
        self.groups_combo_schedule.addItem("all")
        for group in groups:
            self.groups_combo_schedule.addItem(group[0])

    def load_teachers_schedule(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT teacher_surname, teacher_name, teacher_otchestvo, teacher_id FROM teachers ORDER BY teacher_id")
        teachers = cursor.fetchall()
        self.teachers_combo_schedule.addItem("all")
        for teacher in teachers:
            teacher_info = f"{teacher[0]} {teacher[1]} {teacher[2]} ({teacher[3]})"
            self.teachers_combo_schedule.addItem(teacher_info)

    def update_schedule(self):
        group_value = self.groups_combo_schedule.currentText()
        teacher_id = self.teachers_combo_schedule.currentText()

        # Если значение второго комбо бокса не "all", извлекаем teacher_id
        if teacher_id != "all":
            teacher_id = teacher_id.split('(')[-1].split(')')[0]

        cursor = self.connection.cursor()

        # Формируем SQL-запрос в зависимости от выбранных значений в комбо боксах
        if group_value == "all" and (teacher_id == "all" or teacher_id == ""):
            cursor.execute(f"SELECT * FROM schedule ORDER BY date, time")
        elif group_value != "all" and (teacher_id == "all" or teacher_id == ""):
            cursor.execute(f"SELECT * FROM schedule WHERE group_id = (SELECT group_id FROM groups WHERE group_name = '{group_value}') ORDER BY date, time")
        elif group_value == "all" and teacher_id != "all":
            cursor.execute(f"SELECT * FROM schedule WHERE teacher_id = {teacher_id} ORDER BY date, time")
        else:
            cursor.execute(f"SELECT * FROM schedule WHERE group_id = (SELECT group_id FROM groups WHERE group_name = '{group_value}') AND teacher_id = {teacher_id} ORDER BY date, time")

        rows = cursor.fetchall()

        # Очищаем таблицу
        self.schedule_table.setRowCount(0)

        # Заполняем таблицу
        self.schedule_table.setRowCount(len(rows))
        self.schedule_table.setColumnCount(9)
        self.schedule_table.setHorizontalHeaderLabels(["Дата", "Время", "Аудитория", "Преподаватель", "Группа", "Предмет", "Тип", "teacher_id", "classroom_id"])
        
        self.schedule_table.setColumnHidden(7, True)
        self.schedule_table.setColumnHidden(8, True)


        if group_value == "all" and (teacher_id == "all" or teacher_id == ""):
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, classrooms.classroom_name, 
                CONCAT(teachers.teacher_surname, ' ', SUBSTRING(teachers.teacher_name FROM 1 FOR 1), '. ', SUBSTRING(teachers.teacher_otchestvo FROM 1 FOR 1), '.'), 
                groups.group_name, subjects.subject_name, schedule.type, schedule.teacher_id, schedule.classroom_id
                FROM schedule
                INNER JOIN classrooms ON schedule.classroom_id = classrooms.classroom_id
                INNER JOIN teachers ON schedule.teacher_id = teachers.teacher_id
                INNER JOIN groups ON schedule.group_id = groups.group_id
                INNER JOIN subjects ON schedule.subject_id = subjects.subject_id
                ORDER BY schedule.date, schedule.time
            """)
        elif group_value != "all" and (teacher_id == "all" or teacher_id == ""):
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, classrooms.classroom_name, 
                CONCAT(teachers.teacher_surname, ' ', SUBSTRING(teachers.teacher_name FROM 1 FOR 1), '. ', SUBSTRING(teachers.teacher_otchestvo FROM 1 FOR 1), '.'), 
                groups.group_name, subjects.subject_name, schedule.type, schedule.teacher_id, schedule.classroom_id
                FROM schedule
                INNER JOIN classrooms ON schedule.classroom_id = classrooms.classroom_id
                INNER JOIN teachers ON schedule.teacher_id = teachers.teacher_id
                INNER JOIN groups ON schedule.group_id = groups.group_id
                INNER JOIN subjects ON schedule.subject_id = subjects.subject_id
                WHERE groups.group_name = '{group_value}'
                ORDER BY schedule.date, schedule.time
            """)
        elif group_value == "all" and teacher_id != "all":
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, classrooms.classroom_name, 
                CONCAT(teachers.teacher_surname, ' ', SUBSTRING(teachers.teacher_name FROM 1 FOR 1), '. ', SUBSTRING(teachers.teacher_otchestvo FROM 1 FOR 1), '.'), 
                groups.group_name, subjects.subject_name, schedule.type, schedule.teacher_id, schedule.classroom_id
                FROM schedule
                INNER JOIN classrooms ON schedule.classroom_id = classrooms.classroom_id
                INNER JOIN teachers ON schedule.teacher_id = teachers.teacher_id
                INNER JOIN groups ON schedule.group_id = groups.group_id
                INNER JOIN subjects ON schedule.subject_id = subjects.subject_id
                WHERE teachers.teacher_id = {teacher_id}
                ORDER BY schedule.date, schedule.time
            """)
        else:
            cursor.execute(f"""
                SELECT schedule.date, schedule.time, classrooms.classroom_name, 
                CONCAT(teachers.teacher_surname, ' ', SUBSTRING(teachers.teacher_name FROM 1 FOR 1), '. ', SUBSTRING(teachers.teacher_otchestvo FROM 1 FOR 1), '.'), 
                groups.group_name, subjects.subject_name, schedule.type, schedule.teacher_id, schedule.classroom_id
                FROM schedule
                INNER JOIN classrooms ON schedule.classroom_id = classrooms.classroom_id
                INNER JOIN teachers ON schedule.teacher_id = teachers.teacher_id
                INNER JOIN groups ON schedule.group_id = groups.group_id
                INNER JOIN subjects ON schedule.subject_id = subjects.subject_id
                WHERE groups.group_name = '{group_value}' AND teachers.teacher_id = {teacher_id}
                ORDER BY schedule.date, schedule.time
            """)


        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            for j in range(9):
                self.schedule_table.setItem(i, j, QTableWidgetItem(str(row[j])))

        cursor.close()

    def add_lesson(self):
        self.add_lesson_dialog = AddLessonDialog(self.connection, self)
        result = self.add_lesson_dialog.exec_()
        if result == QDialog.Accepted:
            date, time, classroom, group, subject, lesson_type, teacher = self.add_lesson_dialog.get_values()
            cursor = self.connection.cursor()

            cursor.execute(f"SELECT group_id FROM groups WHERE group_name = '{group}'")
            group_id = cursor.fetchone()[0]

            cursor.execute(f"SELECT subject_id FROM subjects WHERE subject_name = '{subject}'")
            subject_id = cursor.fetchone()[0]

            try:
                cursor.execute('CALL public.add_to_schedule(\'{}\', \'{}\', {}, {}, {}, {}, \'{}\')'.format(
                    date.toString("yyyy-MM-d"),
                    time.toString('HH:mm:ss'),
                    classroom.split('(')[-1].split(')')[0],
                    teacher.split('(')[-1].split(')')[0],
                    group_id,
                    subject_id,
                    lesson_type,
                ))
                self.connection.commit()
            except psycopg2.Error as e:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText(str(str(e)).split("\n")[0])
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                self.connection.rollback()

        self.update_schedule()
        self.load_teachers()

    def delete_lesson(self):
        current_row = self.schedule_table.currentRow()
        teacher_id = self.schedule_table.item(current_row, 7).text()
        classroom_id = self.schedule_table.item(current_row, 8).text()
        date = self.schedule_table.item(current_row, 0).text()
        time = self.schedule_table.item(current_row, 1).text()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Вы уверены, что хотите удалить это занятие?")
        msg.setWindowTitle("Подтверждение удаления")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()

        # Если пользователь подтвердил удаление
        if retval == QMessageBox.Ok:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM schedule WHERE teacher_id = {teacher_id} AND classroom_id = {classroom_id} AND date = '{date}' AND time = '{time}'")
            self.connection.commit()

        self.update_schedule()
        self.load_teachers()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())

import PyQt6
from db import Database
from PyQt6 import QtWidgets
from users_form import Ui_Form
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox,QMessageBox,QLabel


class User(QtWidgets.QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.db = Database()
        self.cursor = self.db.get_cursor()
        self.ui.pushButton.clicked.connect(self.add_document)
        self.load_documents_data()


    def load_documents_data(self):
        self.cursor.execute("Select *from document")
        data = self.cursor.fetchall()
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        try:
            for i in range(len(data)):
                self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(data[i][0])))
                self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(data[i][1])))
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(data[i][2])))
                self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(data[i][3])))
                self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(data[i][4])))
        except Exception as e:
            print(e)
    def add_document(self):
        """Добавление нового документа"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Новый документ")
        layout = QVBoxLayout()

        # Элементы формы
        name_edit = QLineEdit()
        start_edit = QLineEdit()
        end_edit = QLineEdit()
        status_edit = QLineEdit("На рассмотрении")
        user_id_edit = QLineEdit()


        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        # Компоновка
        layout.addWidget(QLabel("ID пользователя:"))
        layout.addWidget(user_id_edit)
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(name_edit)
        layout.addWidget(QLabel("Дата начала:"))
        layout.addWidget(start_edit)
        layout.addWidget(QLabel("Дата окончания:"))
        layout.addWidget(end_edit)
        layout.addWidget(QLabel("Статус:"))
        layout.addWidget(status_edit)
        layout.addWidget(buttons)
        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.cursor.execute(
                    """INSERT INTO document (id, Name, start_time, finish_time, status)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (
                        user_id_edit.text(),
                        name_edit.text(),
                        start_edit.text(),
                        end_edit.text(),
                        status_edit.text()
                    )
                )
                self.db.conn.commit()
                self.load_documents_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка добавления: {str(e)}")

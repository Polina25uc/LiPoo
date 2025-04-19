from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QComboBox, QDateEdit)
from PyQt6.QtCore import QDate


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Пользователь')
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Поля для заявки
        self.client_combo = QComboBox(self)
        self.type_combo = QComboBox(self)
        self.amount_input = QLineEdit(self)
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input = QDateEdit(self)
        self.end_date_input.setDate(QDate.currentDate().addYears(1))
        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(['Низкое', 'Среднее', 'Высокое'])

        self.layout.addWidget(QLabel("Клиент:"))
        self.layout.addWidget(self.client_combo)
        self.layout.addWidget(QLabel("Тип страхования:"))
        self.layout.addWidget(self.type_combo)
        self.layout.addWidget(QLabel("Сумма:"))
        self.layout.addWidget(self.amount_input)
        self.layout.addWidget(QLabel("Дата начала:"))
        self.layout.addWidget(self.start_date_input)
        self.layout.addWidget(QLabel("Дата окончания:"))
        self.layout.addWidget(self.end_date_input)
        self.layout.addWidget(QLabel("Приоритет:"))
        self.layout.addWidget(self.priority_combo)

        self.add_request_button = QPushButton('Создать заявку', self)
        self.layout.addWidget(self.add_request_button)

        # Кнопки просмотра
        self.view_requests_button = QPushButton('Мои заявки', self)
        self.layout.addWidget(self.view_requests_button)

        self.history_button = QPushButton('История взаимодействий', self)
        self.layout.addWidget(self.history_button)

        self.notifications_button = QPushButton('Оповещения', self)
        self.layout.addWidget(self.notifications_button)

        # Таблица заявок
        self.requests_table = QTableWidget(self)
        self.requests_table.setColumnCount(8)
        self.requests_table.setHorizontalHeaderLabels(
            ['ID', 'Клиент', 'Тип', 'Статус', 'Сумма', 'Дата начала', 'Дата окончания', 'Приоритет'])
        self.layout.addWidget(self.requests_table)

        self.setLayout(self.layout)
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QComboBox, QTextEdit)


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Администратор')
        self.setGeometry(100, 100, 1000, 600)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Поля для пользователя
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QComboBox(self)
        self.role_input.addItems(['user', 'admin'])
        self.full_name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)

        self.layout.addWidget(QLabel("Имя пользователя:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Пароль:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(QLabel("Роль:"))
        self.layout.addWidget(self.role_input)
        self.layout.addWidget(QLabel("Полное имя:"))
        self.layout.addWidget(self.full_name_input)
        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)

        self.add_user_button = QPushButton('Добавить пользователя', self)
        self.layout.addWidget(self.add_user_button)

        # Поля для клиента
        self.client_name_input = QLineEdit(self)
        self.passport_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        self.client_email_input = QLineEdit(self)
        self.address_input = QTextEdit(self)

        self.layout.addWidget(QLabel("\nДобавить клиента:"))
        self.layout.addWidget(QLabel("Полное имя:"))
        self.layout.addWidget(self.client_name_input)
        self.layout.addWidget(QLabel("Номер паспорта:"))
        self.layout.addWidget(self.passport_input)
        self.layout.addWidget(QLabel("Телефон:"))
        self.layout.addWidget(self.phone_input)
        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.client_email_input)
        self.layout.addWidget(QLabel("Адрес:"))
        self.layout.addWidget(self.address_input)

        self.add_client_button = QPushButton('Добавить клиента', self)
        self.layout.addWidget(self.add_client_button)

        # Кнопки просмотра
        self.view_requests_button = QPushButton('Просмотреть заявки', self)
        self.layout.addWidget(self.view_requests_button)

        self.view_clients_button = QPushButton('Просмотреть клиентов', self)
        self.layout.addWidget(self.view_clients_button)

        self.view_history_button = QPushButton('Просмотреть историю', self)
        self.layout.addWidget(self.view_history_button)

        # Таблица заявок
        self.requests_table = QTableWidget(self)
        self.requests_table.setColumnCount(9)
        self.requests_table.setHorizontalHeaderLabels(
            ['ID', 'Клиент', 'Тип', 'Статус', 'Сумма', 'Комиссия', 'Дата начала', 'Дата окончания', 'Приоритет'])
        self.layout.addWidget(self.requests_table)

        self.setLayout(self.layout)
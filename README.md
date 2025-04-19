# LiPoo
import sys
import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QTableWidget,
                             QTableWidgetItem, QComboBox, QTextEdit, QDateEdit)
from PyQt6.QtCore import QDate


class AdminApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Администратор')
        self.setGeometry(100, 100, 1000, 600)

        self.layout = QVBoxLayout()

        # Поля для добавления пользователя
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
        self.add_user_button.clicked.connect(self.add_user)
        self.layout.addWidget(self.add_user_button)

        # Поля для добавления клиента
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
        self.add_client_button.clicked.connect(self.add_client)
        self.layout.addWidget(self.add_client_button)

        self.view_requests_button = QPushButton('Просмотреть заявки', self)
        self.view_requests_button.clicked.connect(self.view_requests)
        self.layout.addWidget(self.view_requests_button)

        self.view_clients_button = QPushButton('Просмотреть клиентов', self)
        self.view_clients_button.clicked.connect(self.view_clients)
        self.layout.addWidget(self.view_clients_button)

        self.view_history_button = QPushButton('Просмотреть историю взаимодействий', self)
        self.view_history_button.clicked.connect(self.view_interaction_history)
        self.layout.addWidget(self.view_history_button)

        self.requests_table = QTableWidget(self)
        self.requests_table.setColumnCount(9)
        self.requests_table.setHorizontalHeaderLabels(
            ['ID', 'Клиент', 'Тип', 'Статус', 'Сумма', 'Комиссия', 'Дата начала', 'Дата окончания', 'Приоритет'])
        self.layout.addWidget(self.requests_table)

        self.setLayout(self.layout)

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='insurance_company',
                user='root',
                password=''
            )
            return connection
        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка подключения к базе данных: {str(e)}")
            return None

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()
        full_name = self.full_name_input.text()
        email = self.email_input.text()

        if not all([username, password, full_name, email]):
            QMessageBox.warning(self, 'Предупреждение', 'Все поля должны быть заполнены')
            return

        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, role, full_name, email) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (username, password, role, full_name, email))
            connection.commit()
            QMessageBox.information(self, 'Успех', 'Пользователь добавлен успешно.')
            # Очищаем поля после успешного добавления
            self.username_input.clear()
            self.password_input.clear()
            self.full_name_input.clear()
            self.email_input.clear()
        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при добавлении пользователя: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_client(self):
        full_name = self.client_name_input.text()
        passport = self.passport_input.text()
        phone = self.phone_input.text()
        email = self.client_email_input.text()
        address = self.address_input.toPlainText()

        if not all([full_name, passport, phone]):
            QMessageBox.warning(self, 'Предупреждение', 'Обязательные поля: имя, паспорт и телефон')
            return

        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO clients (full_name, passport_number, phone, email, address) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (full_name, passport, phone, email if email else None, address if address else None))
            connection.commit()
            QMessageBox.information(self, 'Успех', 'Клиент добавлен успешно.')
            # Очищаем поля после успешного добавления
            self.client_name_input.clear()
            self.passport_input.clear()
            self.phone_input.clear()
            self.client_email_input.clear()
            self.address_input.clear()
        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при добавлении клиента: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def view_requests(self):
        self.requests_table.setRowCount(0)
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT ir.request_id, c.full_name, it.type_name, ir.status, ir.amount, 
                       ir.commission, ir.start_date, ir.end_date, ir.priority
                FROM insurance_requests ir
                JOIN clients c ON ir.client_id = c.client_id
                JOIN insurance_types it ON ir.type_id = it.type_id
            ''')
            requests = cursor.fetchall()

            for row in requests:
                row_position = self.requests_table.rowCount()
                self.requests_table.insertRow(row_position)
                self.requests_table.setItem(row_position, 0, QTableWidgetItem(str(row['request_id'])))
                self.requests_table.setItem(row_position, 1, QTableWidgetItem(row['full_name']))
                self.requests_table.setItem(row_position, 2, QTableWidgetItem(row['type_name']))
                self.requests_table.setItem(row_position, 3, QTableWidgetItem(row['status']))
                self.requests_table.setItem(row_position, 4, QTableWidgetItem(str(row['amount'])))
                self.requests_table.setItem(row_position, 5, QTableWidgetItem(str(row['commission'])))
                self.requests_table.setItem(row_position, 6, QTableWidgetItem(str(row['start_date'])))
                self.requests_table.setItem(row_position, 7, QTableWidgetItem(str(row['end_date'])))
                self.requests_table.setItem(row_position, 8, QTableWidgetItem(row['priority']))

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при загрузке заявок: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def view_clients(self):
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT client_id, full_name, passport_number, phone, email, address FROM clients')
            clients = cursor.fetchall()

            client_window = QWidget()
            client_window.setWindowTitle("Список клиентов")
            client_window.setGeometry(150, 150, 800, 500)
            layout = QVBoxLayout()

            clients_table = QTableWidget(client_window)
            clients_table.setColumnCount(6)
            clients_table.setHorizontalHeaderLabels(['ID', 'Имя', 'Паспорт', 'Телефон', 'Email', 'Адрес'])
            clients_table.setRowCount(0)

            for row in clients:
                row_position = clients_table.rowCount()
                clients_table.insertRow(row_position)
                clients_table.setItem(row_position, 0, QTableWidgetItem(str(row['client_id'])))
                clients_table.setItem(row_position, 1, QTableWidgetItem(row['full_name']))
                clients_table.setItem(row_position, 2, QTableWidgetItem(row['passport_number']))
                clients_table.setItem(row_position, 3, QTableWidgetItem(row['phone']))
                clients_table.setItem(row_position, 4, QTableWidgetItem(row['email'] if row['email'] else ''))
                clients_table.setItem(row_position, 5, QTableWidgetItem(row['address'] if row['address'] else ''))

            layout.addWidget(clients_table)
            client_window.setLayout(layout)
            client_window.show()

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при загрузке клиентов: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def view_interaction_history(self):
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT h.history_id, ir.request_id, u.full_name, h.action, h.action_time 
                FROM interaction_history h
                JOIN insurance_requests ir ON h.request_id = ir.request_id
                JOIN users u ON h.user_id = u.user_id
                ORDER BY h.action_time DESC
            ''')
            history = cursor.fetchall()

            history_window = QWidget()
            history_window.setWindowTitle("История взаимодействий")
            history_window.setGeometry(150, 150, 800, 500)
            layout = QVBoxLayout()

            history_table = QTableWidget(history_window)
            history_table.setColumnCount(5)
            history_table.setHorizontalHeaderLabels(['ID', 'Заявка ID', 'Пользователь', 'Действие', 'Время'])
            history_table.setRowCount(0)

            for row in history:
                row_position = history_table.rowCount()
                history_table.insertRow(row_position)
                history_table.setItem(row_position, 0, QTableWidgetItem(str(row['history_id'])))
                history_table.setItem(row_position, 1, QTableWidgetItem(str(row['request_id'])))
                history_table.setItem(row_position, 2, QTableWidgetItem(row['full_name']))
                history_table.setItem(row_position, 3, QTableWidgetItem(row['action']))
                history_table.setItem(row_position, 4, QTableWidgetItem(str(row['action_time'])))

            layout.addWidget(history_table)
            history_window.setLayout(layout)
            history_window.show()

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при загрузке истории: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class UserApp(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('Пользователь')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Поля для создания новой заявки
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
        self.add_request_button.clicked.connect(self.add_request)
        self.layout.addWidget(self.add_request_button)

        self.view_requests_button = QPushButton('Просмотреть мои заявки', self)
        self.view_requests_button.clicked.connect(self.view_my_requests)
        self.layout.addWidget(self.view_requests_button)

        self.history_button = QPushButton('Просмотреть историю взаимодействия', self)
        self.history_button.clicked.connect(self.view_history)
        self.layout.addWidget(self.history_button)

        self.notifications_button = QPushButton('Получить оповещения о выполнении', self)
        self.notifications_button.clicked.connect(self.view_notifications)
        self.layout.addWidget(self.notifications_button)

        self.requests_table = QTableWidget(self)
        self.requests_table.setColumnCount(8)
        self.requests_table.setHorizontalHeaderLabels(
            ['ID', 'Клиент', 'Тип', 'Статус', 'Сумма', 'Дата начала', 'Дата окончания', 'Приоритет'])
        self.layout.addWidget(self.requests_table)

        self.load_clients_and_types()
        self.setLayout(self.layout)

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='insurance_company',
                user='root',
                password=''
            )
            return connection
        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка подключения к базе данных: {str(e)}")
            return None

    def load_clients_and_types(self):
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)

            # Загрузка клиентов
            cursor.execute('SELECT client_id, full_name FROM clients')
            clients = cursor.fetchall()
            self.client_combo.clear()
            for client in clients:
                self.client_combo.addItem(client['full_name'], client['client_id'])

            # Загрузка типов страхования
            cursor.execute('SELECT type_id, type_name FROM insurance_types')
            types = cursor.fetchall()
            self.type_combo.clear()
            for type_ in types:
                self.type_combo.addItem(type_['type_name'], type_['type_id'])

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при загрузке данных: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_request(self):
        client_id = self.client_combo.currentData()
        type_id = self.type_combo.currentData()
        amount = self.amount_input.text()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        priority = self.priority_combo.currentText()

        if not all([client_id, type_id, amount]):
            QMessageBox.warning(self, 'Предупреждение', 'Все поля должны быть заполнены')
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, 'Предупреждение', 'Сумма должна быть числом')
            return

        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            # Рассчитываем комиссию (10% от суммы)
            commission = amount * 0.1

            cursor.execute('''
                INSERT INTO insurance_requests 
                (client_id, type_id, amount, commission, start_date, end_date, priority, assigned_to)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (client_id, type_id, amount, commission, start_date, end_date, priority, self.user_id))

            # Получаем ID новой заявки
            request_id = cursor.lastrowid

            # Добавляем запись в историю
            cursor.execute('''
                INSERT INTO interaction_history 
                (request_id, user_id, action)
                VALUES (%s, %s, %s)
            ''', (request_id, self.user_id, 'Создана новая заявка'))

            connection.commit()
            QMessageBox.information(self, 'Успех', 'Заявка создана успешно.')

            # Очищаем поля
            self.amount_input.clear()
            self.view_my_requests()

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при создании заявки: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def view_my_requests(self):
        if not self.user_id:
            QMessageBox.warning(self, 'Предупреждение', 'Пользователь не авторизован')
            return

        self.requests_table.setRowCount(0)
        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT ir.request_id, c.full_name, it.type_name, ir.status, ir.amount, 
                       ir.start_date, ir.end_date, ir.priority
                FROM insurance_requests ir
                JOIN clients c ON ir.client_id = c.client_id
                JOIN insurance_types it ON ir.type_id = it.type_id
                WHERE ir.assigned_to = %s
            ''', (self.user_id,))
            requests = cursor.fetchall()

            for row in requests:
                row_position = self.requests_table.rowCount()
                self.requests_table.insertRow(row_position)
                self.requests_table.setItem(row_position, 0, QTableWidgetItem(str(row['request_id'])))
                self.requests_table.setItem(row_position, 1, QTableWidgetItem(row['full_name']))
                self.requests_table.setItem(row_position, 2, QTableWidgetItem(row['type_name']))
                self.requests_table.setItem(row_position, 3, QTableWidgetItem(row['status']))
                self.requests_table.setItem(row_position, 4, QTableWidgetItem(str(row['amount'])))
                self.requests_table.setItem(row_position, 5, QTableWidgetItem(str(row['start_date'])))
                self.requests_table.setItem(row_position, 6, QTableWidgetItem(str(row['end_date'])))
                self.requests_table.setItem(row_position, 7, QTableWidgetItem(row['priority']))

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при загрузке заявок: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def view_history(self):
        if not self.user_id:
            QMessageBox.warning(self, 'Предупреждение', 'Пользователь не авторизован')
            return

        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT h.history_id, ir.request_id, u.full_name, h.action, h.action_time 
                FROM interaction_history h
                JOIN insurance_requests ir ON h.request_id = ir.request_id
                JOIN users u ON h.user_id = u.user_id
                WHERE ir.assigned_to = %s
                ORDER BY h.action_time DESC
            ''', (self.user_id,))
            history = cursor.fetchall()

            history_window = QWidget()
            history_window.setWindowTitle("История взаимодействий")
            history_window.setGeometry(150, 150, 800, 500)
            layout = QVBoxLayout()

            history_table = QTableWidget(history_window)
            history_table.setColumnCount(5)
            history_table.setHorizontalHeaderLabels(['ID', 'Заявка ID', 'Пользователь', 'Действие', 'Время'])
            history_table.setRowCount(0)

            for row in history:
                row_position = history_table.rowCount()
                history_table.insertRow(row_position)
                history_table.setItem(row_position, 0, QTableWidgetItem(str(row['history_id'])))
                history_table.setItem(row_position, 1, QTableWidgetItem(str(row['request_id'])))
                history_table.setItem(row_position, 2, QTableWidgetItem(row['full_name']))
                history_table.setItem(row_position, 3, QTableWidgetItem(row['action']))
                history_table.setItem(row_position, 4, QTableWidgetItem(str(row['action_time'])))

            layout.addWidget(history_table)
            history_window.setLayout(layout)
            history_window.show()

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при загрузке истории: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def view_notifications(self):
        if not self.user_id:
            QMessageBox.warning(self, 'Предупреждение', 'Пользователь не авторизован')
            return

        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT request_id, status, completed_at 
                FROM insurance_requests 
                WHERE assigned_to = %s AND status = 'completed' 
                AND completed_at >= DATE_SUB(NOW(), INTERVAL 1 DAY)
            ''', (self.user_id,))
            notifications = cursor.fetchall()

            if not notifications:
                QMessageBox.information(self, 'Уведомления', 'Новых уведомлений нет.')
                return

            msg = QMessageBox()
            msg.setWindowTitle("Уведомления о выполнении")
            msg.setText(f"У вас {len(notifications)} выполненных заявок за последние сутки:")

            details = "\n".join([f"Заявка #{n['request_id']} завершена в {n['completed_at']}" for n in notifications])
            msg.setDetailedText(details)
            msg.exec()

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка при проверке уведомлений: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход в систему')
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addWidget(QLabel("Имя пользователя:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Пароль:"))
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton('Войти', self)
        self.login_button.clicked.connect(self.authenticate)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)
        self.user_app = None
        self.admin_app = None

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='insurance_company',
                user='root',
                password=''
            )
            return connection
        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка подключения к базе данных: {str(e)}")
            return None

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Предупреждение', 'Введите имя пользователя и пароль')
            return

        connection = self.get_db_connection()
        if connection is None:
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT user_id, username, role FROM users WHERE username = %s AND password = %s',
                           (username, password))
            user = cursor.fetchone()

            if user:
                if user['role'] == 'admin':
                    self.admin_app = AdminApp()
                    self.admin_app.show()
                    self.close()
                else:
                    self.user_app = UserApp(user['user_id'])
                    self.user_app.show()
                    self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверное имя пользователя или пароль')

        except Error as e:
            QMessageBox.critical(self, 'Ошибка', f"Ошибка аутентификации: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

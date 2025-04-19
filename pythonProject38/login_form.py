from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                            QLineEdit, QPushButton)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход в систему')
        self.setGeometry(100, 100, 300, 200)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addWidget(QLabel("Имя пользователя:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Пароль:"))
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton('Войти', self)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)
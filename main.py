import PyQt6
from db import Database
from forms import Ui_Form
from PyQt6.QtWidgets import QApplication,QWidget
from user import User
from admin import Admin

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.db = Database()
        self.cursor = self.db.get_cursor()
        self.ui.pushButton.clicked.connect(self.vxod)

    def vxod(self):
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        self.cursor.execute("SELECT* from user")
        data = self.cursor.fetchall()
        for i in data:
            if login == i[1] and password == i[2] and i[3]=="admin":
                self.open_admin(i[0])
                print("admin")
                break
            elif login == i[1] and password == i[2] and i[3]=="user":
                self.open_user(i[0])
                print("user")
                break
        else:
            print("Пользователь не найден")

    def open_user(self,id_user: int):
        self.us = User(id_user)
        self.us.show()
        self.close()

    def open_admin(self,id_admin: int):
        self.ad = Admin(id_admin)
        self.ad.show()
        self.close()




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    windows = Login()
    windows.show()
    sys.exit(app.exec())



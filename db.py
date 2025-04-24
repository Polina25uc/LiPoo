import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        try:
            self.conn = pymysql.connect(host="localhost", user="root", password="", database="company")
            print('Подключение успешное')
        except Error as e:
            print('Ошибка подключения')

    def get_cursor(self):
        return self.conn.cursor()
    def close(self):
        if self.conn:
            self.conn.close()

            print('Соединение закрыто')



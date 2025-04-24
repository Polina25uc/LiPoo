import PyQt6
from db import Database
from PyQt6 import QtWidgets
from admin_form import Ui_Form
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox,QMessageBox


class Admin(QtWidgets.QWidget):
    def __init__(self, admin_id=None):
        super().__init__()
        self.admin_id = admin_id
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.db = Database()
        self.cursor = self.db.get_cursor()
        self.ui.pushButton_3.clicked.connect(self.delete_selected_document)
        self.load_documents_data()
        self.ui.pushButton_2.clicked.connect(self.edit_document)

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

    def delete_selected_document(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            item = self.ui.tableWidget.item(selected_row, 0)
            if item:
                document_id = int(item.text())
                self.cursor.execute("DELETE FROM document WHERE id = %s", (document_id,))
                self.db.conn.commit()
                self.load_documents_data()

    def edit_document(self):
        row = self.ui.tableWidget.currentRow()
        if row < 0: return
        doc_id = self.ui.tableWidget.item(row, 0).text()
        current_name = self.ui.tableWidget.item(row, 1).text()
        current_start = self.ui.tableWidget.item(row, 2).text()
        current_end = self.ui.tableWidget.item(row, 3).text()
        current_status = self.ui.tableWidget.item(row, 4).text()
        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование")
        layout = QVBoxLayout()
        name_edit = QLineEdit(current_name)
        start_edit = QLineEdit(current_start)
        end_edit = QLineEdit(current_end)
        status_edit = QLineEdit(current_status)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(name_edit)
        layout.addWidget(start_edit)
        layout.addWidget(end_edit)
        layout.addWidget(status_edit)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.cursor.execute(
                    """UPDATE document SET
                        Name = %s,
                        start_time = %s,
                        finish_time = %s,
                        status = %s
                    WHERE id = %s""",
                    (name_edit.text(), start_edit.text(),
                     end_edit.text(), status_edit.text(), doc_id)
                )
                self.db.conn.commit()
                self.load_documents_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка обновления: {str(e)}")


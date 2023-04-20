import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("MainWin.ui", self)
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui.btnCrud_clients.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.page_crud_clients))
        self.ui.btnCrud_users.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_users))
        self.ui.btnCrud_cars.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_cars))
    def connect_to_database(self):
        self.connexion.connect()
        if self.connexion.connection.is_connected():
            QtWidgets.QMessageBox.information(self, "Success", "Connected to database")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to database")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

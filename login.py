import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("login.ui", self)
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui.connectButton.clicked.connect(self.connect_to_database)

    def getLoginPassword(self):
        req = f"select * from utilisateur"
        self.connexion.cursor.execute(req)
        users = self.connexion.cursor.fetchall()
        return users

    def connect_to_database(self):
        if(self.connexion.connect()):
            print("success")
            users = self.getLoginPassword()
            print(users)
    def verifyCoordinates(self):
        login = self.ui.login.text()
        mdp = self.ui.mdp.text()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())

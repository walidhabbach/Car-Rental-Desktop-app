import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("login.ui", self)
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui.connectButton.clicked.connect(self.connect_to_database)

    def getLoginPassword(self,login,password):
        req = f"select * from utilisateur where login='{login}' and mdp='{password}'"
        self.connexion.cursor.execute(req)
        users = self.connexion.cursor.fetchall()
        return users

    def connect_to_database(self):
        if(self.connexion.connect()):
            login = self.ui.login.text()
            mdp = self.ui.mdp.text()
            print("success")
            users = self.getLoginPassword(login,mdp)
            if (len(users) == 0):
                message = QtWidgets.QMessageBox()
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("mot de passe ou login incorrecte")
                message.setWindowTitle("Error!")
                message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setText("Login et mdp correcte :=)")
                message.setWindowTitle("nice!")
                message.exec_()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())

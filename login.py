import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn
import mainInt as m
class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("login.ui", self)
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui.connectButton.clicked.connect(self.connect_to_database)
        self.ui.login.setText("a")
        self.ui.mdp.setText("12345")
        self.admin_o_n = True #switch this to False to view normal demonstration this is just for test :)

    def getLoginPassword(self,login,password,admin_o_n):
        message = QtWidgets.QMessageBox()
        if(login != "" and password != ""):
            flag = True
            req = f"select admin from super_utilisateur su join utilisateur u on su.idUser = u.idUser where login='{login}' and mdp='{password}' "
            try:
                self.connexion.cursor.execute(req)
                users = self.connexion.cursor.fetchall()
                if (len(users) != 0):
                    print(admin_o_n)
                    if (admin_o_n == 'Admin' and users[0][0] == 0):
                        print("ceci est un compte d'un employé : ")
                        message.setIcon(QtWidgets.QMessageBox.Critical)
                        message.setText("ceci est un compte d'un employé : ")
                        message.exec_()
                        return False
                    elif (admin_o_n == 'Admin' and users[0][0] == 1):
                        message.setText("Connexion reussie")
                        message.exec_()
                        self.admin_o_n = True
                    if (admin_o_n == 'Employé' and users[0][0] == 1):
                        print("ceci est un compte d'un admin")
                        message.setIcon(QtWidgets.QMessageBox.Critical)
                        message.setText("ceci est un compte d'un admin")
                        message.exec_()
                        return False
                    elif (admin_o_n == 'Employé' and users[0][0] == 0):
                        message.setText("Connexion reussie")
                        message.exec_()
                else:
                    message.setText("Login ou mot de passe sont incorrecte")
                    message.exec_()
                    return False
            except Exception as e:
                print(f"An error occurred during SQL query execution: {e}")
                return False
        elif(login == "" and password != ""):
            message.setText("Login est vide")
            message.exec_()
            return False
        elif(login != "" and password == ""):
            message.setText("mot de passe est vide")
            message.exec_()
            return False
        else:
            message.setText("Login et mot de passe sont vide")
            message.exec_()
            return False
        return flag
    def connect_to_database(self):
        if(self.connexion.connect()):
            login = self.ui.login.text()
            mdp = self.ui.mdp.text()
            choix = self.ui.choix_admin.currentText()
            check = self.getLoginPassword(login,mdp,choix)
            # giving access to the main :
            if(check == True):
                print("everything is good")
                main_window = m.MainWindow(login,choix,self.admin_o_n)
                main_window.show()
                self.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn
class EditClient(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("editClient_ui.ui", self)

    def loadDataClient(self):
        req = f"select admin from super_utilisateur su join utilisateur u on su.idUser = u.idUser where login='{login}' and mdp='{password}' "
        self.connexion.cursor.execute(req)
        users = self.connexion.cursor.fetchall()


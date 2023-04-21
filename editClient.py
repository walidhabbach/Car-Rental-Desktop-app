import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn
class EditClient(QtWidgets.QMainWindow):
    def __init__(self,userid):
        super().__init__()
        self.idUser = userid
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui = uic.loadUi("editClient_ui.ui", self)
        self.loadDataClient()
    def loadDataClient(self):
        if (self.connexion.connect()):
            req = f"select adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation from client c join utilisateur u on c.idUser = u.idUser where u.idUser = '{self.idUser}'"
            self.connexion.cursor.execute(req)
            users = self.connexion.cursor.fetchall()
            for user in users:
                adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation = user
            self.ui.societe.setText(societe)
            self.ui.nom.setText(nom)
            self.ui.prenom.setText(prenom)
            self.ui.ville.setText(ville)
            self.ui.tel.setText(tel)
            self.ui.passport.setText(passport)
            self.ui.observation.setText(observation)
            self.ui.cin.setText(cin)
            self.ui.permis.setText(permis)

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import conn
import mysql.connector as mc

class EditClient(QtWidgets.QMainWindow):
    def __init__(self,userid):
        super().__init__()
        self.idUser = userid
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui = uic.loadUi("editClient_ui.ui", self)
        self.ui.cancelBtn.clicked.connect(self.hide)
        self.ui.editBtn.clicked.connect(self.editClientBtn)
        self.loadDataClient()
    def loadDataClient(self):
        if (self.connexion.connect()):
            req = f"select adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client c join utilisateur u on c.idUser = u.idUser where u.idUser = '{self.idUser}'"
            self.connexion.cursor.execute(req)
            users = self.connexion.cursor.fetchall()
            for user in users:
                adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire = user
            self.ui.societe.setText(societe)
            self.ui.nom.setText(nom)
            self.ui.prenom.setText(prenom)
            self.ui.ville.setText(ville)
            self.ui.tel.setText(tel)
            self.ui.passport.setText(passport)
            self.ui.observation.setText(observation)
            self.ui.cin.setText(cin)
            self.ui.permis.setText(permis)
            self.ui.adresse.setPlainText(adresse)
            if(liste_noire == 0):
                self.ui.radioNon.setChecked(True)
            else:
                self.ui.radioOui.setChecked(True)
    def editClientBtn(self):
        print("edit button triggered")
        req = f"UPDATE client SET tel='{self.ui.tel.text()}', liste_noire = '{1 if self.ui.radioOui.isChecked() else 0}', " \
              f" permis = '{self.ui.permis.text()}',observation='{self.ui.observation.toPlainText()}' WHERE idUser='{self.idUser}'"
        self.connexion.cursor.execute(req)
        self.connexion.conn.commit()

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
class EditClient(QtWidgets.QMainWindow):
    def __init__(self,userid):
        super().__init__()
        self.userid = userid
        self.client = Client.Client()
        self.ui = uic.loadUi("../main/editClient_ui.ui",self)
        self.ui.editBtn.clicked.connect(self.editClientBtn)
        self.displayDataClient(f"select adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser ")

    def displayDataClient(self,request):
        users = self.client.getClientsData(request)
        for user in users:
            adresse, nom, prenom, societe, cin, tel, ville, permis, passport, observation, liste_noire = user
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
        if (liste_noire == 0):
            self.ui.radioNon.setChecked(True)
        else:
            self.ui.radioOui.setChecked(True)
    def editClientBtn(self):
        self.client.updateClient(self.ui.tel.text(),1 if self.ui.radioOui.isChecked() else 0,self.ui.permis.text(),self.ui.observation.toPlainText(),self.userid)

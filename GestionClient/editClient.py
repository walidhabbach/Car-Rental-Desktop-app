from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
class EditClient(QtWidgets.QMainWindow):
    def __init__(self,user_dict_):
        super().__init__()
        self.user_dict = user_dict_
        self.client = Client.Client()
        self.ui = uic.loadUi("../main/editClient_ui.ui",self)
        self.ui.editBtn.clicked.connect(self.editClientBtn)
        self.displayDataClient()
    def setDictionary(self,user_dict):
        self.user_dict = user_dict
    def displayDataClient(self):
        self.ui.societe.setText(self.user_dict['societe'])
        self.ui.nom.setText(self.user_dict['nom'])
        self.ui.prenom.setText(self.user_dict['prenom'])
        self.ui.ville.setText(self.user_dict['ville'])
        self.ui.tel.setText(self.user_dict['tel'])
        self.ui.passport.setText(self.user_dict['passport'])
        self.ui.observation.setText(self.user_dict['observation'])
        self.ui.cin.setText(self.user_dict['cin'])
        self.ui.permis.setText(self.user_dict['permis'])
        self.ui.adresse.setPlainText(self.user_dict['Adresse'])
        if (int(self.user_dict['liste_noire']) == 0):
            self.ui.radioNon.setChecked(True)
        else:
            self.ui.radioOui.setChecked(True)
    def editClientBtn(self):
        print("edit client Btn")
        societe = self.ui.societe.text()
        nom = self.ui.nom.text()
        prenom = self.ui.prenom.text()
        observation = self.ui.permis.text()
        adresse = self.ui.adresse()
        print(societe)

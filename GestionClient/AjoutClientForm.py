from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
class AjoutClient(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = Client.Client()
        self.ui = uic.loadUi("../main/editClient_ui.ui",self)
        self.ui.editBtn.clicked.connect(self.editClientBtn)
        self.setDictionary()
    def setDictionary(self):
        print("hna")
        for widget in self.ui.findChildren(QtWidgets.QWidget):
            if isinstance(widget, QtWidgets.QLineEdit):
                print(f"widget:  {widget.text()}")

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
        #problem with empty dictionary trying to resolve it :
        print(self.ui.societe.text())
        self.user_dict['idUser'] = self.idUser
        self.user_dict['societe'] = self.ui.societe.text()
        self.user_dict['nom'] = self.ui.nom.text()
        self.user_dict['prenom'] = self.ui.prenom.text()
        self.user_dict['ville'] = self.ui.prenom.text()
        self.user_dict['tel'] = self.ui.tel.text()
        self.user_dict['passport'] = self.ui.passport.text()
        self.user_dict['liste_noire'] = 1 if self.ui.radioOui.isChecked() == True else 0
        self.user_dict['cin'] = self.ui.cin.text()
        self.user_dict['permis'] = self.ui.permis.text()
        self.user_dict['observation'] = self.ui.observation.toPlainText()
        #calling update function :
        self.client.updateClient(self.user_dict)
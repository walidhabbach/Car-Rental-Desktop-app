from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
import random
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QFileDialog, QLabel
import string
from datetime import datetime
import sys
sys.path.append("./Tools/")
from Tools import Convertion
class AjoutClient(QtWidgets.QMainWindow):
    def __init__(self,tableWid,comboBox):
        super().__init__()
        self.table = tableWid
        self.client = Client.Client()
        self.convert = Convertion.convert()
        self.ui = uic.loadUi("../main/editClient_ui.ui",self)
        self.ui.image_btn.clicked.connect(self.image_dialog)
        self.ui.valider_btn.clicked.connect(self.AddButtonClient)
        self.ui.genererPass.clicked.connect(self.generateRandomPassword)

        self.combo = comboBox
    def image_dialog(self):
        try:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Image files (*.jpg *.jpeg *.png *.bmp)")
            if file_dialog.exec_():

                file_path = file_dialog.selectedFiles()[0]
                print(file_path)
                self.imagePath = file_path
                pixmap = QPixmap(file_path)
                # Set the desired size
                desired_size = QtCore.QSize(200, 200)  # Width, Height
                # Scale the pixmap to the desired size
                pixmap = pixmap.scaled(desired_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.ui.image_label_cli.setPixmap(pixmap)
                self.ui.image_label_cli.adjustSize()

        except Exception as e:
            print(f"An error occurred: {e}")

    def AddButtonClient(self):
        try:
            if(self.verificationFields()):
                self.user_dict = dict()
                for widget in self.ui.findChildren(QtWidgets.QWidget):
                    if isinstance(widget, QtWidgets.QLineEdit) and widget.objectName() != "qt_spinbox_lineedit":
                        self.user_dict[widget.objectName()] = widget.text()
                    elif (widget.objectName() == "observation" or widget.objectName() == "adresse"):
                        self.user_dict[widget.objectName()] = widget.toPlainText()
                    elif(isinstance(widget, QtWidgets.QDateEdit)):
                        tuple_date = widget.date().getDate()
                        my_string = '/'.join(map(str, tuple_date))
                        self.user_dict['date_permis'] = my_string

                        print(self.user_dict['date_permis'])
                self.user_dict['liste_noire'] = 1 if (self.ui.radioOui.isChecked()) else 0
                self.user_dict['photo'] = self.convert.convertToBinary(self.imagePath)
                self.client.addClient(self.user_dict)
                self.client.displayClients(
                    f"select su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser ",
                    self.table)
                self.combo.clear()
                self.client.fillComboClient(self.combo,
                                     "SELECT client.idUser,nom from client join utilisateur on client.idUser = utilisateur.idUser",
                                     "client")
                self.clearAllField()
        except Exception as e:
            print(f"An error occurred: {e}")
    def generateRandomPassword(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = str()
        for i in range(5):
            password += random.choice(characters)
        self.ui.mdp.setText(password)

    def verificationFields(self):
        checkers = []
        flag = True
        flagChecks = False
        for widget in self.ui.findChildren(QtWidgets.QWidget):
            if isinstance(widget, QtWidgets.QLineEdit) and widget.objectName() != "qt_spinbox_lineedit":
                if(widget.text() == ""):
                    self.client.warning(f"champs {widget.objectName()} est requis :  ")
                    widget.setStyleSheet("border: 1px solid red")
                    flag = False
                else:
                    widget.setStyleSheet("border: 1px solid green")
                    if(widget.objectName() == "cin"):
                       if(self.client.testCin(widget.text(),"")):
                           widget.setStyleSheet("border: 1px solid red")
                           self.client.warning("cin deja entré")
                           flag = False

            elif isinstance(widget,QtWidgets.QRadioButton):
                if(widget.isChecked()):
                    flagChecks = True

            elif isinstance(widget,QtWidgets.QTextEdit):
                if (widget.toPlainText() == ""):
                    self.client.warning(f"widget is empty : {widget.objectName()} ")
                    widget.setStyleSheet("border: 1px solid red")
                    flag = False
                else:
                    widget.setStyleSheet("border: 1px solid green")

            elif isinstance(widget,QtWidgets.QDateEdit):
                dure_permis  = datetime.now().date() - datetime.strptime(widget.text(), '%d/%m/%Y').date()
                if((dure_permis.days)/365 < 2):
                    flag = False
                    self.client.warning("duree permis est inférieur a 2 ans : ")

            elif isinstance(widget,QtWidgets.QLabel):
                if widget.objectName() == "image_label_cli":
                    if widget.pixmap() is None:
                        self.client.warning("image n'est pas définie")
                        flag = False
        if(flag and flagChecks):
            return True
        elif(flag and not flagChecks):
           self.client.warning("Checkers must be filled in : ")
           return False
        elif(not flag or not flagChecks):
            return False

    def clearAllField(self):
        for widget in self.ui.findChildren(QtWidgets.QWidget):
            if isinstance(widget, QtWidgets.QLineEdit) and widget.objectName() != "qt_spinbox_lineedit" or isinstance(widget,QtWidgets.QTextEdit):
                widget.clear()
                widget.setStyleSheet("border: 1px solid gray")
            elif isinstance(widget,QtWidgets.QLabel):
                widget.clear()
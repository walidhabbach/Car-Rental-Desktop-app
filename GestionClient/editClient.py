from PyQt5 import QtCore, QtGui, QtWidgets, uic
import base64
import mainInt
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QByteArray,QBuffer,QIODevice,QDate
from datetime import datetime
import Client
class EditClient(QtWidgets.QMainWindow):
    def __init__(self,user_dict_,tableWid,table_listeNoir):
        super().__init__()
        self.table = tableWid
        self.table_list_no = table_listeNoir
        self.idUser = user_dict_['idUser']
        self.user_dict = user_dict_
        self.client = Client.Client()
        self.ui = uic.loadUi("../Location-voiture-master/editClient_ui.ui",self)
        self.ui.valider_btn.clicked.connect(self.editClientBtn)
        self.displayDataClient()
        self.getUserImage()
        self.ui.image_btn.clicked.connect(self.image_dialog)
    def getUserImage(self):
        try:
            data = self.client.getClientsData(f"SELECT photo from client where idUser={self.idUser}")
            # Convert the blob image to a QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(data[0][0])

            # Set the desired size
            desired_size = QtCore.QSize(200, 200)  # Width, Height
            # Scale the pixmap to the desired size
            pixmap = pixmap.scaled(desired_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.ui.image_label_cli.setPixmap(pixmap)
            self.ui.image_label_cli.adjustSize()
        except Exception as e:
            print(e)
    def displayDataClient(self):
        try:
            print(self.user_dict)
            for widget in self.ui.findChildren(QtWidgets.QWidget):
                for key, value in self.user_dict.items():
                    if(isinstance(widget,QtWidgets.QDateEdit)):
                        date = QDate.fromString(self.user_dict['date_permis'], 'yyyy-MM-dd')
                        widget.setDate(date)
                    else:
                        if (key.lower() == widget.objectName().lower()):
                            widget.setText(self.user_dict[key])
            if (int(self.user_dict['liste_noire']) == 0):
                self.ui.radioNon.setChecked(True)
            else:
                self.ui.radioOui.setChecked(True)
        except Exception as e:
            print(f"error : {e}")

    def editClientBtn(self):
        try:
            if (self.verificationFields()):
                # problem with empty dictionary trying to resolve it :
                for widget in self.ui.findChildren(QtWidgets.QWidget):
                    if isinstance(widget, QtWidgets.QLineEdit) and widget.objectName() != "qt_spinbox_lineedit":
                        self.user_dict[widget.objectName()] = widget.text()
                    elif (widget.objectName() == "observation"):
                        self.user_dict[widget.objectName()] = widget.toPlainText()
                    elif isinstance(widget, QtWidgets.QDateEdit):
                        tuple_date = widget.date().getDate()
                        my_string = '/'.join(map(str, tuple_date))
                        self.user_dict['date_permis'] = my_string

                self.user_dict['liste_noire'] = 1 if (self.ui.radioOui.isChecked()) else 0
                self.user_dict['idUser'] = self.idUser
                pixmap = self.ui.image_label_cli.pixmap()  # Get the pixmap from the label widget
                if pixmap is not None:
                    byte_array = QByteArray()
                    buffer = QBuffer(byte_array)
                    buffer.open(QIODevice.WriteOnly)
                    pixmap.toImage().save(buffer, 'PNG')
                    self.user_dict['photo'] = byte_array
                    self.client.updateClient(self.user_dict)
                    self.client.displayClients(
                        f"select su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser "
                        , self.table)
                    self.client.displayClients(
                        f"select su.idUser,photo,email,login,mdp,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire,date_permis from client su join utilisateur u on su.idUser = u.idUser WHERE liste_noire = 1"
                        , self.table_list_no)
        except Exception as e:
            print(e)
    def verificationFields(self):
        checkers = []
        flag = True
        flagChecks = False
        for widget in self.ui.findChildren(QtWidgets.QWidget):
            if isinstance(widget, QtWidgets.QLineEdit) and widget.objectName() != "qt_spinbox_lineedit":
                if(widget.text() == ""):
                    widget.setStyleSheet("border: 1px solid red")
                    flag = False
                else:
                    widget.setStyleSheet("border: 1px solid green")
                    if (widget.objectName() == "cin"):
                        if (self.client.testCin(widget.text(),self.idUser)):
                            widget.setStyleSheet("border: 1px solid red")
                            print("cin deja entré for edit client")
                            flag = False

            elif isinstance(widget,QtWidgets.QRadioButton):
                if(widget.isChecked()):
                    flagChecks = True
            elif isinstance(widget,QtWidgets.QTextEdit):
                if (widget.toPlainText() == ""):
                    #print(f"widget is empty : {widget.objectName()} ")
                    widget.setStyleSheet("border: 1px solid red")
                    flag = False
                else:
                    widget.setStyleSheet("border: 1px solid green")
            elif isinstance(widget,QtWidgets.QDateEdit):
                dure_permis  = datetime.now().date() - datetime.strptime(widget.text(), '%d/%m/%Y').date()
                if((dure_permis.days)/365 < 2):
                    flag = False
                    print("azbiiiii rah duree permis est inférieur a 2 ans : ")

            elif isinstance(widget,QtWidgets.QLabel):
                if widget.objectName() == "image_label_cli":
                    if widget.pixmap() is None:
                        print("image n'est pas définie")
                        flag = False

        if(flag and flagChecks):
            return True
        elif(flag and not flagChecks):
           print("Checkers must be filled in : ")
           return False
        elif(not flag or not flagChecks):
            return False

    def image_dialog(self):
        try:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Image files (*.jpg *.jpeg *.png *.bmp)")
            if file_dialog.exec_():
                file_path = file_dialog.selectedFiles()[0]
                self.imagePath = file_path
                pixmap = QPixmap(file_path)
                # Set the desired size
                desired_size = QtCore.QSize(200, 200)  # Width, Height
                # Scale the pixmap to the desired size
                pixmap = pixmap.scaled(desired_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.ui.image_label_cli.setPixmap(pixmap)
                self.ui.image_label_cli.adjustSize()
        except Exception as e:
            print(e)
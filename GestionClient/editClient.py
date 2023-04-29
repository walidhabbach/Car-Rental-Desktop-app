from PyQt5 import QtCore, QtGui, QtWidgets, uic
import base64
from PyQt5.QtGui import QPixmap, QImage
from main import mainInt
import Client
class EditClient(QtWidgets.QMainWindow):
    def __init__(self,user_dict_):
        super().__init__()
        self.idUser = user_dict_['idUser']
        self.user_dict = user_dict_
        self.client = Client.Client()
        self.ui = uic.loadUi("../main/editClient_ui.ui",self)
        self.ui.valider_btn.clicked.connect(self.editClientBtn)
        self.displayDataClient()
        self.getUserImage()
    def getUserImage(self):
        try:
            data = self.client.getClientsData(f"SELECT photo from client where idUser={self.idUser}")
            print(data[0][0])

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
        for widget in self.ui.findChildren(QtWidgets.QWidget):
            for key,value in self.user_dict.items():
                if(key.lower() == widget.objectName().lower()):
                    widget.setText(self.user_dict[key])
        if (int(self.user_dict['liste_noire']) == 0):
            self.ui.radioNon.setChecked(True)
        else:
            self.ui.radioOui.setChecked(True)

    def editClientBtn(self):
        if(self.verificationFields()):
            # problem with empty dictionary trying to resolve it :
            for widget in self.ui.findChildren(QtWidgets.QWidget):
                if isinstance(widget, QtWidgets.QLineEdit) and widget.objectName() != "qt_spinbox_lineedit":
                    self.user_dict[widget.objectName()] = widget.text()
                elif (widget.objectName() == "observation"):
                    self.user_dict[widget.objectName()] = widget.toPlainText()
            self.user_dict['liste_noire'] = 1 if (self.ui.radioOui.isChecked()) else 0
            self.user_dict['idUser'] = self.idUser
            self.client.updateClient(self.user_dict)
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

            elif isinstance(widget,QtWidgets.QRadioButton):
                if(widget.isChecked()):
                    flagChecks = True
            elif isinstance(widget,QtWidgets.QTextEdit):
                if (widget.toPlainText() == ""):
                    print(f"widget is empty : {widget.objectName()} ")
                    widget.setStyleSheet("border: 1px solid red")
                    flag = False
                else:
                    widget.setStyleSheet("border: 1px solid green")
        if(flag and flagChecks):
            return True
        elif(flag and not flagChecks):
           print("Checkers must be filled in : ")
           return False
        elif(not flag or not flagChecks):
            return False
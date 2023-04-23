from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
import random
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QFileDialog, QLabel
import string
class AjoutClient(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = Client.Client()
        self.ui = uic.loadUi("../main/editClient_ui.ui",self)
        self.ui.image_btn.clicked.connect(self.image_dialog)
        self.ui.valider_btn.clicked.connect(self.AddButtonClient)
        self.ui.genererPass.clicked.connect(self.generateRandomPassword)

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
        self.user_dict = dict()
        for widget in self.ui.findChildren(QtWidgets.QWidget):
            if isinstance(widget, QtWidgets.QLineEdit) and widget.objectName() != "qt_spinbox_lineedit":
                self.user_dict[widget.objectName()] = widget.text()
            elif (widget.objectName() == "observation" or widget.objectName() == "adresse"):
                self.user_dict[widget.objectName()] = widget.toPlainText()
        self.user_dict['liste_noire'] = 1 if (self.ui.radioOui.isChecked()) else 0
        self.client.addClient(self.user_dict)

    def generateRandomPassword(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = str()
        for i in range(5):
            password += random.choice(characters)
        self.ui.mdp.setText(password)
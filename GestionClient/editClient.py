from PyQt5 import QtCore, QtGui, QtWidgets, uic
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

    def setDictionary(self,user_dict):
        print("hna")
    def displayDataClient(self):
        print(self.user_dict)
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
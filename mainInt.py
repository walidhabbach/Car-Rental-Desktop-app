import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import conn
import editClient as ec
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,login,choix):
        super().__init__()
        self.ui = uic.loadUi("MainWin.ui", self)
        self.visible = False
        self.ui.drop_down_two.setVisible(self.visible)
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui.btnCrud_clients.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.page_crud_clients))
        self.ui.btnCrud_users.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_users))
        self.ui.btnCrud_cars.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_cars))
        self.ui.exitBtn.clicked.connect(self.exitApp)
        self.ui.dropBtn.clicked.connect(self.dropMenu)
        self.login_name.setText(self.login_name.text() + login)
        self.ui.clients_data.clicked.connect(self.handlClick)
        self.getClientsData(choix)
    def dropMenu(self):
        if(self.visible == True):
            self.visible = False
        else:
            self.visible = True
        self.ui.drop_down_two.setVisible(self.visible)
    def handlClick(self,index:QtCore.QModelIndex):
        row = index.row()
        column = index.column()
        if(column == 4):
            model = self.ui.clients_data.model()
            # Get the idUser of the clicked cell
            data = model.data(model.index(0, 0))
            message = QtWidgets.QMessageBox.question(None,"Confirmation",f"Etes vous sure de le modifier idUser : {data}",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                     QtWidgets.QMessageBox.No)
            if(message == QtWidgets.QMessageBox.Yes):
                print("yes")
                edit_client = ec.EditClient()
                edit_client.show()
            else:
                print("NO")


    def getClientsData(self,choix):
        if (self.connexion.connect()):
            flag = True
            req = f"select su.idUser,nom,prenom,adresse from client su join utilisateur u on su.idUser = u.idUser "
            self.connexion.cursor.execute(req)
            users = self.connexion.cursor.fetchall()
            # create a standard item model and set the headers
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['idUser', 'Nom', 'prenom', 'Adresse',''])
            # loop through the fetched data and add it to the model
            tab = ["edit.png","voir.png"]
            for user in users:
                row = []
                for item in user:
                    row.append(QStandardItem(str(item)))
                for i in range(2):
                    icon = QtGui.QIcon("./icons/" + tab[i])
                    item = QStandardItem()
                    item.setIcon(icon)
                    row.append(item)
                model.appendRow(row)
            self.ui.clients_data.setModel(model)
    def connect_to_database(self):
        self.connexion.connect()
        if self.connexion.connection.is_connected():
            QtWidgets.QMessageBox.information(self, "Success", "Connected to database")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to database")
    def affichage(self):
        print("hamza is in mainint")
    def exitApp(self):
        QtWidgets.QApplication.exit()


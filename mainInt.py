import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
sys.path.append("./GestionClient/")
from GestionClient import Client
from GestionClient import editClient as ec
from PyQt5.QtWidgets import QTableWidgetItem,QTabWidget
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,login,choix):
        super().__init__()
        self.ui = uic.loadUi("MainWin.ui", self)
        self.visible = False
        self.ui.drop_down_two.setVisible(self.visible)
        self.ui.btnCrud_clients.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.page_crud_clients))
        self.ui.btnCrud_users.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_users))
        self.ui.btnCrud_cars.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_cars))
        self.ui.exitBtn.clicked.connect(self.exitApp)
        self.ui.dropBtn.clicked.connect(self.dropMenu)
        self.login_name.setText(self.login_name.text() + login)
        self.ui.clients_data.clicked.connect(self.handlClick)
        self.client = Client.Client()
        self.displayClients()
    def displayClients(self):
        self.ui.clients_data.clearContents()  # Clear the existing data in the table
        self.ui.clients_data.setColumnCount(14)  # Set the number of columns in the table
        self.ui.clients_data.setHorizontalHeaderLabels(['idUser', 'Adresse', 'nom', 'prenom','societe','cin','tel','ville','permis','passport','observation','liste_noire'])  # Set the column labels

        users = self.client.getClientsData(f"select su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser ")
        self.ui.clients_data.setRowCount(len(users))  # Set the number of rows in the table
        tab = ["edit.png", "voir.png"]

        #adding select check mark :


        for row_idx, user in enumerate(users):
            for col_idx, item in enumerate(user):
                self.ui.clients_data.setItem(row_idx, col_idx,
                                             QTableWidgetItem(str(item)))  # Set the table item with the data



        icon = QtGui.QIcon("./icons/edit.png")
        icon_col = QTableWidgetItem("")
        icon_col.setIcon(icon)
        self.ui.clients_data.setItem(0, 12, icon_col)
        self.ui.clients_data.resizeColumnsToContents()  # Resize the columns to fit the content

        icon = QtGui.QIcon("./icons/delete.png")
        icon_col = QTableWidgetItem("")
        icon_col.setIcon(icon)
        self.ui.clients_data.setItem(0, 13, icon_col)
        self.ui.clients_data.resizeColumnsToContents()  # Resize the columns to fit the content


        for row in range(self.ui.clients_data.rowCount()):
            for col in range(self.ui.clients_data.columnCount()-2):
                item = self.ui.clients_data.item(row, col)
                if(col == 11):
                    if(int(item.text()) == 1):
                        item.setBackground(QtGui.QColor("red"))
                    else:
                        item.setBackground(QtGui.QColor("green"))

    def dropMenu(self):
        if(self.visible == True):
            self.visible = False
        else:
            self.visible = True
        self.ui.drop_down_two.setVisible(self.visible)
    def exitApp(self):
        QtWidgets.QApplication.exit()
    def handlClick(self,index:QtCore.QModelIndex):
        row = index.row()
        column = index.column()
        if(column == 12):
            model = self.ui.clients_data.model()
            # Get the idUser of the clicked cell
            data = model.data(model.index(0, 0))
            print(data)
            message = QtWidgets.QMessageBox.question(None, "Confirmation", f"Etes vous sure de le modifier idUser : {data}",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                     QtWidgets.QMessageBox.No)
            if (message == QtWidgets.QMessageBox.Yes):
                print("yes")
                edit_client = ec.EditClient(data)
                edit_client.show()
            else:
                print("NO")


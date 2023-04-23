import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
sys.path.append("./GestionClient/")
from GestionClient import Client
from GestionClient import editClient as ec
from PyQt5.QtWidgets import QTableWidgetItem,QTabWidget
from GestionClient import ReservationClient as rc
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,login,choix,admin_o_n):
        super().__init__()
        self.ui = uic.loadUi("main_ui.ui", self)
        self.ui.full_menu_widget.setVisible(False)
        self.client_dict = dict()
        pixmap = QtGui.QPixmap("./icon/Logo.png")
        self.ui.main_logo.setPixmap(pixmap)
        self.ui.home_Btn.setIcon(QtGui.QIcon("./icon/home-4-32.ico"))
        self.ui.home_btn_2.setIcon(QtGui.QIcon("./icon/home-4-48.ico"))
        self.ui.change_btn.setIcon(QtGui.QIcon("./icon/menu-4-32.ico"))
        self.ui.search_btn.setIcon(QtGui.QIcon("./icon/search-13-48.ico"))
        self.ui.dashborad_btn.setIcon(QtGui.QIcon("./icon/dashboard-5-32.ico"))
        self.ui.dashborad_btn_2.setIcon(QtGui.QIcon("./icon/dashboard-5-48.ico"))
        self.ui.exit_btn.setIcon(QtGui.QIcon("./icon/close-window-64.ico"))
        self.ui.exit_btn_2.setIcon(QtGui.QIcon("./icon/close-window-64.ico"))
        self.ui.client_btn.setIcon(QtGui.QIcon("./icon/group-32.ico"))
        self.ui.client_btn_2.setIcon(QtGui.QIcon("./icon/group-48.ico"))
        self.ui.exit_btn_2.setIcon(QtGui.QIcon("./icon/close-window-64.ico"))
        self.ui.cars_btn.setIcon(QtGui.QIcon("./icon/car.png"))
        self.ui.cars_btn_2.setIcon(QtGui.QIcon("./icon/car.png"))
        self.ui.users_btn.setIcon(QtGui.QIcon("./icon/activity-feed-32.ico"))
        self.ui.users_btn_2.setIcon(QtGui.QIcon("./icon/activity-feed-48.ico"))
        self.ui.user_info_btn.setIcon(QtGui.QIcon("./icon/user-48.ico"))
        self.ui.reservation_btn2.setIcon(QtGui.QIcon("./icon/user-48.ico"))

        self.ui.client_btn_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_clients))
        self.ui.client_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_clients))

        self.ui.users_btn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_users))

        self.ui.cars_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_cars))
        self.ui.cars_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_crud_cars))

        self.ui.liste_noire_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_noire_clients))

        self.ui.reserv.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_reserv))

        self.ui.clients_data.clicked.connect(self.handlClick)
        self.client = Client.Client()

        #setting the CRUD user to disabled view to the privilege of the admin :
        self.ui.users_btn.setEnabled(admin_o_n)
        if(not admin_o_n):
            self.users_btn.setStyleSheet('color: #788596')
            self.ui.user_label.setText(self.ui.user_label.text() + " Employé")
        else: self.ui.user_label.setText(self.ui.user_label.text() + " Admin")
        #linking the update button with the update method:
        self.ui.modifier_btn.clicked.connect(self.updateTable)
        self.ui.supprimer_btn.clicked.connect(self.deleteButtonClient)
        self.ui.comboClients.currentIndexChanged.connect(self.searchByComboClient)
        self.ui.comboClients_2.currentIndexChanged.connect(self.searchByComboClient)
        self.ui.reservation_client_btn.clicked.connect(self.selectReservationClient)

        self.displayClients(f"select su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser ",self.ui.clients_data)
        self.displayClients(f"select su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser where liste_noire = '{1}'",
            self.ui.page_noire_data)
        '''
        self.ui.drop_down_two.setVisible(self.visible)
        self.ui.dropBtn.clicked.connect(self.dropMenu)
        self.login_name.setText(self.login_name.text() + login)
       '''
        self.displayReservations()
        self.fillComboClient(self.ui.comboClients,
                             "SELECT client.idUser,nom from client join utilisateur on client.idUser = utilisateur.idUser")
        self.fillComboClient(self.ui.comboClients_2,
                             f"SELECT client.idUser,nom from client join utilisateur on client.idUser = utilisateur.idUser WHERE liste_noire = '{1}'")
    def selectReservationClient(self):
        if(bool(self.client_dict) == True):
            reservations = self.client.getValuePairDataClient(
                f"SELECT idCar,date_depart,date_arr FROM RESERVATION WHERE idUser = '{self.client_dict['idUser']}'")
            reservation_client_ui = rc.ReservationClient(reservations)
            reservation_client_ui.show()
        else:
            print("Try to click on a client")
        self.client_dict.clear()
    def updateTable(self):
        if(bool(self.client_dict)) == True:
            message = QtWidgets.QMessageBox.question(None, "Confirmation",
                                                     f"Etes vous sure de le modifier idUser : {self.client_dict['idUser']}",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                     QtWidgets.QMessageBox.No)
            if (message == QtWidgets.QMessageBox.Yes):
                edit_client = ec.EditClient(self.client_dict)
                edit_client.show()
            else:
                print("NO")
            self.client_dict.clear()
        else:
            print("try to click on a client")
    def deleteButtonClient(self):
        if (bool(self.client_dict)) == True:
            message = QtWidgets.QMessageBox.question(None, "Confirmation",
                                                     f"Etes vous sure de le supprimer idUser : {self.client_dict['idUser']}",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                     QtWidgets.QMessageBox.No)
            if (message == QtWidgets.QMessageBox.Yes):
                self.client.supprimerClient(self.client_dict['idUser'])
            else:
                print("NO")
            self.client_dict.clear()
        else:
            print("try to click on a client")
    def displayClients(self,request,table):
        table.clearContents()  # Clear the existing data in the table
        table.setColumnCount(12)  # Set the number of columns in the table
        table.setHorizontalHeaderLabels(['idUser', 'Adresse', 'nom', 'prenom','societe','cin','tel','ville','permis','passport','observation','liste_noire'])  # Set the column labels

        users = self.client.getClientsData(request)
        table.setRowCount(len(users))  # Set the number of rows in the table
        #adding select check mark :

        for row_idx, user in enumerate(users):
            for col_idx, item in enumerate(user):
                table.setItem(row_idx, col_idx,
                                             QTableWidgetItem(str(item)))  # Set the table item with the data

        for row in range(table.rowCount()):
            for column in range(self.ui.clients_data.columnCount()):
                item = self.ui.clients_data.item(row, column)
                if item is not None:
                    column_name = self.ui.clients_data.horizontalHeaderItem(column).text()
                    if(column_name == "liste_noire" and int(item.text()) == 1):
                        item.setBackground(QtGui.QColor("red"))
                    elif (column_name == "liste_noire" and int(item.text()) == 0):
                        item.setBackground(QtGui.QColor("green"))
        table.resizeColumnsToContents()  # Resize the columns to fit the content
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
        #to get the current row and the idUser which is 0 order
        for column in range(self.ui.clients_data.columnCount()):
            item = self.ui.clients_data.item(row, column)
            if item is not None:
                column_name = self.ui.clients_data.horizontalHeaderItem(column).text()
                self.client_dict[column_name] = item.text()


    def displayReservations(self):
        self.ui.reservation_data.clearContents()  # Clear the existing data in the table
        self.ui.reservation_data.setColumnCount(3)  # Set the number of columns in the table
        self.ui.reservation_data.setHorizontalHeaderLabels(
            ['idUser', 'idCar', 'date'])  # Set the column labels

        users = self.client.getClientsData("SELECT * FROM RESERVATION")
        print(users)
        self.ui.reservation_data.setRowCount(len(users))  # Set the number of rows in the table
        tab = ["edit.png", "voir.png"]

        # adding select check mark :

        for row_idx, user in enumerate(users):
            for col_idx, item in enumerate(user):
                self.ui.reservation_data.setItem(row_idx, col_idx,
                              QTableWidgetItem(str(item)))  # Set the table item with the data

    def fillComboClient(self,combo,request):
        diction_client = self.client.getValuePairDataClient(request)
        combo.addItem('Selectionner client')
        for key, value in diction_client.items():
            combo.addItem(value)
            # Set the key as custom data for the item
            combo.setItemData(combo.count() - 1, key)
    def searchByComboClient(self,condition):
        if (self.ui.comboClients.currentData() is not None):
            self.displayClients(f"SELECT su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser where su.idUser = '{self.ui.comboClients.currentData()}'",self.ui.clients_data)
        else:
            self.displayClients(
                f"select su.idUser,adresse,nom,prenom,societe,cin,tel,ville,permis,passport,observation,liste_noire from client su join utilisateur u on su.idUser = u.idUser ",
                self.ui.clients_data)


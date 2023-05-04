#comboBoxReservation

import conn
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QFileDialog, QLabel
from PyQt5 import QtGui
import Client

class Reservation:

    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.client_ = Client.Client()
    def getAllReser(self,request):
        try:
            if (self.connexion.connect()):
                self.connexion.cursor.execute(request)
                data = self.connexion.cursor.fetchall()
                return data
        except Exception as e:
            print(e)
    def displayReservations(self, table):
        try:
            table.clearContents()  # Clear the existing data in the table
            table.setColumnCount(3)  # Set the number of columns in the table
            table.setHorizontalHeaderLabels(
                ['idUser', 'idCar', 'date'])  # Set the column labels

            users = self.client_.getClientsData("SELECT idUser,idCar,date_depart,date_arr FROM RESERVATION")
            table.setRowCount(len(users))  # Set the number of rows in the table

            # adding select check mark :

            for row_idx, user in enumerate(users):
                for col_idx, item in enumerate(user):
                    table.setItem(row_idx, col_idx,
                                  QTableWidgetItem(str(item)))  # Set the table item with the data
        except Exception as e:
            print(f"{e}")
    def filterComboBox(self,combo,idClient):
        print(f"(---------------------triggering filter combo : {idClient} ")
        combo.clear()
        if(idClient != None ):
            count = 0
            dict_res = dict()
            combo.addItem(f'Selectionner Reservation ')
            request = f"SELECT reservation.idUser,concat(date_depart,'/',date_arr) from client join reservation on client.idUser = reservation.idUser" \
                      f" where client.idUser = '{idClient}'"
            print(request)
            res = self.getAllReser(request)
            for re in res:
                combo.addItem(str(re[1]))
                # Set the key as custom data for the item
                combo.setItemData(combo.count() - 1, re[0])
            print(res)


    def searchByReservation(self,combo,table,idClient):
        try:
            print("-------------------------------------------------------" + str(combo.currentText()))
            if(combo.currentText() != "Selectionner Reservation "):
                date_ = combo.currentText().split('/')
                print(date_)
                if (len(date_) == 2):
                    request = f"SELECT reservation.idUser,date_depart,date_arr from client join reservation on client.idUser = reservation.idUser" \
                              f" where date_depart = '{date_[0]}' and date_arr='{date_[1]}' and reservation.idUser = '{combo.currentData()}'"
                    data = self.getAllReser(request)
                    self.displayReservationsClient(table, data)
            else:
                print(f"hna 3la lkhawi {combo.currentData()}")
                request = f"SELECT reservation.idUser,date_depart,date_arr from client join reservation on client.idUser = reservation.idUser" \
                          f" WHERE reservation.idUser = '{idClient}'"
                data = self.getAllReser(request)
                self.displayReservationsClient(table, data)
        except Exception as e:
            print(e)
    def supprimer(self,request):
        try:
            if (self.connexion.connect()):
                self.connexion.cursor.execute(request)
                self.connexion.conn.commit()
                print("deleted succesfully")
        except Exception as e:
            print(e)

    def displayReservationsClient(self, table,data):
        try:
            table.clearContents()  # Clear the existing data in the table
            table.setColumnCount(3)  # Set the number of columns in the table
            table.setHorizontalHeaderLabels(
                ['idUser', 'idCar', 'date'])  # Set the column labels

            table.setRowCount(len(data))  # Set the number of rows in the table

            # adding select check mark :

            for row_idx, res in enumerate(data):
                for col_idx, item in enumerate(res):
                    table.setItem(row_idx, col_idx,
                                  QTableWidgetItem(str(item)))  # Set the table item with the data
        except Exception as e:
            print(f"{e}")
    def searchByUser(self,table,id,comboBox):
        if(id is not None):
            print("searching by User")
            request = f"SELECT idUser,idCar,date_depart,date_arr FROM RESERVATION where idUser='{id}'"
            data = self.getAllReser(request)
            print(data)
            self.displayReservationsClient(table, data)
            self.filterComboBox(comboBox,id)
        else:
            self.displayReservations(table)


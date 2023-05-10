#comboBoxReservation
from PyQt5.QtGui import QFont
import conn
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QFileDialog, QLabel,QTableWidget
from PyQt5 import QtGui
import Client
import os
import sys
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
            table.setColumnCount(9)  # Set the number of columns in the table
            table.setHorizontalHeaderLabels(
                ['idRes','nom_client','idUser', 'idCar', 'date_depart','date_arrivé','status','prix','message'])  # Set the column labels

            reservations = self.getAllReser("SELECT id_res,idUser,idCar,date_depart,date_arr,status,price,message FROM RESERVATION")
            table.setRowCount(len(reservations))  # Set the number of rows in the table

            # adding select check mark :
            for row_idx, res in enumerate(reservations):
                name = self.client_.getClientsData(
                    f"select nom from client join utilisateur on utilisateur.idUser = client.idUser where client.idUser = '{res[1]}'")
                table.setItem(row_idx, 0, QTableWidgetItem(str(res[0])))
                table.setItem(row_idx, 1, QTableWidgetItem(name[0][0]))


            for row_idx, res in enumerate(reservations):
                # get the name of client  :
                for col_idx in range(2, 9):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(res[col_idx-1])))

            for row in range(table.rowCount()):
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    if item is not None:
                        column_name = table.horizontalHeaderItem(column).text()
                        if (column_name == "status" and int(item.text()) == 1):
                            item.setBackground(QtGui.QColor("green"))
                        elif (column_name == "status" and int(item.text()) == 0):
                            item.setBackground(QtGui.QColor("red"))

            font = QFont()
            font.setBold(True)
            table.horizontalHeader().setFont(font)
            # Set row height
            table.verticalHeader().setDefaultSectionSize(80)

            # Set alternating row colors
            table.setAlternatingRowColors(True)
            table.setStyleSheet("alternate-background-color: gray;")
            table.setStyleSheet("background-color: white;  ")

            # Set selection mode to row selection
            table.setSelectionBehavior(QTableWidget.SelectRows)
        except Exception as e:
            print(f"{e}")
    def filterComboBox(self,combo,idClient):
        try:
            for i in reversed(range(combo.count())):
                item_text = combo.itemText(i)
                if "select reservation" != item_text.lower():
                    combo.removeItem(i)
            if (idClient != None):
                request = f"SELECT reservation.idUser,concat(date_depart,'/',date_arr) from client join reservation on client.idUser = reservation.idUser" \
                          f" where client.idUser = '{idClient}'"
                res = self.getAllReser(request)
                for re in res:
                    combo.addItem(str(re[1]))
                    # Set the key as custom data for the item
                    combo.setItemData(combo.count() - 1, re[0])
        except Exception as e:
            print(e)


    def getDict(self,req):
        if(self.connexion.connect()):
            self.connexion.cursor.execute(req)
            columns = [desc[0] for desc in self.connexion.cursor.description]

            results = self.connexion.cursor.fetchall()
            res = []
            for row in results:
                res.append(dict(zip(columns, row)))
            return res
    def searchByReservation(self,combo,table,idClient):
        try:
            if(combo.currentText().lower() != "select reservation"):
                date_ = combo.currentText().split('/')
                if (len(date_) == 2):
                    request = f"SELECT id_res,reservation.idUser,idCar,date_depart,date_arr,status,price,message from client join reservation on client.idUser = reservation.idUser" \
                              f" where date_depart = '{date_[0]}' and date_arr='{date_[1]}' and reservation.idUser = '{combo.currentData()}'"
                    data = self.getAllReser(request)
                    self.displayReservationsClient(table, data)
            else:
                request = f"SELECT id_res,reservation.idUser,idCar,date_depart,date_arr,status,price,message from client join reservation on client.idUser = reservation.idUser" \
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
            table.setColumnCount(9)  # Set the number of columns in the table
            table.setHorizontalHeaderLabels(
                ['idRes','nom_client','idUser', 'idCar', 'date_depart','date_arrivé','status','prix','message'])  # Set the column labels
            table.setRowCount(len(data))  # Set the number of rows in the table

            # adding select check mark :
            for row_idx, res in enumerate(data):
                name = self.client_.getClientsData(
                    f"select nom from client join utilisateur on utilisateur.idUser = client.idUser where client.idUser = '{res[1]}'")
                table.setItem(row_idx, 0, QTableWidgetItem(str(res[0])))
                table.setItem(row_idx, 1, QTableWidgetItem(str(name[0][0])))


            for row_idx, res in enumerate(data):
                # get the name of client  :
                for col_idx in range(2, 9):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(res[col_idx-1])))

            for row in range(table.rowCount()):
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    if item is not None:
                        column_name = table.horizontalHeaderItem(column).text()
                        if (column_name == "status" and int(item.text()) == 1):
                            item.setBackground(QtGui.QColor("green"))
                        elif (column_name == "status" and int(item.text()) == 0):
                            item.setBackground(QtGui.QColor("red"))
        except Exception as e:
            print(f"{e}")
    def searchByUser(self,table,id,comboBox):
        try:
            if (id is not None):
                print("searching by User")
                request = f"SELECT id_res,idUser,idCar,date_depart,date_arr,status,price,message FROM RESERVATION where idUser='{id}'"
                data = self.getAllReser(request)
                self.displayReservationsClient(table, data)
                self.filterComboBox(comboBox, id)
            else:
                for i in reversed(range(comboBox.count())):
                    item_text = comboBox.itemText(i)
                    if "select reservation" != item_text.lower():
                        comboBox.removeItem(i)
                self.displayReservations(table)
        except Exception as e:
            print(e)


    def updateReservation(self,reserva_dict):
        try:
            if (self.connexion.connect()):
                req = f"UPDATE reservation SET status={reserva_dict['status']} where id_res={reserva_dict['idRes']} "
                self.connexion.cursor.execute(req)
                self.connexion.conn.commit()
                print("updated successfully")
        except Exception as e:
            print(e)
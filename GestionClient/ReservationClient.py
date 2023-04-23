from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
from PyQt5.QtWidgets import QTableWidgetItem,QTabWidget
class ReservationClient(QtWidgets.QMainWindow):
    def __init__(self,reservation_dict):
        super().__init__()
        self.res_dict = reservation_dict
        self.client = Client.Client()
        self.ui = uic.loadUi("../main/reservation_ui.ui",self)
        self.displayReservation()
    def setDictionary(self,user_dict):
        print("hna")
    def displayReservation(self):
        self.ui.reservation_data.clearContents()  # Clear the existing data in the table
        self.ui.reservation_data.setColumnCount(3)  # Set the number of columns in the table
        self.ui.reservation_data.setHorizontalHeaderLabels(['idCar', 'date depart', 'date arrivée'])

        self.ui.reservation_data.setRowCount(len(self.res_dict))  # Set the number of rows in the table
        #adding select check mark :
        row_idx = 0
        for key, value in self.res_dict.items():
            self.ui.reservation_data.setItem(row_idx, 0, QTableWidgetItem(str(key)))
            for col in range(1,3):
                self.ui.reservation_data.setItem(row_idx, col, QTableWidgetItem(str(self.res_dict[key])))
        row_idx+=1

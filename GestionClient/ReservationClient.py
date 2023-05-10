from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
from PyQt5.QtWidgets import QTableWidgetItem,QTabWidget
class ReservationClient(QtWidgets.QMainWindow):
    def __init__(self,reservation_dict):
        super().__init__()
        self.res_dict = reservation_dict
        self.client = Client.Client()
        self.ui = uic.loadUi("../main/reservation_ui.ui",self)
        self.displayReservation(reservation_dict)
    def displayReservation(self,res):
        try:
            self.ui.reservation_data.clearContents()  # Clear the existing data in the table
            self.ui.reservation_data.setColumnCount(8)  # Set the number of columns in the table
            self.ui.reservation_data.setHorizontalHeaderLabels(['idCar','idUser', 'date depart', 'date arrivée','price','message','id_res','status'])

            self.ui.reservation_data.setRowCount(len(res))  # Set the number of rows in the table
            # adding select check mark :
            row_idx = 0
            col = 0
            print(res)
            for item in res:
                col = 0
                for key, value in item.items():
                        print(item[key])
                        self.ui.reservation_data.setItem(row_idx, col, QTableWidgetItem(str(item[key])))
                        col+=1
                row_idx += 1
        except Exception as e:
            print(e)

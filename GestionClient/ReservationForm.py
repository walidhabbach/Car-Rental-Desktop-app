from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
from PyQt5.QtWidgets import QTableWidgetItem,QTabWidget
import Reservation
class ReservationForm(QtWidgets.QMainWindow):
    def __init__(self,id_res):
       try:
           super().__init__()
           self.reservation = Reservation.Reservation()
           self.idRes = id_res
           self.ui = uic.loadUi("../main/statusReservationUi.ui", self)
           self.ui.confirmer.clicked.connect(self.confirmerBtn)
       except Exception as e:
           print(e)

    def confirmerBtn(self):
        try:
            details_status_res = dict()
            details_status_res['status'] = True
            details_status_res['idRes'] = self.idRes
            self.reservation.updateReservation(details_status_res)
        except Exception as e:
            print(e)

    def annulerBtn(self,res):
        try:
            res['status'] = False
            self.reservation.updateReservation(res)
        except Exception as e:
            print(e)
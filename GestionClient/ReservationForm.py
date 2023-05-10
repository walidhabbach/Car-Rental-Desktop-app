from PyQt5 import QtCore, QtGui, QtWidgets, uic
import Client
from PyQt5.QtWidgets import QTableWidgetItem,QTabWidget
import Reservation
class ReservationForm(QtWidgets.QMainWindow):
    def __init__(self,id_res):
       try:
           super().__init__()
           self.client = Client.Client()
           self.reservation = Reservation.Reservation()
           self.idRes = id_res
           self.ui = uic.loadUi("../main/statusReservationUi.ui", self)
           self.ui.confirmer.clicked.connect(self.confirmerBtn)
           self.setButtons()
       except Exception as e:
           print(e)


    def setButtons(self):
        reservations = self.reservation.getDict(f"SELECT * from reservation where id_res = '{self.idRes}'")
        print(reservations)
        iduser = reservations[0]['idUser']
        user = self.client.getDict(f"SELECT nom from client c join utilisateur u on u.idUser=c.idUser where c.iduser = '{iduser}'")
        self.ui.monsieurLab.setText(self.ui.monsieurLab.text() + f"{user[0]['nom']}")
        if (reservations[0]['status'] == 1):
            self.ui.confirmer.setEnabled(False)
        else:
            self.client.warning("Cette reservation est encore annuler")
            self.ui.confirmer.setEnabled(True)
    def confirmerBtn(self):
        try:
            details_status_res = dict()
            details_status_res['status'] = True
            details_status_res['idRes'] = self.idRes
            self.reservation.updateReservation(details_status_res)
            self.client.warning("cette reservation est maintenant confirmer")
        except Exception as e:
            print(e)

    def annulerBtn(self,res):
        try:
            res['status'] = False
            self.reservation.updateReservation(res)
            print("cette reservation est maintenant annuler")
        except Exception as e:
            print(e)
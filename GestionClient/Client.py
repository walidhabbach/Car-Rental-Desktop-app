import conn
from Tools import Convertion
from PyQt5.QtWidgets import QTableWidgetItem, QTabWidget, QFileDialog, QLabel
from PyQt5 import QtGui
class Client:

    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")

    def getClientsData(self,request):
        if(self.connexion.connect()):
            req = request
            self.connexion.cursor.execute(req)
            users = self.connexion.cursor.fetchall()
            return users

    def getValuePairDataClient(self,request):
        vp = dict()
        req = request
        self.connexion.cursor.execute(req)
        users = self.connexion.cursor.fetchall()
        for user in users:
            vp[user[0]] = user[1]
        return vp

    def updateClient(self,client_dict):
        try:
            print(client_dict['date_permis'])
            if (self.connexion.connect()):
                req = f"UPDATE client SET `photo`=%s ,`cin`=%s, `liste_noire` = %s, " \
                      f" `permis` = %s,`passport`=%s,`email`=%s,`observation`=%s,`societe`=%s,`ville`=%s,`tel`=%s,`date_permis`=%s WHERE `idUser`=%s"

                self.connexion.cursor.execute(req, (
                bytes(client_dict['photo']), client_dict['cin'], client_dict['liste_noire'],
                client_dict['permis'], client_dict['passport'],
                client_dict['email'], client_dict['observation'], client_dict['societe'], client_dict['ville'],
                client_dict['tel'], client_dict['date_permis'],client_dict['idUser']))

                self.connexion.conn.commit()
                print("updated successfully")
        except Exception as e:
            print(f"error: {e}")

    def supprimer(self,request):
        try:
            if (self.connexion.connect()):
                self.connexion.cursor.execute(request)
                self.connexion.conn.commit()
                print("deleted succesfully")
        except Exception as e:
            print(e)

    def addClient(self, client_dict):
        if self.connexion.connect():
            try:
                # create for the user a login and a password:
                req1 = f"INSERT INTO utilisateur(`nom`, `prenom`, `login`, `mdp`) " \
                       f"VALUES ('{client_dict['nom']}', '{client_dict['prenom']}', '{client_dict['login']}', '{client_dict['mdp']}')"
                self.connexion.cursor.execute(req1)

                num_rows = self.connexion.cursor.rowcount

                # get the id of the current row:
                req2 = f"SELECT idUser FROM utilisateur ORDER BY idUser DESC LIMIT {num_rows}"
                self.connexion.cursor.execute(req2)
                result = self.connexion.cursor.fetchone()
                client_id = result[0]
                # creating the client:
                req3 = f"INSERT INTO client(`idUser`,`photo`, `adresse`, `cin`, `liste_noire`, `permis`, `passport`, `email`, " \
                       f"`observation`, `societe`, `ville`, `tel`,`date_permis`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.connexion.cursor.execute(req3,(client_id,client_dict['photo'],client_dict['adresse'], client_dict['cin'],client_dict['liste_noire'], client_dict['permis'], client_dict['passport'],
                       client_dict['email'], client_dict['observation'], client_dict['societe'],client_dict['ville'],client_dict['tel'],client_dict['date_permis']))

                self.connexion.conn.commit()
                print("Added successfully")
            except Exception as e:
                print(f"Error: {e}")

    def displayClients(self,request,table):
        try:
            table.clearContents()  # Clear the existing data in the table
            table.setColumnCount(17)  # Set the number of columns in the table
            table.setHorizontalHeaderLabels(
                ['idUser', 'photo', 'email' , 'login', 'mdp', 'Adresse', 'nom', 'prenom', 'societe', 'cin', 'tel', 'ville',
                 'permis', 'passport', 'observation', 'liste_noire','date_permis'])  # Set the column labels
            users = self.getClientsData(request)
            table.setRowCount(len(users))  # Set the number of rows in the table
            # adding select check mark :
            self.convert = Convertion.convert()
            for row_idx, user in enumerate(users):
                table.setItem(row_idx, 0, QTableWidgetItem(str(user[0])))
                if(user[1] is not None):
                    label = QLabel()  # Create a QLabel to display the image
                    label.setScaledContents(True)  # Set the label to scale its contents
                    label.setMaximumSize(80, 80)
                    pixmap = self.convert.getImageLabel(user[1])  # Get QPixmap from binary data
                    label.setPixmap(pixmap)
                    table.setCellWidget(row_idx, 1,
                                                       label)  # Set the label as the cell widget for the image column
                for col_idx in range(2,17):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(user[col_idx])))

            #table.setColumnHidden(0, True)
            table.setColumnHidden(3, True)
            table.setColumnHidden(4, True)

            for row in range(table.rowCount()):
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    if item is not None:
                        column_name = table.horizontalHeaderItem(column).text()
                        if (column_name == "liste_noire" and int(item.text()) == 1):
                            item.setBackground(QtGui.QColor("red"))
                        elif (column_name == "liste_noire" and int(item.text()) == 0):
                            item.setBackground(QtGui.QColor("green"))
            table.resizeColumnsToContents()  # Resize the columns to fit the content

        except Exception as e:
            print(f"{e}")

    def displayReservations(self,table):
        try:
            table.clearContents()  # Clear the existing data in the table
            table.setColumnCount(3)  # Set the number of columns in the table
            table.setHorizontalHeaderLabels(
                ['idUser', 'idCar', 'date'])  # Set the column labels

            users = self.getClientsData("SELECT idUser,idCar,date_depart,date_arr FROM RESERVATION")
            table.setRowCount(len(users))  # Set the number of rows in the table

            # adding select check mark :

            for row_idx, user in enumerate(users):
                for col_idx, item in enumerate(user):
                    table.setItem(row_idx, col_idx,
                                  QTableWidgetItem(str(item)))  # Set the table item with the data
        except Exception as e:
            print(f"{e}")

    def testCin(self,cinClie,idUser):
        request = f"SELECT cin from client where idUser != '{idUser}'" if idUser != "" else "SELECT cin from client"
        cins = self.getClientsData(request)
        for cin in cins:
            if(cinClie == cin[0]):
                return True
        return False
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QLabel
import sys
import conn




class User:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")


    def getSuperUserDict(self, req):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    self.connexion.cursor.execute(req)
                    columns = [desc[0] for desc in self.connexion.cursor.description]
                    results = self.connexion.cursor.fetchall()
                    data = []
                    for row in results:
                        print("row[0] = ", row[0])
                        newDict = self.getUserById(int(row[0]))[0] | dict(zip(columns, row))
                        data.append(newDict)
                    return data
        except Exception as e:
            print(f"getSuperUserDict: An error occurred: {e}")
    def getUserDict(self, req):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    self.connexion.cursor.execute(req)
                    columns = [desc[0] for desc in self.connexion.cursor.description]
                    results = self.connexion.cursor.fetchall()
                    data = []
                    for row in results:
                        print(dict(zip(columns, row)))
                        data.append(dict(zip(columns, row)))
                    return data
        except Exception as e:
            print(f"getUserDict: An error occurred: {e}")
    def getUserById(self,idUser):
        return self.getUserDict(f"SELECT * FROM utilisateur WHERE idUser = {idUser}")

    def getSuperUserAll(self):
        return self.getSuperUserDict("SELECT * FROM super_utilisateur");
    def getSuperUserById(self,idUser):
        return self.getSuperUserDict(f"SELECT * FROM super_utilisateur where idUser={idUser}");



    def addEmployee(self, employee_dict):
        try:
            if self.connexion.connect():
                # create for the user a login and a password:
                req1 = f"INSERT INTO utilisateur(`nom`, `prenom`, `login`, `mdp`) " \
                       f"VALUES ('{employee_dict['nom']}', '{employee_dict['prenom']}', '{employee_dict['login']}', '{employee_dict['mdp']}')"
                self.connexion.cursor.execute(req1)

                num_rows = self.connexion.cursor.rowcount
                print("super user")
                # get the id of the current row:
                req2 = f"SELECT idUser FROM utilisateur ORDER BY idUser DESC LIMIT {num_rows}"
                self.connexion.cursor.execute(req2)
                result = self.connexion.cursor.fetchone()
                employee_dict["idUser"] = result[0]
                print("get id",employee_dict["idUser"] )
                # creating the client:
                req3 = f"INSERT INTO super_utilisateur(`idUser`, `admin`, `address`, `cin`, `salary`) VALUES (%s,%s,%s,%s,%s)"
                self.connexion.cursor.execute(req3, ( employee_dict["idUser"], employee_dict["admin"], employee_dict['address'], employee_dict['cin'],  employee_dict['salary']))

                self.connexion.conn.commit()
                ("Added successfully")
        except Exception as e:
            print(f"addEmployee :Error: {e}")

    def updateEmployee(self, employee_dict,idUser):
        try:
            if self.connexion.connect():
                # Update the employee's data in the utilisateur table
                req1 = f"UPDATE utilisateur SET nom = '{employee_dict['nom']}', prenom = '{employee_dict['prenom']}', " \
                       f"login = '{employee_dict['login']}', mdp = '{employee_dict['mdp']}' WHERE idUser = {idUser}"
                self.connexion.cursor.execute(req1)

                # Update the employee's data in the super_utilisateur table
                req2 = f"UPDATE super_utilisateur SET admin = %s, address = %s, cin = %s, salary = %s WHERE idUser = %s"
                self.connexion.cursor.execute(req2,
                                              (employee_dict["admin"], employee_dict['address'], employee_dict['cin'],
                                               employee_dict['salary'], idUser))

                self.connexion.conn.commit()
                print("Successfully updated employee data")
        except Exception as e:
            print(f"edit_employee: Error: {e}")

    def delete(self, idUser):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"DELETE FROM `super_utilisateur` WHERE idUser= '{idUser}'"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()

                    req = f"DELETE FROM utilisateur WHERE idUser= '{idUser}'"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Car deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")





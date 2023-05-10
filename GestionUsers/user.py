
import conn
import base64

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


    def updateUser(self,client_dict):
        if(self.connexion.connect()):
            print("update use r: ")
            req = f"UPDATE utilisateur SET `login`=%s ,`mdp`=%s, `nom` = %s, " \
                  f" `prenom` = %s WHERE `idUser`=%s"

            self.connexion.cursor.execute(req, (client_dict['login'], client_dict['mdp'], client_dict['nom'],
                client_dict['prenom'], client_dict['idUser']))
            self.connexion.conn.commit()

            self.warning("Modifié avec succés : ")
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
        except Exception as e:
            print(f"error: {e}")
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



    # Search methods
    def searchByModel(self,model):
        req = f"SELECT * FROM voiture WHERE LOWER(model) like '{model.lower()}%'"
        return self.getDict(req)
    def searchByIdBrand(self,id_brand):
        req = f"SELECT * FROM voiture WHERE idMarque = {id_brand}"
        return self.getDict(req)

    def getCarById(self,id):
        req = f"SELECT * FROM voiture WHERE idCar = {id}"
        return self.getDict(req)


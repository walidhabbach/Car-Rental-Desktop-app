from main import conn
class Client:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
    def getClientsData(self,request):
        if(self.connexion.connect()):
            req = request
            self.connexion.cursor.execute(req)
            users = self.connexion.cursor.fetchall()
            return users
    def updateClient(self,client_dict):
        if(self.connexion.connect()):
            print("edit button triggered")
            print(client_dict)
            req = f"UPDATE client SET tel='{client_dict['tel']}', liste_noire = '{client_dict['liste_noire']}', " \
                  f" permis = '{client_dict['permis']}',observation='{client_dict['observation']}' WHERE idUser='{client_dict['idUser']}'"
            self.connexion.cursor.execute(req)
            self.connexion.conn.commit()
            print("updated successfully")
    def supprimerClient(self,id):
        req = f"DELETE FROM CLIENT WHERE IDUSER = '{id}'"
        self.connexion.cursor.execute(req)
        self.connexion.conn.commit()
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
    def updateClient(self,tel,radioOui,permis,observation,idUser):
        print("edit button triggered")
        req = f"UPDATE client SET tel='{tel}', liste_noire = '{radioOui}', " \
              f" permis = '{permis}',observation='{observation}' WHERE idUser='{idUser}'"
        self.connexion.cursor.execute(req)
        self.connexion.conn.commit()

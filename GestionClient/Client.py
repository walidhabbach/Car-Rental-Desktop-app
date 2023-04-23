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
    def getValuePairDataClient(self,request):
        vp = dict()
        req = request
        self.connexion.cursor.execute(req)
        users = self.connexion.cursor.fetchall()
        for user in users:
            vp[user[0]] = user[1]
        return vp
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
        req = f"DELETE FROM client WHERE IDUSER = '{id}'"
        self.connexion.cursor.execute(req)
        self.connexion.conn.commit()
        print("deleted succesfully")
    def addClient(self,client_dict):
        if(self.connexion.connect()):
            try:
                #create for the user a login and a password :
                req1 = f"INSERT INTO utilisateur(`nom`, `prenom`, `login`, `mdp`) VALUES ('{client_dict['nom']}','{client_dict['prenom']}','{client_dict['login']}','{client_dict['mdp']}')"
                self.connexion.cursor.execute(req1)
                self.connexion.conn.commit()

                #get the id of the current row :
                req2 = "SELECT LAST_INSERT_ID() FROM utilisateur"
                self.connexion.cursor.execute(req2)
                result = self.connexion.cursor.fetchone()
                client_id = result[0]
                print(client_id)

                #creating the client :
                req3 = f"INSERT INTO client(`idUser` ,`adresse`, `cin`, `photo`, `liste_noire`, `permis`, `passport`, `email`, `observation`," \
                      f" `societe`, `ville`, `tel`) VALUES ('{client_id}','{client_dict['adresse']}','{client_dict['cin']}',''," \
                      f"'{client_dict['liste_noire']}','{client_dict['permis']}','{client_dict['passport']}','{client_dict['email']}','{client_dict['observation']}','{client_dict['societe']}','{client_dict['ville']}','{client_dict['tel']}')"
                print(req3)
                self.connexion.cursor.execute(req3)
                self.connexion.conn.commit()
                print("Added  succesfully")
            except Exception as e:
                print(f"error : {e}")

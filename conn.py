import mysql.connector as mc

class Connexion:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.conn = None
        self.cursor=None

    def connect(self):
        flag = False
        try:
            self.conn = mc.connect(host=self.host, database=self.database, user=self.username, password=self.password)
            print("connect to database")
            flag = True
        except mc.Error as err:
            print(err)
        self.cursor = self.conn.cursor()
        return flag

    def affichage(self):
        print(self.cursor)




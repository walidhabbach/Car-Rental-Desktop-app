import conn
import car
class Fuel:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.car = car.Car()

    def getFuel(self):
        try:
            if self.connexion.connect():
                data = dict()
                with self.connexion.conn:
                    self.connexion.cursor.execute("SELECT idCarburant ,nom FROM carburant")
                    result = self.connexion.cursor.fetchall()
                    for row in result:
                        data[row[0]] = row[1]
                return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}  # Return default data dictionary
        finally:
            if self.connexion.cursor:
                self.connexion.cursor.close()
            if self.connexion.conn:
                self.connexion.conn.close()


    def searchByIdFuel(self,id_Fuel):
        req = f"SELECT * FROM voiture WHERE idCarburant = {id_Fuel}"
        return self.car.getDict(req)
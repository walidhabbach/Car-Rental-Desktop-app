
import conn
import base64
class Car:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")

    def getCar(self,req):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                   # req = f"SELECT * FROM voiture WHERE idVoiture = {car_id}"
                    self.connexion.cursor.execute(req)
                    result = self.connexion.cursor.fetchall()
                    return result
        except Exception as e:
            print(f"An error occurred: {e}")

    def addCar(self, brand, model, fuel, image):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = "INSERT INTO voiture(`idMarque`, `idCarburant`, `model`, `image`) VALUES (%s, %s, %s, %s)"
                    self.connexion.cursor.execute(req, (brand, fuel, model, image))
                    self.connexion.conn.commit()
                    print("Record added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def updateCar(self, car_id, brand, model, fuel):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"UPDATE voiture SET idMarque = {brand}, idCarburant = {fuel}, image = '{model}' WHERE idCar  = '{car_id}'"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Record updated successfully.")

        except Exception as e:
             print(f"An error occurred: {e}")
    def deleteCar(self, car_id):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"DELETE FROM `voiture` WHERE  idCar = '{car_id}'"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Record deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def getFuel(self):
        try:
            if self.connexion.connect():
                data = {}
                with self.connexion.conn:
                    self.connexion.cursor.execute("SELECT idCarburant ,nom FROM carburant")
                    result = self.connexion.cursor.fetchall()
                    for row in result:
                        data[row[0]] = row[1]
                        print(data)
                return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}  # Return default data dictionary
        finally:
            if self.connexion.cursor:
                self.connexion.cursor.close()
            if self.connexion.conn:
                self.connexion.conn.close()

    # Search methods
    def searchByModel(self,model):
        req = f"SELECT * FROM voiture WHERE model like '{model}%'"
        return self.getCar(req)
    def searchByIdBrand(self,id_brand):
        req = f"SELECT * FROM voiture WHERE idMarque = {id_brand}"
        return self.getCar(req)
    def searchByIdCar(self,id):
        req = f"SELECT * FROM voiture WHERE idCar = {id}"
        return self.getCar(req)

import brand
import conn
import base64

class Car:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")

    def get(self,req):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                   # req = f"SELECT * FROM voiture WHERE idVoiture = {car_id}"
                    self.connexion.cursor.execute(req)
                    result = self.connexion.cursor.fetchall()
                    return result
        except Exception as e:
            print(f"get : An error occurred: {e}")

    def add(self, brand, model, fuel, image):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = "INSERT INTO voiture(`idMarque`, `idCarburant`, `model`, `image`) VALUES (%s, %s, %s, %s)"
                    self.connexion.cursor.execute(req, (brand, fuel, model, image))
                    self.connexion.conn.commit()
                    print("Record added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self, car_id, brand, model, fuel, image):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = "UPDATE voiture SET idMarque = %s, idCarburant = %s, model = %s, image = %s WHERE idCar = %s"
                    values = (brand, fuel, model, image, car_id)
                    self.connexion.cursor.execute(req, values)
                    self.connexion.conn.commit()
                    print("Record updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")


        except Exception as e:
             print(f"An error occurred: {e}")
    def delete(self, car_id):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"DELETE FROM `voiture` WHERE  idCar = '{car_id}'"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Record deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")


    # Search methods
    def searchByModel(self,model):
        req = f"SELECT * FROM voiture WHERE model like '{model}%'"
        return self.get(req)
    def searchByIdBrand(self,id_brand):
        req = f"SELECT * FROM voiture WHERE idMarque = {id_brand}"
        return self.get(req)

    def getCarById(self,id):
        req = f"SELECT * FROM voiture WHERE idCar = {id}"
        return self.get(req)

    def getAll(self):
        req = f"SELECT * FROM voiture"
        return self.get(req)
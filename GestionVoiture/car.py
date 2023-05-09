import brand
import conn
import base64

class Car:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")

    def getDict(self, req):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    self.connexion.cursor.execute(req)
                    columns = [desc[0] for desc in self.connexion.cursor.description]

                    results = self.connexion.cursor.fetchall()
                    cars = []
                    for row in results:
                        cars.append(dict(zip(columns, row)))
                    return cars
        except Exception as e:
            print(f"get: An error occurred: {e}")

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

    def add(self, brand, model, fuel, image,idgear,price,power,seats,doors,production_date,image_links):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = "INSERT INTO voiture(`idMarque`, `idCarburant`, `model`, `image`, `power`, `seats`, `doors`, `price`,`idTransmission`,`production_date`,`image_links`) VALUES (%s, %s, %s, %s,%s,%s, %s, %s,%s,%s,%s)"
                    self.connexion.cursor.execute(req, (brand, fuel, model, image,power,seats,doors,price,idgear,production_date,image_links))
                    self.connexion.conn.commit()
                    print("Record added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self, car_id, brand, model, fuel, image,idTransmission,price,power,seats,doors,production_date,image_links):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = "UPDATE voiture SET idMarque = %s, idCarburant = %s, model = %s, image = %s,idTransmission=%s , power = %s ,  seats = %s ,  doors = %s ,  price = %s , image_links=%s,production_date=%s WHERE idCar = %s "
                    values = (brand, fuel, model, image,idTransmission,power,seats,doors,price,image_links,production_date, car_id)
                    self.connexion.cursor.execute(req, values)
                    self.connexion.conn.commit()
                    print("car has been updated successfully.")

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
                    print("Car deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")


    # Search methods
    def searchByModel(self,model):
        req = f"SELECT * FROM voiture WHERE model like '{model}%'"
        return self.getDict(req)
    def searchByIdBrand(self,id_brand):
        req = f"SELECT * FROM voiture WHERE idMarque = {id_brand}"
        return self.getDict(req)

    def getCarById(self,id):
        req = f"SELECT * FROM voiture WHERE idCar = {id}"
        return self.getDict(req)

    def getAll(self):
        req = f"SELECT * FROM voiture"
        return self.getDict(req)
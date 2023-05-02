
import conn
import base64
class Brand:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")

    def addBrands(self, logo, name):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    print("image_base64 ")
                    req = "INSERT INTO marque(`logo`, `name`) VALUES (%s, %s)"
                    self.connexion.cursor.execute(req, (logo, name))
                    self.connexion.conn.commit()
                    print("Record added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def getBrands(self):
        try:
            print("getBrands")
            if self.connexion.connect():
                data = dict()
                with self.connexion.conn:
                    self.connexion.cursor.execute("SELECT idMarque,nom FROM marque")
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
    def getBrandById(self,id):
        try:
            if self.connexion.connect():
                data = dict()
                with self.connexion.conn:
                    self.connexion.cursor.execute(f"SELECT nom FROM marque where idMarque='{id}'")
                    result = self.connexion.cursor.fetchall()
                return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}  # Return default data dictionary
        finally:
            if self.connexion.cursor:
                self.connexion.cursor.close()
            if self.connexion.conn:
                self.connexion.conn.close()
    def updateBrand(self, brand_id,logo, brand):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"UPDATE voiture SET name = {brand}, logo = '{logo}' WHERE idMarque  = {brand_id}"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Record updated successfully.")

        except Exception as e:
             print(f"An error occurred: {e}")
    def deleteBrand(self, brand_id):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"DELETE FROM marque WHERE idMarque  = {brand_id}"
                    self.connexion.cursor.execute(req)
                    self.connexion.conn.commit()
                    print("Record deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
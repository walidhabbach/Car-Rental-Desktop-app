
import conn
import base64
class Brand:
    def __init__(self):
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")

    def addBrand(self, name):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = "INSERT INTO marque(`nom`) VALUES (%s)"
                    self.connexion.cursor.execute(req, (name,))
                    self.connexion.conn.commit()
                    print("brand added successfully.")
        except Exception as e:
            print(f"addBrand : An error occurred: {e}")

    def getLastId(self):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = "SELECT idMarque FROM marque ORDER BY idMarque DESC LIMIT 1;"
                    self.connexion.cursor.execute(req)
                    result = self.connexion.cursor.fetchone()
                    if result:
                        last_id = result[0]
                        print(f"Last inserted ID: {last_id}")
                        return last_id
                    else:
                        print("No records found in the table.")
        except Exception as e:
            print(f"getLastId: An error occurred: {e}")
            return

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

    def getIdByBrand(self, brand):
        try:
            if self.connexion.connect():
                data = dict()
                with self.connexion.conn:
                    self.connexion.cursor.execute(f"SELECT idMarque FROM marque where LOWER(nom)='{brand.lower()}'")
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
    def updateBrand(self, brand_id, brand):
        try:
            if self.connexion.connect():
                with self.connexion.conn:
                    req = f"UPDATE voiture SET nom = {brand}  WHERE idMarque  = {brand_id}"
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
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import user
import conn
import string
import random
class Edit_Emp(QtWidgets.QMainWindow):
    def __init__(self,idUser):
        super().__init__()
        # self.tool = Tool.tool()
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.user = user.User()
        self.ui = uic.loadUi("../main/EditEmpForm_ui.ui", self)
        self.ui.genererPass_3.clicked.connect(self.generateRandomPassword)
        self.ui.valider_btn_emp_3.clicked.connect(self.EditButtonEmployee)
        self.idUser = idUser
        print(self.idUser)
        self.loadUserData()

    def loadUserData(self):
        try:
            data_Users = self.user.getSuperUserById(self.idUser)[0]
            print(data_Users)
            self.ui.nom_3.setText(data_Users['nom'])
            self.ui.prenom_3.setText(data_Users['prenom'])
            self.ui.login_3.setText(data_Users['login'])
            self.ui.mdp_3.setText(data_Users['mdp'])
            self.ui.adresse_3.setText(data_Users['address'])
            self.ui.cin_3.setText(data_Users['cin'])
            self.ui.salary_3.setValue(float(data_Users['salary']))
            self.ui.choix_admin_3.setCurrentIndex(int(data_Users['admin']))

            self.ui.phone_3.setText(data_Users['nom'])
        except Exception as e:
            print(f"loadUserData :Error: {e}")

    def EditButtonEmployee(self):
        try:
            employee_dict= dict()
            employee_dict['nom'] = self.ui.nom_3.text()
            employee_dict['prenom'] = self.ui.prenom_3.text()
            employee_dict['login'] = self.ui.login_3.text()
            employee_dict['mdp'] = self.ui.mdp_3.text()
            employee_dict['address'] = self.ui.adresse_3.text()
            employee_dict['cin'] = self.ui.cin_3.text()

            employee_dict['phone'] = self.ui.phone_3.text()
            employee_dict['salary'] = float(self.ui.salary_3.value())

            employee_dict['admin'] = self.ui.choix_admin_3.currentIndex()

            if employee_dict['nom'] == "":
                self.tool.warning("Please enter a name.")
                return
            elif employee_dict['prenom'] == "":
                self.tool.warning("Please enter last name.")
                return
            elif employee_dict['login'] == "":
                self.tool.warning("enter a login.")
                return
            elif employee_dict['mdp'] == "":
                self.tool.warning("mdp")
                return
            elif employee_dict['address'] == "":
                self.tool.warning("address")
                return
            elif employee_dict['cin'] == "":
                self.tool.warning("cin")
                return
            elif employee_dict['phone'] == "":
                self.tool.warning("phone")
                return
            elif employee_dict['salary'] == "":
                self.tool.warning("salary")
                return
            elif employee_dict['phone'] == "":
                self.tool.warning("phone")
                return

            self.user.updateEmployee(employee_dict,self.idUser)
            #self.tool.warning("user added ")

        except Exception as e:
            print(f"EditButtonEmployee :Error: {e}")



    def generateRandomPassword(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = str()
        for i in range(5):
            password += random.choice(characters)
        self.ui.mdp_3.setText(password)

    def clearField(self):
        self.ui.nom_3.setText("")
        self.ui.prenom_3.setText("")
        self.ui.login_3.setText("")
        self.ui.mdp_3.setText("")
        self.ui.adresse_3.setText("")
        self.ui.cin_3.setText("")
        self.ui.salary_3.setValue(0)
        self.ui.choix_admin_3.setCurrentIndex(0)

        self.ui.phone_3.setText("")




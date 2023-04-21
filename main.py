import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from car import Car
import conn
from PyQt5.QtWidgets import QTableWidgetItem,QFileDialog,QLabel
from PyQt5.QtGui import QPixmap
import base64

class MainWindow(QtWidgets.QMainWindow):
    car = Car()
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("MainWin.ui", self)
        self.connexion = conn.Connexion(host="localhost", username="root", password="", database="Location_voiture")
        self.ui.btnCrud_clients.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.page_crud_clients))
        self.ui.btnCrud_users.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_users))
        self.ui.btnCrud_cars.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.page_crud_cars))
        self.connect_to_database()

        #Add Car Section
        self.ui.AddButton.clicked.connect(self.addCarButton)
        self.displayCars()
        self.addImage.clicked.connect(self.image_dialog)

    def connect_to_database(self):
        self.connexion.connect()
        if(self.connexion.connect()):
            QtWidgets.QMessageBox.information(self, "Success", "Connected to database")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to connect to database")

    # Add Car Section
    def convertToBinary(self,path):
        try:
            with open(path, "rb") as File:
                binary_data = File.read()
            return binary_data
        except FileNotFoundError:
            print(f"Error: File not found at path '{path}'")
        except PermissionError:
            print(f"Error: Permission denied to read file at path '{path}'")
        except Exception as e:
            print(f"An error occurred: {e}")
    def addCarButton(self):
        brand = self.ui.brand.text()
        model = self.ui.model.text()
        fuel = self.ui.fuel.text()

        img = self.convertToBinary(self.imagePath)
        print(img)
        self.car.addCar(brand, model, fuel,img)

    def displayCars(self):
        self.ui.tableWidget.clearContents()  # Clear the existing data in the table
        cars = self.car.getCar("SELECT * FROM voiture;")
        self.ui.tableWidget.setColumnCount(4)  # Set the number of columns in the table
        self.ui.tableWidget.setHorizontalHeaderLabels(['idCar', 'Brand', 'Model', 'Fuel'])  # Set the column labels
        self.ui.tableWidget.setRowCount(len(cars))  # Set the number of rows in the table

        for row_idx, car in enumerate(cars):
            for col_idx, item in enumerate(car):
                self.ui.tableWidget.setItem(row_idx, col_idx,
                                            QTableWidgetItem(str(item)))  # Set the table item with the data

        self.ui.tableWidget.resizeColumnsToContents()  # Resize the columns to fit the content


    def image_dialog(self):
        try:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Image files (*.jpg *.jpeg *.png *.bmp)")
            if file_dialog.exec_():
                file_path = file_dialog.selectedFiles()[0]

                self.imagePath = file_path

                print( self.imagePath)
                pixmap = QPixmap(file_path)
                # Set the desired size
                desired_size = QtCore.QSize(200, 150)  # Width, Height
                # Scale the pixmap to the desired size
                pixmap = pixmap.scaled(desired_size, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)
                self.image_label.adjustSize()
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

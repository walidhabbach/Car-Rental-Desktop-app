from GestionVoiture import car
from GestionVoiture import brand
from GestionVoiture import fuel
from Scraping import scraping

import base64
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox ,QComboBox
from PyQt5 import QtCore


class tool:

    def __init__(self):
        self.scraping = scraping.scrap()
        self.car = car.Car()
        self.brand = brand.Brand()
        self.fuel = fuel.Fuel()
    def convertToBinary(self, path):
        try:
            with open(path, "rb") as File:
                binary_data = File.read()
            return binary_data
        except FileNotFoundError:
            print(f"Error: File not found at path '{path}'")
        except PermissionError:
            print(f"Error: Permission denied to read file at path '{path}'")
        except Exception as e:
            print(f"An error occurred convertToBinary : {e}")

    def getImageLabel(self, binary_data):
        try:
            # Convert binary data to base64-encoded string
            base64_data = base64.b64encode(binary_data).decode()
            # Create QPixmap from base64-encoded string
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(base64_data))
            return pixmap
        except Exception as e:
            print(f"An error occurred getImageLabel : {e}")
    def warning(self,message):

        # Create an instance of QMessageBox
        msg_box = QMessageBox()

        # Set the icon and title
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Error")

        # Set the text or message
        msg_box.setText(message)

        # Set additional buttons (optional)
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Set the appearance (optional)
        msg_box.setStyleSheet("QMessageBox { background-color: lightgray; }")

        # Show the message box and wait for user response
        result = msg_box.exec_()

        # Check the user response
        if result == QMessageBox.Ok:
            # User clicked OK, handle the event
            pass
    def fill_combobox(self,combo,brand=None):
        print(1)
        try:
            combo.clear()
            data = dict()
            print(combo.objectName())
            if combo.objectName() == 'comboBoxBrand' or combo.objectName() == 'comboBoxBrand_1':
                combo.addItem('All Brands')
                data = self.brand.getBrands()
            elif combo.objectName() == 'comboBoxFuel' or combo.objectName() == 'comboBoxFuel_1':
                combo.addItem('Select Fuel')
                data = self.fuel.getFuel()
            elif combo.objectName() == 'comboAllBrands':
                print("combo.addItem('Select Brand')")
                combo.addItem('Select Brand')
                print("combo.addItem('Select Brand')")
                data = self.scraping.getCarBrandAll()

            elif combo.objectName() == 'comboAllModels' and brand is not None:
                combo.addItem('Select Model')
                data = self.scraping.getCarModelsByBrand(brand)
            print(data)
            for key, value in data.items():
                combo.addItem(value)
                combo.setItemData(combo.count() - 1, key)

            return data
        except Exception as e:
            print(f"fill_combobox: {e}")
    def handlClick(self, index: QtCore.QModelIndex, table):
        try:
            row = index.row()
            idCar = table.item(row, 1)
            column = index.column()
            if table.horizontalHeaderItem(column).text() == "Delete":
                self.car.delete(int(idCar.text()))
                table.removeRow(row)
                return None
            # Edit Car:
            return int(idCar.text())

        except Exception as e:
            print(f"handlClick: {e}")

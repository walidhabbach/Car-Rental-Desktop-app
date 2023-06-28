import sys
sys.path.append("../GestionVoiture/")
from GestionVoiture import car
from GestionVoiture import brand
from GestionVoiture import fuel
from GestionVoiture import transmission
sys.path.append("../GestionUsers/")
from GestionUsers import user
from GestionUsers import EditEmp as ep

from Scraping import scraping
from PIL import Image
import base64
from PyQt5.QtGui import  QPixmap, QImage, qRgb, qRed, qGreen, qBlue
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QImage
import numpy as np
from PyQt5.QtCore import QByteArray, QBuffer, Qt


class tool:

    def __init__(self):
        try:
            self.scraping = scraping.scrap()
            self.car = car.Car()
            self.user = user.User()
            self.brand = brand.Brand()
            self.fuel = fuel.Fuel()
            self.gearBox = transmission.Transmission()
        except Exception as e:
            print(e)
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


    def label_to_binary(self,qpixmap):
        # Get the QPixmap from the QLabel
        pixmap = qpixmap.pixmap()
        qimage = pixmap.toImage()

        # Convert the QImage to a numpy array
        buffer = qimage.bits().asstring(qimage.byteCount())
        arr = np.frombuffer(buffer, dtype=np.uint8).reshape(qimage.height(), qimage.width(), 4)

        # Convert the numpy array to a binary image
        gray = arr[:, :, 0]
        binary = np.where(gray < 128, 0, 255)

        return binary



    def label_to_byte_array(self,label):
        # Get the pixmap from the label
        pixmap = label.pixmap()

        # Convert the pixmap to a QImage
        qimage = pixmap.toImage()

        # Convert the QImage to a QByteArray
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QBuffer.WriteOnly)
        qimage.save(buffer, "PNG")

        return byte_array

    def qlabel_to_binary(self,qlabel):
        # Get the QPixmap from the QLabel
        pixmap = qlabel.pixmap()
        # Convert the QPixmap to a QImage
        qimage = pixmap.toImage()
        # Create a binary image from the QImage
        binary = []
        for y in range(qimage.height()):
            row = []
            for x in range(qimage.width()):
                pixel = qimage.pixel(x, y)
                gray = qRgb(qRed(pixel), qGreen(pixel), qBlue(pixel))
                if gray < qRgb(128, 128, 128):
                    row.append(0)
                else:
                    row.append(255)
            binary.append(row)
        return binary
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

        try:
            combo.clear()
            data = dict()
            print(combo.objectName())
            if combo.objectName() == 'comboBoxGear_1' :
                combo.addItem('Select Transmission')
                data = self.gearBox.getGearBox()
            if combo.objectName() == 'comboBoxBrand' or combo.objectName() == 'comboBoxBrand_1':
                combo.addItem('All Brands')
                data = self.brand.getBrands()
            elif combo.objectName() == 'comboBoxFuel' or combo.objectName() == 'comboBoxFuel_1':
                combo.addItem('Select Fuel')
                data = self.fuel.getFuel()
                print(data)
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
            if "tableWidgeModels" == table.objectName():
                column = index.column()
                return table.item(row, 1).text()
            elif "tableWidgetUsers" == table.objectName():
                idUser = int(table.item(row, 0).text())
                column = index.column()
                print(column)
                print(idUser)
                if table.horizontalHeaderItem(column).text() == "Delete":
                    # Ask the user to confirm before deleting:
                    confirm = QMessageBox.question(None, "Confirmation", "Are you sure you want to delete this user?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if confirm == QMessageBox.Yes:
                        self.user.delete(idUser)
                        table.removeRow(row)
                        self.warning(f"user id :{idUser} has been deleted")
                    else:
                        return None
                elif table.horizontalHeaderItem(column).text() == "Edit":
                    # Edit Emp:
                    editemp = ep.Edit_Emp(int(idUser))
                    editemp.show()
                    return idUser

            elif "tableWidgetCar" == table.objectName():
                idCar = int(table.item(row, 1).text())
                column = index.column()
                print(column)
                if table.horizontalHeaderItem(column).text() == "Delete":
                    # Ask the user to confirm before deleting:
                    confirm = QMessageBox.question(None,"Confirmation","Are you sure you want to delete this car?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
                    if confirm == QMessageBox.Yes:
                        self.car.delete(idCar)
                        table.removeRow(row)
                        self.warning(f"Car id :{idCar} has been deleted")
                    else:
                        return None
                elif table.horizontalHeaderItem(column).text() == "Edit":
                    # Edit Car:
                    return idCar

            return
        except Exception as e:
            print(f"handlClick: {e}")
            return

    def alignItemsCenter(self,table):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item is not None:
                    item.setTextAlignment(Qt.AlignCenter)
import base64

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox


class tool:
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
            print(f"An error occurred: {e}")

    def getImageLabel(self, binary_data):
        try:
            # Convert binary data to base64-encoded string
            base64_data = base64.b64encode(binary_data).decode()
            # Create QPixmap from base64-encoded string
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(base64_data))
            return pixmap
        except Exception as e:
            print(f"An error occurred: {e}")
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

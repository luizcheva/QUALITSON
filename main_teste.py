# import sys
# from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QLineEdit, QPushButton


# class meuForms(QMainWindow):
#     def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
#         super().__init__(parent, *args, **kwargs)
#         self.cw = QWidget()
#         self.vLayout = QVBoxLayout()
#         self.cw.setLayout(self.vLayout)
#         self.setCentralWidget(self.cw)

#         scroll = QLineEdit()
#         self.vLayout.addWidget(scroll)

#         new = QWidget()
#         bottom = QVBoxLayout(new)
#         btn = QPushButton("Testess")

#         bottom.addWidget(btn)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = meuForms()

#     window.show()
#     app.exec()

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

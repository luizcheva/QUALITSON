import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from files.ui import ChatWindow
from variables import WINDOW_ICON_PATH
from files.theme import setupTheme


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme()
    window = ChatWindow()

    # Icone
    icon = QIcon()
    icon.addFile(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    window.show()
    app.exec()

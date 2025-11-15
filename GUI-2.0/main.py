

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QStackedLayout
from PyQt6.QtCore import QSize

import qt_themes

from database import init_db  # Import db creation function from database.py file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        init_db()  # function call once to create a new database

app = QApplication([])

qt_themes.set_theme('monokai')

window = MainWindow()
window.show()

app.exec()

# Reference
# https://github.com/beatreichenbach/qt-themes?tab=readme-ov-file
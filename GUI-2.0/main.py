

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QStackedLayout
from PyQt6.QtCore import QSize

import qt_themes

from database import seed_data # imported function to add entries

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        # init_db()
        seed_data() # function call to add entries

app = QApplication([])

qt_themes.set_theme('monokai')

window = MainWindow()
window.show()

app.exec()

# Reference
# https://github.com/beatreichenbach/qt-themes?tab=readme-ov-file
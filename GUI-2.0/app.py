

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QStackedLayout
from PyQt6.QtCore import QSize

import qt_themes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")

app = QApplication([])

qt_themes.set_theme('monokai')

window = MainWindow()
window.show()

app.exec()

# Reference
# https://github.com/beatreichenbach/qt-themes?tab=readme-ov-file
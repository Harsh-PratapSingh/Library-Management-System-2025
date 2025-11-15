

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QStackedLayout, QLabel
from PyQt6.QtCore import QSize
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import pyqtSignal

import qt_themes

from database import init_db, seed_data

import os
os.environ["QT_SCALE_FACTOR"] = "2.0"  # Increased app scaling

from auth_page import AuthPage
from user_page import UserPage
from admin_page import AdminPage




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("Library-Management-System-2025/Database/library.db")
        db.open()

        self.setWindowTitle("Library Management System")

        # init_db()
        # seed_data() 

        self.setFixedSize(QSize(1242, 770))
        
        # Create stacked layout
        self.stacked_layout = QStackedLayout()
        
        # Create pages
        self.auth_page = AuthPage()
        self.auth_page.login_success.connect(self.open_page)
        self.user_page = UserPage()
        self.admin_page = AdminPage()
        
        # Add pages to stack (index 0 = auth, 1 = user, 2 = admin)
        self.stacked_layout.addWidget(self.auth_page)
        self.stacked_layout.addWidget(self.user_page)
        self.stacked_layout.addWidget(self.admin_page)
        
        # Set stacked layout as central widget
        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)
        
        # Start on auth page
        self.stacked_layout.setCurrentIndex(0)

    def open_page(self, role):
        if role == 'user':   
            self.stacked_layout.setCurrentIndex(1)
            self.user_page.user_id = self.auth_page.user_id
        else:
            self.stacked_layout.setCurrentIndex(2)
            self.admin_page.user_id = self.auth_page.user_id

        

app = QApplication([])

qt_themes.set_theme('monokai')

window = MainWindow()
window.show()

app.exec()

# Reference
# https://github.com/beatreichenbach/qt-themes?tab=readme-ov-file
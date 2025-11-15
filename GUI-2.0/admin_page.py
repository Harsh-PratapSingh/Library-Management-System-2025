from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont

class AdminPage(QWidget):
    def __init__(self):
        super().__init__()

        self.user_id = None
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Admin Dashboard")
        title.setFont(QFont("Arial", 16))
        layout.addWidget(title)
        
        # Placeholder content for admin features
        admin_info = QLabel("Manage users, add/edit books, view reports.")
        admin_info.setFont(QFont("Arial", 12))
        layout.addWidget(admin_info)
        
        layout.addStretch()

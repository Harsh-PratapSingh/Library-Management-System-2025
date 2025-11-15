from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont

class UserPage(QWidget):
    def __init__(self):
        super().__init__()

        self.user_id = None
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("User Dashboard")
        title.setFont(QFont("Arial", 16))
        layout.addWidget(title)
        
        # Placeholder content for user features
        welcome = QLabel("Welcome! Search books, borrow books, view history.")
        welcome.setFont(QFont("Arial", 12))
        layout.addWidget(welcome)
        
        layout.addStretch()
